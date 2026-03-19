#!/usr/bin/env python3
import json
import threading
import time

import rclpy
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node

from geometry_msgs.msg import Pose, PoseStamped
from std_msgs.msg import Bool
from tf2_geometry_msgs import do_transform_pose
from tf2_ros import Buffer, TransformListener

from eddie_ros.action import ArmControl, GripperControl
from cartesian_planner.srv import PlanScanPath
from pick_place_fsm.action import Perception
from coord_dsl.fsm import fsm_step
from coord_dsl.event_loop import reconfig_event_buffers, produce_event
from fsm_door_disassemble import create_fsm, StateID, EventID


class DoorDisassembleNode(Node):
    def __init__(self):
        super().__init__("door_disassemble_fsm_py")

        self.fsm = create_fsm()
        self.user_data = {
            "last_state": StateID.S_IDLE,
            "action_dispatched": False,
            "view_pose_global": self.get_default_view_pose_global(),
            "table_drop_pose_global": self.get_default_table_drop_pose_global(),
            "subdoor_poses": [],
            "car_objects": {},
            "active_object_detection": None,
            "active_object_radius": 0.0,
            "active_object_class": "",
            "scan_message": "",
            "scan_screw_poses": [],
            "arm_motion_mode": "",
            "pending_object_classes": [],
        }

        self.declare_parameter("base_frame", "eddie_base_link")
        self.declare_parameter("ee_frame", "eddie_right_arm_robotiq_85_grasp_link")
        self.declare_parameter("camera_frame", "eddie_right_arm_camera_link")
        self.declare_parameter("perception_action_server", "perception")
        self.declare_parameter("car_object_classes", ["motor", "unit"])

        self.base_frame = self.get_parameter("base_frame").value
        self.ee_frame = self.get_parameter("ee_frame").value
        self.camera_frame = self.get_parameter("camera_frame").value
        self.perception_action_server = self.get_parameter("perception_action_server").value
        self.car_object_classes = list(self.get_parameter("car_object_classes").value)
        self.object_pick_z_offset = 0.1

        self.cb_group = ReentrantCallbackGroup()
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.arm_client = ActionClient(
            self, ArmControl, "right_arm/arm_control", callback_group=self.cb_group
        )
        self.gripper_client = ActionClient(
            self, GripperControl, "right_arm/gripper_control", callback_group=self.cb_group
        )
        self.perception_client = ActionClient(
            self, Perception, self.perception_action_server, callback_group=self.cb_group
        )
        self.scan_client = self.create_client(
            PlanScanPath, "plan_scan_path", callback_group=self.cb_group
        )
        self.create_subscription(
            Bool,
            "/door_disassemble/abort",
            self.abort_callback,
            10,
            callback_group=self.cb_group,
        )

        self.fsm_timer = self.create_timer(0.1, self.fsm_loop, callback_group=self.cb_group)

        self.input_thread = threading.Thread(target=self.input_loop, daemon=True)
        self.input_thread.start()

        self.get_logger().info("Door disassemble node ready.")
        self.get_logger().info("Press Enter to start. Type 'a' + Enter to abort.")

    def get_default_view_pose_global(self) -> Pose:
        p = Pose()
        p.position.x = 0.749
        p.position.y = 0.003
        p.position.z = 0.339
        p.orientation.x = 0.475857
        p.orientation.y = 0.493639
        p.orientation.z = 0.546011
        p.orientation.w = 0.481407
        return p

    def get_default_table_drop_pose_global(self) -> Pose:
        p = Pose()
        p.position.x = 0.60
        p.position.y = -0.66
        p.position.z = 0.343951
        p.orientation.x = 0.475857
        p.orientation.y = 0.493639
        p.orientation.z = 0.546011
        p.orientation.w = 0.481407
        return p

    def abort_callback(self, msg: Bool):
        if msg.data:
            self.get_logger().warn("Abort message received.")
            produce_event(self.fsm.event_data, EventID.E_ABORT)

    def input_loop(self):
        while rclpy.ok():
            try:
                cmd = input(">> Enter=start, 'a'=abort\n").strip().lower()
            except EOFError:
                break

            if cmd == "a":
                produce_event(self.fsm.event_data, EventID.E_ABORT)
                continue

            if self.fsm.current_state_index == StateID.S_IDLE:
                produce_event(self.fsm.event_data, EventID.E_START)
            else:
                self.get_logger().info("FSM is busy. Use 'a' to abort.")

            time.sleep(0.2)

    def fsm_loop(self):
        if self.fsm.current_state_index == StateID.S_EXIT:
            self.get_logger().info("FSM reached EXIT state. Shutting down.")
            raise SystemExit

        if self.fsm.current_state_index != self.user_data["last_state"]:
            state_name = StateID(self.fsm.current_state_index).name
            self.get_logger().info(f"State changed to: {state_name}")
            self.user_data["last_state"] = self.fsm.current_state_index
            self.user_data["action_dispatched"] = False

        self.fsm_behavior()
        fsm_step(self.fsm)
        reconfig_event_buffers(self.fsm.event_data)

    def fsm_behavior(self):
        cs = self.fsm.current_state_index
        ud = self.user_data

        if cs == StateID.S_IDLE:
            return

        if cs == StateID.S_INITIALIZE and not ud["action_dispatched"]:
            self.get_logger().info("Initializing...")
            time.sleep(3.0)
            self.get_logger().info("Initialized.")
            produce_event(self.fsm.event_data, EventID.E_INIT_DONE)
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_MOVE_TO_VIEW_POSE and not ud["action_dispatched"]:
            self.get_logger().info("Moving arm to global view pose...")
            ud["arm_motion_mode"] = "VIEW_POSE"
            produce_event(self.fsm.event_data, EventID.E_GO_MOVE_ARM)
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_GET_SUBDOOR and not ud["action_dispatched"]:
            self.get_logger().info("Requesting subdoor poses from perception action...")
            self.request_perception("subdoor", "", self.on_subdoor_result)
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_GET_OBJECTS and not ud["action_dispatched"]:
            self.get_logger().info(
                "Requesting car object poses from perception action for classes "
                f"{self.car_object_classes}..."
            )
            self.request_car_objects()
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_RASTER_SCAN and not ud["action_dispatched"]:
            self.get_logger().info("Calling raster scan service /plan_scan_path ...")
            if not self.scan_client.wait_for_service(timeout_sec=2.0):
                self.get_logger().error("Raster scan service not available.")
                produce_event(self.fsm.event_data, EventID.E_SCAN_FAIL)
                ud["action_dispatched"] = True
                return
            
            if len(ud["subdoor_poses"]) < 4:
                self.get_logger().error("Need 4 subdoor poses before raster scan.")
                produce_event(self.fsm.event_data, EventID.E_SCAN_FAIL)
                ud["action_dispatched"] = True
                return
            
            req = PlanScanPath.Request()
            req.top_left = ud["subdoor_poses"][0]
            req.top_right = ud["subdoor_poses"][1]
            req.bottom_right = ud["subdoor_poses"][2]
            req.bottom_left = ud["subdoor_poses"][3]
            # Uncomment below two lines and comment out produce event line to enable raster scan
            # future = self.scan_client.call_async(req)
            # future.add_done_callback(self.on_scan_response)
            produce_event(self.fsm.event_data, EventID.E_SCAN_DONE)
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_RETURN_TO_HOME_POSE and not ud["action_dispatched"]:
            self.get_logger().info("Returning to default home/view pose after scan...")
            ud["arm_motion_mode"] = "RETURN_HOME"
            produce_event(self.fsm.event_data, EventID.E_GO_MOVE_ARM)
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_MOVE_ARM and not ud["action_dispatched"]:
            target = None
            success_evt = None
            fail_evt = None
            context = "arm motion"

            if ud["arm_motion_mode"] == "VIEW_POSE":
                target = self.global_pose_to_relative_pose(
                    ud["view_pose_global"], self.base_frame, self.ee_frame
                )
                success_evt = EventID.E_VIEW_POSE_DONE
                fail_evt = EventID.E_VIEW_POSE_FAIL
                context = "move to global view pose"
            elif ud["arm_motion_mode"] == "RETURN_HOME":
                target = self.global_pose_to_relative_pose(
                    ud["view_pose_global"], self.base_frame, self.ee_frame
                )
                success_evt = EventID.E_RETURN_HOME_DONE
                fail_evt = EventID.E_RETURN_HOME_FAIL
                context = "return to default home/view pose"
            elif ud["arm_motion_mode"] == "PICK_OBJECT":
                target = self.object_pose_to_relative_pose(
                    ud["active_object_detection"], z_offset=self.object_pick_z_offset
                )
                success_evt = EventID.E_PICK_OBJECT_DONE
                fail_evt = EventID.E_ARM_MOVE_FAIL
                context = "move to object pre-pick pose"
                if target is None:
                    self.get_logger().error("Failed to resolve target during object pre-pick.")
                    produce_event(self.fsm.event_data, fail_evt)
                else:
                    self.get_logger().info("Executing arm motion: move to object pre-pick pose")
                    self.send_pick_object_sequence(
                        target,
                        self.make_relative_offset_pose(dz=self.object_pick_z_offset),
                        success_evt,
                        fail_evt,
                    )
                ud["action_dispatched"] = True
                return
            elif ud["arm_motion_mode"] == "RETREAT_WITH_OBJECT":
                target = self.make_relative_offset_pose(dz=-self.object_pick_z_offset)
                success_evt = EventID.E_RETREAT_WITH_OBJECT_DONE
                fail_evt = EventID.E_ARM_MOVE_FAIL
                context = "retreat with grasped object"
            elif ud["arm_motion_mode"] == "MOVE_TO_TABLE_DROP":
                target = self.global_pose_to_relative_pose(
                    ud["table_drop_pose_global"], self.base_frame, self.ee_frame
                )
                success_evt = EventID.E_MOVE_TO_TABLE_DONE
                fail_evt = EventID.E_ARM_MOVE_FAIL
                context = "move to table drop pose"
            elif ud["arm_motion_mode"] == "POST_DROP_HOME":
                target = self.global_pose_to_relative_pose(
                    ud["view_pose_global"], self.base_frame, self.ee_frame
                )
                success_evt = EventID.E_POST_DROP_HOME_DONE
                fail_evt = EventID.E_POST_DROP_HOME_FAIL
                context = "return to default home/view pose after drop"

            if success_evt is None or fail_evt is None:
                self.get_logger().error(
                    f"S_MOVE_ARM has no valid motion to execute. mode={ud['arm_motion_mode']}"
                )
                produce_event(self.fsm.event_data, EventID.E_ABORT)
            elif target is None:
                self.get_logger().error(f"Failed to resolve target during {context}.")
                produce_event(self.fsm.event_data, fail_evt)
            else:
                self.get_logger().info(f"Executing arm motion: {context}")
                self._send_direct_arm_goal(target, success_evt, fail_evt, context)
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_EXECUTE_SCREWDRIVER_PROBE and not ud["action_dispatched"]:
            self.execute_screwdriver_probe()
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_SELECT_NEXT_OBJECT and not ud["action_dispatched"]:
            if not self.select_next_car_object():
                self.get_logger().info("No more objects left to pick.")
                produce_event(self.fsm.event_data, EventID.E_NO_MORE_OBJECTS)
            else:
                self.get_logger().info(
                    "Selected next object pose from perception results "
                    f"class='{ud['active_object_class']}' "
                    f"with radius {ud['active_object_radius']}."
                )
                ud["arm_motion_mode"] = "PICK_OBJECT"
                produce_event(self.fsm.event_data, EventID.E_OBJECT_READY)
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_CLOSE_GRIPPER and not ud["action_dispatched"]:
            self.send_gripper_command(
                100.0,
                EventID.E_GRIPPER_CLOSE_DONE,
                EventID.E_GRIPPER_FAIL,
                "close gripper on object",
            )
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_RETREAT_ARM_WITH_OBJECT and not ud["action_dispatched"]:
            self.get_logger().info("Retreating with grasped object...")
            ud["arm_motion_mode"] = "RETREAT_WITH_OBJECT"
            produce_event(self.fsm.event_data, EventID.E_GO_MOVE_ARM)
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_MOVE_TO_TABLE_DROP_POSE and not ud["action_dispatched"]:
            self.get_logger().info("Moving to table drop pose...")
            ud["arm_motion_mode"] = "MOVE_TO_TABLE_DROP"
            produce_event(self.fsm.event_data, EventID.E_GO_MOVE_ARM)
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_OPEN_GRIPPER and not ud["action_dispatched"]:
            self.send_gripper_command(
                0.0,
                EventID.E_GRIPPER_OPEN_DONE,
                EventID.E_GRIPPER_FAIL,
                "open gripper to drop object",
            )
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_RETURN_HOME_AFTER_DROP and not ud["action_dispatched"]:
            self.get_logger().info("Returning to home/view pose after drop...")
            ud["arm_motion_mode"] = "POST_DROP_HOME"
            produce_event(self.fsm.event_data, EventID.E_GO_MOVE_ARM)
            ud["action_dispatched"] = True
            return

        if cs == StateID.S_CONFIRM_DATA and not ud["action_dispatched"]:
            self.get_logger().info("Confirm step reached. Stored data summary:")
            self.get_logger().info(f"Subdoor poses: {len(ud['subdoor_poses'])}")
            self.get_logger().info(f"Car objects: {list(ud['car_objects'].keys())}")
            self.get_logger().info(f"Raster scan message: {ud['scan_message']}")
            self.get_logger().info(f"Raster screws: {len(ud['scan_screw_poses'])}")
            produce_event(self.fsm.event_data, EventID.E_CONFIRM_DONE)
            ud["action_dispatched"] = True

    def global_pose_to_relative_pose(
        self, global_pose: Pose, global_frame: str, target_frame: str
    ) -> Pose | None:
        try:
            transform = self.tf_buffer.lookup_transform(
                target_frame, global_frame, rclpy.time.Time()
            )
            return do_transform_pose(global_pose, transform)
        except Exception as e:
            self.get_logger().warn(f"Failed to transform global pose to relative: {e}")
            return None

    def relative_pose_to_global_pose(
        self, relative_pose: Pose, relative_frame: str, global_frame: str
    ) -> Pose | None:
        try:
            transform = self.tf_buffer.lookup_transform(
                global_frame, relative_frame, rclpy.time.Time()
            )
            return do_transform_pose(relative_pose, transform)
        except Exception as e:
            self.get_logger().warn(f"Failed to transform relative pose to global: {e}")
            return None

    def object_pose_to_relative_pose(self, detection, z_offset=0.0) -> Pose | None:
        if detection is None:
            self.get_logger().error("Active object detection is missing pose data.")
            return None

        transformed_pose = self.global_pose_to_relative_pose(
            detection.pose, detection.header.frame_id, self.ee_frame
        )
        if transformed_pose is None:
            return None

        transformed_pose.orientation.x = 0.0
        transformed_pose.orientation.y = 0.0
        transformed_pose.orientation.z = 0.0
        transformed_pose.orientation.w = 1.0
        transformed_pose.position.z -= z_offset
        return transformed_pose

    def get_next_available_object_class(self) -> str | None:
        for object_class in self.car_object_classes:
            if object_class in self.user_data["car_objects"]:
                return object_class
        return None

    def select_next_car_object(self) -> bool:
        object_class = self.get_next_available_object_class()
        if object_class is None:
            return False

        active_object = self.user_data["car_objects"][object_class]
        self.user_data["active_object_class"] = object_class
        self.user_data["active_object_detection"] = active_object["pose"]
        self.user_data["active_object_radius"] = active_object["radius"]
        return True

    def clear_active_car_object(self):
        self.user_data["active_object_detection"] = None
        self.user_data["active_object_radius"] = 0.0
        self.user_data["active_object_class"] = ""

    def transform_pose_stamped_to_base(self, pose_stamped: PoseStamped) -> PoseStamped | None:
        transformed_pose = self.relative_pose_to_global_pose(
            pose_stamped.pose, pose_stamped.header.frame_id, self.base_frame
        )
        if transformed_pose is None:
            return None

        result = PoseStamped()
        result.header.frame_id = self.base_frame
        result.header.stamp = self.get_clock().now().to_msg()
        result.pose = transformed_pose
        return result

    def transform_pose_array_to_base(self, poses):
        transformed_poses = []
        for index, pose_stamped in enumerate(poses):
            transformed_pose = self.transform_pose_stamped_to_base(pose_stamped)
            if transformed_pose is None:
                self.get_logger().error(
                    f"Failed to transform perception pose {index} into {self.base_frame}."
                )
                return None
            transformed_poses.append(transformed_pose)
        return transformed_poses

    def make_relative_offset_pose(self, dx=0.0, dy=0.0, dz=0.0) -> Pose:
        p = Pose()
        p.position.x = dx
        p.position.y = dy
        p.position.z = dz
        p.orientation.w = 1.0
        return p

    def on_scan_response(self, future):
        try:
            resp = future.result()
            if resp is None:
                self.get_logger().error("Raster scan service returned no response.")
                produce_event(self.fsm.event_data, EventID.E_SCAN_FAIL)
                return

            self.user_data["scan_message"] = resp.message
            self.user_data["scan_screw_poses"] = []

            if resp.success:
                # Optional parse of planner payload:
                # {"status": "...", "screw_poses": [...]}
                try:
                    payload = json.loads(resp.message) if resp.message else {}
                    screws = payload.get("screw_poses", [])
                    if isinstance(screws, list):
                        self.user_data["scan_screw_poses"] = screws
                    else:
                        detected = payload.get("detected_objects", {})
                        if isinstance(detected, dict):
                            self.user_data["scan_screw_poses"] = list(detected.values())
                except Exception:
                    pass

                self.get_logger().info("Raster scan completed.")
                produce_event(self.fsm.event_data, EventID.E_SCAN_DONE)
            else:
                self.get_logger().error(f"Raster scan failed: {resp.message}")
                produce_event(self.fsm.event_data, EventID.E_SCAN_FAIL)
        except Exception as e:
            self.get_logger().error(f"Raster scan response exception: {e}")
            produce_event(self.fsm.event_data, EventID.E_SCAN_FAIL)

    def execute_screwdriver_probe(self):
        self.get_logger().info("Screwdriver probe execution is currently disabled.")
        produce_event(self.fsm.event_data, EventID.E_SCREWDRIVER_PROBE_DONE)

    def request_perception(self, task_name, object_class, result_callback):
        if not self.perception_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error("Perception action server not available.")
            result_callback(None)
            return

        goal = Perception.Goal()
        goal.task_name = task_name
        goal.object_class = object_class
        future = self.perception_client.send_goal_async(goal)
        future.add_done_callback(
            lambda fut: self._perception_goal_response(
                fut, task_name, object_class, result_callback
            )
        )

    def _perception_goal_response(self, future, task_name, object_class, result_callback):
        try:
            goal_handle = future.result()
            if goal_handle is None or not goal_handle.accepted:
                self.get_logger().error(
                    "Perception goal rejected for task "
                    f"'{task_name}' object_class='{object_class}'."
                )
                result_callback(None)
                return

            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(
                lambda fut: result_callback(fut.result().result if fut.result() else None)
            )
        except Exception as e:
            self.get_logger().error(
                "Perception goal exception for task "
                f"'{task_name}' object_class='{object_class}': {e}"
            )
            result_callback(None)

    def request_car_objects(self):
        self.user_data["car_objects"] = {}
        self.clear_active_car_object()
        self.user_data["pending_object_classes"] = list(self.car_object_classes)
        self._request_next_car_object_class()

    def _request_next_car_object_class(self):
        if not self.user_data["pending_object_classes"]:
            self.get_logger().info(
                f"Stored car objects in {self.base_frame}: "
                f"{list(self.user_data['car_objects'].keys())}."
            )
            produce_event(self.fsm.event_data, EventID.E_OBJECTS_DONE)
            return

        object_class = self.user_data["pending_object_classes"][0]
        self.request_perception(
            "car_objects",
            object_class,
            lambda result: self._handle_car_object_result(object_class, result),
        )

    def on_subdoor_result(self, result):
        self._store_perception_poses(
            result,
            "subdoor_poses",
            "subdoor",
            EventID.E_SUBDOOR_DONE,
            EventID.E_SUBDOOR_FAIL,
        )

    def _handle_car_object_result(self, object_class, result):
        if not self.store_car_object(object_class, result):
            produce_event(self.fsm.event_data, EventID.E_OBJECTS_FAIL)
            return

        if self.user_data["pending_object_classes"]:
            self.user_data["pending_object_classes"].pop(0)
        self._request_next_car_object_class()

    def store_car_object(self, object_class, result):
        if result is None or not result.success:
            message = "No object pose or resulted in failure" if result is None else result.message
            self.get_logger().error(
                f"Object perception failed for class '{object_class}': {message}"
            )
            return False

        transformed_poses = self.transform_pose_array_to_base(result.poses)
        if transformed_poses is None or len(transformed_poses) < 1:
            self.get_logger().error(
                f"Object perception returned no valid poses for class '{object_class}'."
            )
            return False

        if len(transformed_poses) > 1:
            self.get_logger().warn(
                f"Object perception returned {len(transformed_poses)} poses for class "
                f"'{object_class}'. Using the first one."
            )

        self.user_data["car_objects"][object_class] = {
            "pose": transformed_poses[0],
            "radius": result.estimated_value,
        }
        self.get_logger().info(
            f"Stored {object_class} object pose in {self.base_frame} "
            f"with radius {result.estimated_value}."
        )
        return True

    def _store_perception_poses(self, result, storage_key, label, success_evt, fail_evt):
        if result is None or not result.success:
            message = "no response" if result is None else result.message
            self.get_logger().error(f"{label.capitalize()} perception failed: {message}")
            produce_event(self.fsm.event_data, fail_evt)
            return

        transformed_poses = self.transform_pose_array_to_base(result.poses)
        if transformed_poses is None:
            produce_event(self.fsm.event_data, fail_evt)
            return

        self.user_data[storage_key] = transformed_poses
        self.get_logger().info(
            f"Stored {len(self.user_data[storage_key])} {label} poses in {self.base_frame}."
        )
        produce_event(self.fsm.event_data, success_evt)

    def send_pick_object_sequence(self, pre_pick_pose, pick_offset_pose, success_evt, fail_evt):
        if not self.arm_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error("Arm action server not available during object pre-pick.")
            produce_event(self.fsm.event_data, fail_evt)
            return
        goal = ArmControl.Goal()
        goal.target_pose = pre_pick_pose
        future = self.arm_client.send_goal_async(goal)
        future.add_done_callback(
            lambda fut: self._pick_pre_pose_goal_response(
                fut, pick_offset_pose, success_evt, fail_evt
            )
        )

    def send_gripper_command(self, position, success_evt, fail_evt, context):
        if not self.gripper_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error(f"Gripper action server not available during {context}.")
            produce_event(self.fsm.event_data, fail_evt)
            return

        goal = GripperControl.Goal()
        goal.target_position = position
        goal.velocity = 20.0
        goal.force = 10.0

        future = self.gripper_client.send_goal_async(goal)
        future.add_done_callback(
            lambda fut: self._gripper_goal_response(fut, success_evt, fail_evt, context)
        )

    def _send_direct_arm_goal(self, pose, success_evt, fail_evt, context):
        if not self.arm_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error(f"Arm action server not available during {context}.")
            produce_event(self.fsm.event_data, fail_evt)
            return
        goal = ArmControl.Goal()
        goal.target_pose = pose
        future = self.arm_client.send_goal_async(goal)
        future.add_done_callback(
            lambda fut: self._arm_goal_response(fut, success_evt, fail_evt, context)
        )

    def _arm_goal_response(self, future, success_evt, fail_evt, context):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().error(f"Arm goal rejected during {context}.")
                produce_event(self.fsm.event_data, fail_evt)
                return
            res_future = goal_handle.get_result_async()
            res_future.add_done_callback(
                lambda fut: self._arm_result(fut, success_evt, fail_evt, context)
            )
        except Exception as e:
            self.get_logger().error(f"Arm goal exception during {context}: {e}")
            produce_event(self.fsm.event_data, fail_evt)

    def _arm_result(self, future, success_evt, fail_evt, context):
        try:
            result = future.result().result
            if result.result_code == ArmControl.Result.SUCCESS:
                self.get_logger().info(f"Arm action succeeded during {context}.")
                produce_event(self.fsm.event_data, success_evt)
            else:
                msg = (
                    result.result_message
                    if hasattr(result, "result_message")
                    else result.message
                )
                self.get_logger().error(f"Arm action failed during {context}: {msg}")
                produce_event(self.fsm.event_data, fail_evt)
        except Exception as e:
            self.get_logger().error(f"Arm result exception during {context}: {e}")
            produce_event(self.fsm.event_data, fail_evt)

    def _pick_pre_pose_goal_response(self, future, pick_offset_pose, success_evt, fail_evt):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().error("Arm goal rejected during object pre-pick.")
                produce_event(self.fsm.event_data, fail_evt)
                return
            res_future = goal_handle.get_result_async()
            res_future.add_done_callback(
                lambda fut: self._pick_pre_pose_result(
                    fut, pick_offset_pose, success_evt, fail_evt
                )
            )
        except Exception as e:
            self.get_logger().error(f"Arm goal exception during object pre-pick: {e}")
            produce_event(self.fsm.event_data, fail_evt)

    def _pick_pre_pose_result(self, future, pick_offset_pose, success_evt, fail_evt):
        try:
            result = future.result().result
            if result.result_code == ArmControl.Result.SUCCESS:
                self.get_logger().info("Arm action succeeded during object pre-pick.")
                self._send_direct_arm_goal(
                    pick_offset_pose,
                    success_evt,
                    fail_evt,
                    "advance to object pick pose",
                )
            else:
                msg = (
                    result.result_message
                    if hasattr(result, "result_message")
                    else result.message
                )
                self.get_logger().error(f"Arm action failed during object pre-pick: {msg}")
                produce_event(self.fsm.event_data, fail_evt)
        except Exception as e:
            self.get_logger().error(f"Arm result exception during object pre-pick: {e}")
            produce_event(self.fsm.event_data, fail_evt)

    def _gripper_goal_response(self, future, success_evt, fail_evt, context):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().error(f"Gripper goal rejected during {context}.")
                produce_event(self.fsm.event_data, fail_evt)
                return
            res_future = goal_handle.get_result_async()
            res_future.add_done_callback(
                lambda fut: self._gripper_result(fut, success_evt, fail_evt, context)
            )
        except Exception as e:
            self.get_logger().error(f"Gripper goal exception during {context}: {e}")
            produce_event(self.fsm.event_data, fail_evt)

    def _gripper_result(self, future, success_evt, fail_evt, context):
        try:
            result = future.result().result
            if result.result_code == GripperControl.Result.SUCCESS:
                self.get_logger().info(f"Gripper action succeeded during {context}.")
                if success_evt == EventID.E_GRIPPER_OPEN_DONE and self.user_data["active_object_class"]:
                    self.user_data["car_objects"].pop(self.user_data["active_object_class"], None)
                    self.get_logger().info(
                        "Dropped object and removed it from pending list."
                    )
                    self.clear_active_car_object()
                produce_event(self.fsm.event_data, success_evt)
            else:
                msg = (
                    result.result_message
                    if hasattr(result, "result_message")
                    else result.message
                )
                self.get_logger().error(f"Gripper action failed during {context}: {msg}")
                produce_event(self.fsm.event_data, fail_evt)
        except Exception as e:
            self.get_logger().error(f"Gripper result exception during {context}: {e}")
            produce_event(self.fsm.event_data, fail_evt)

def main(args=None):
    rclpy.init(args=args)
    node = DoorDisassembleNode()
    try:
        rclpy.spin(node)
    except SystemExit:
        node.get_logger().info("Node stopped via SystemExit")
    except KeyboardInterrupt:
        node.get_logger().info("Node stopped via KeyboardInterrupt")
    finally:
        node.destroy_node()
        try:
            if rclpy.ok():
                rclpy.shutdown()
        except Exception:
            pass


if __name__ == "__main__":
    main()

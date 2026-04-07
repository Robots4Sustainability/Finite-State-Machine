#!/usr/bin/env python3
import json
import math
import threading
import time
from pathlib import Path

import rclpy
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.duration import Duration
from rclpy.node import Node

from geometry_msgs.msg import Pose, PoseStamped
from std_msgs.msg import Bool
from tf2_ros import Buffer, TransformListener
from eddie_ros.action import ArmControl, ForceControl
from cartesian_planner.srv import PlanScanPath
from my_robot_interfaces.action import RunVision
from pick_place_fsm.srv import RunScrewdriverRoutine
from coord_dsl.fsm import fsm_step
from coord_dsl.event_loop import reconfig_event_buffers, produce_event
from common import FlowLogger, NamedPoseStore, PoseUtils, RobotActionHelper, PerceptionHelper, gripper_action_name, gripper_action_type
from fsm_door_disassemble import create_fsm, StateID, EventID


class DoorDisassembleNode(Node):
    def __init__(self):
        super().__init__("door_disassemble_fsm_py")

        self.fsm = create_fsm()

        self.declare_parameter("base_frame", "eddie_base_link")
        self.declare_parameter("ee_frame", "eddie_right_arm_robotiq_85_grasp_link")
        self.declare_parameter("camera_frame", "eddie_right_arm_camera_link")
        self.declare_parameter("perception_action_server", "run_perception_pipeline")
        self.declare_parameter("car_object_classes", ["unit", "speaker", "motor_grip"])
        self.declare_parameter("enable_raster_scan", False)
        self.declare_parameter("screwdriver_probe", True)
        self.declare_parameter("pose_store_path", str("/home/r4s/r4s-ws/src/Finite-State-Machine/src/named_poses.json"))        
        
        self.base_frame = self.get_parameter("base_frame").value
        self.ee_frame = self.get_parameter("ee_frame").value
        self.camera_frame = self.get_parameter("camera_frame").value
        self.perception_action_server = self.get_parameter("perception_action_server").value
        self.car_object_classes = list(self.get_parameter("car_object_classes").value)
        self.enable_raster_scan = bool(self.get_parameter("enable_raster_scan").value)
        self.enable_screwdriver_probe = bool(self.get_parameter("screwdriver_probe").value)
        self.pose_store_path = Path(self.get_parameter("pose_store_path").value).expanduser()
        self.object_pick_z_offset = 0.1
        self.named_pose_store = NamedPoseStore(self, self.base_frame, self.pose_store_path)
        self.screwdriver_probe_pending = False

        self.user_data = {
            "last_state": StateID.S_IDLE,
            "action_dispatched": False,
            "view_pose_global": self.get_default_view_pose_global(),
            "table_drop_pose_global": self.get_default_table_drop_pose_global(),
            "active_place_pose_global": None,
            "subdoor_poses": [],
            "car_objects": {},
            "active_object_detection": None,
            "active_object_radius": 0.0,
            "active_object_class": "",
            "scan_message": "",
            "scan_screw_poses": [],
            "arm_motion_mode": "",
            "view_pose_phase": "",
            "pre_place_phase": "",
            "pick_motion_phase": "",
            "pending_object_classes": [],
        }

        self.cb_group = ReentrantCallbackGroup()
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.pose_utils = PoseUtils(self, self.tf_buffer, self.base_frame, self.ee_frame)

        self.arm_client = ActionClient(self, ArmControl, "right_arm/arm_control", callback_group=self.cb_group)
        self.force_client = ActionClient(self, ForceControl, "right_arm/force_control", callback_group=self.cb_group)
        self.gripper_client = ActionClient(self, gripper_action_type(), gripper_action_name(), callback_group=self.cb_group)
        self.perception_client = ActionClient(self, RunVision, self.perception_action_server, callback_group=self.cb_group)
        self.robot_actions = RobotActionHelper(self, self.arm_client, self.gripper_client, self.force_client)
        self.perception_helper = PerceptionHelper(self, self.perception_client, self.pose_utils, self.base_frame)
        self.flow_logger = FlowLogger(self)
        self.scan_client = self.create_client(PlanScanPath, "plan_scan_path", callback_group=self.cb_group)
        self.screwdriver_client = self.create_client(
            RunScrewdriverRoutine, "/screwdriver_pick/run", callback_group=self.cb_group
        )
        self.create_subscription(Bool, "/door_disassemble/abort", self.abort_callback, 10, callback_group=self.cb_group)
        self.create_subscription(Bool, "/screwdriver_pick/done", self.screwdriver_done_callback, 10, callback_group=self.cb_group)
        self.safety_sub = None

        self.fsm_timer = self.create_timer(0.1, self.fsm_loop, callback_group=self.cb_group)

        self.input_thread = threading.Thread(target=self.input_loop, daemon=True)
        self.input_thread.start()

        self.get_logger().info("Door disassemble node ready.")
        self.get_logger().info("Press Enter to start. Type 'a' + Enter to abort.")

    def get_named_pose(self, key: str) -> Pose | None:
        return self.named_pose_store.get_named_pose(key)

    def get_default_view_pose_global(self) -> Pose:
        named_pose = self.get_named_pose("home_pose")
        if named_pose is not None:
            self.get_logger().info("Using home_pose from named poses for home/view pose.")
            return named_pose

        p = Pose()
        p.position.x = 0.729990
        p.position.y = -0.285972
        p.position.z = 0.575513
        p.orientation.x = 0.461884
        p.orientation.y = 0.469245
        p.orientation.z = 0.549966
        p.orientation.w = 0.513819
        return p

    def get_default_table_drop_pose_global(self) -> Pose:
        named_pose = self.get_named_pose("table_drop_pose")
        if named_pose is not None:
            self.get_logger().info("Using table_drop_pose from named poses.")
            return named_pose

        p = Pose()
        p.position.x = 0.60
        p.position.y = -0.66
        p.position.z = 0.343951
        p.orientation.x = 0.475857
        p.orientation.y = 0.493639
        p.orientation.z = 0.546011
        p.orientation.w = 0.481407
        return p

    def get_view_pose_for_object_class(self, object_class: str) -> Pose:
        named_pose = self.get_named_pose(f"view_pose_{object_class}")
        if named_pose is not None:
            self.get_logger().info(f"Using view_pose_{object_class} from named poses for perception.")
            return named_pose
        return self.user_data["view_pose_global"]

    def get_place_target_pose_global(self) -> Pose | None:
        active_place_pose = self.user_data["active_place_pose_global"]
        if active_place_pose is None:
            return None

        target = Pose()
        target.position.x = active_place_pose.position.x
        target.position.y = active_place_pose.position.y
        target.position.z = active_place_pose.position.z

        # Keep the wrist orientation fixed during placement. The place pose from
        # perception only provides where to put the object, not a new EE attitude.
        target.orientation = self.user_data["table_drop_pose_global"].orientation
        return target

    def abort_callback(self, msg: Bool):
        if msg.data:
            self.get_logger().warn("Abort message received.")
            produce_event(self.fsm.event_data, EventID.E_ABORT)

    def safety_status_callback(self, msg: Bool):
        if not msg.data:
            self.get_logger().fatal("COLLISION DETECTED! Aborting FSM immediately.")
            produce_event(self.fsm.event_data, EventID.E_ABORT)

    def screwdriver_done_callback(self, msg: Bool):
        if not self.screwdriver_probe_pending:
            return
        self.screwdriver_probe_pending = False
        if not msg.data:
            self.get_logger().error("Screwdriver routine reported failure. Continuing anyway.")
        else:
            self.get_logger().info("Screwdriver routine completed.")
        produce_event(self.fsm.event_data, EventID.E_SCREWDRIVER_PROBE_DONE)

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
            phase = ""
            for value in (
                self.user_data["pick_motion_phase"],
                self.user_data["pre_place_phase"],
                self.user_data["view_pose_phase"],
                self.user_data["arm_motion_mode"],
            ):
                if value:
                    phase = value
                    break
            self.flow_logger.state_banner(state_name, self.user_data["active_object_class"], phase)
            self.user_data["last_state"] = self.fsm.current_state_index
            self.user_data["action_dispatched"] = False

        self.fsm_behavior()
        fsm_step(self.fsm)
        reconfig_event_buffers(self.fsm.event_data)

    def fsm_behavior(self):
        cs = self.fsm.current_state_index
        if cs == StateID.S_IDLE or self.user_data["action_dispatched"]:
            return

        state_handlers = {
            StateID.S_INITIALIZE: self.handle_initialize,
            StateID.S_MOVE_TO_VIEW_POSE: self.handle_move_to_view_pose,
            StateID.S_GET_SUBDOOR: self.handle_get_subdoor,
            StateID.S_GET_OBJECTS: self.handle_get_objects,
            StateID.S_RASTER_SCAN: self.handle_raster_scan,
            StateID.S_MOVE_ARM: self.handle_move_arm,
            StateID.S_EXECUTE_SCREWDRIVER_PROBE: self.handle_execute_screwdriver_probe,
            StateID.S_SELECT_NEXT_OBJECT: self.handle_select_next_object,
            StateID.S_MOVE_TO_PRE_PLACE_POSE: self.handle_move_to_pre_place_pose,
            StateID.S_TABLE_PERCEIVE: self.handle_table_perceive,
            StateID.S_MOVE_TO_PICK_OBJECT: self.handle_move_to_pick_object,
            StateID.S_CLOSE_GRIPPER: self.handle_close_gripper,
            StateID.S_MOVE_TO_PLACE_POSE: self.handle_move_to_place_pose,
            StateID.S_OPEN_GRIPPER: self.handle_open_gripper,
            StateID.S_CONFIRM_DATA: self.handle_confirm_data,
        }
        handler = state_handlers.get(cs)
        if handler is not None:
            handler()

    def handle_initialize(self):
        self.get_logger().info("Initializing...")
        self.user_data["view_pose_phase"] = "INITIAL"
        if self.check_system_readiness():
            self.get_logger().info("Initialization checks passed.")
            produce_event(self.fsm.event_data, EventID.E_INIT_DONE)
        else:
            self.get_logger().error("Initialization checks failed.")
            produce_event(self.fsm.event_data, EventID.E_ABORT)
        self.user_data["action_dispatched"] = True

    def handle_move_to_view_pose(self):
        self.get_logger().info("Moving arm to global view pose...")
        self.user_data["arm_motion_mode"] = "VIEW_POSE"
        produce_event(self.fsm.event_data, EventID.E_GO_MOVE_ARM)
        self.user_data["action_dispatched"] = True

    def handle_get_subdoor(self):
        ud = self.user_data
        if ud["view_pose_phase"] == "AFTER_SCAN":
            self.get_logger().info(
                "Post-scan view pose reached. Skipping subdoor request and "
                "continuing to screwdriver probe stage."
            )
            ud["view_pose_phase"] = ""
            ud["action_dispatched"] = False
            self.fsm.current_state_index = StateID.S_EXECUTE_SCREWDRIVER_PROBE
            return
        if ud["view_pose_phase"] == "BEFORE_PICK":
            self.get_logger().info(
                "View pose reached before pick. Skipping subdoor request and "
                "continuing to object pick motion."
            )
            ud["view_pose_phase"] = ""
            ud["action_dispatched"] = False
            self.fsm.current_state_index = StateID.S_MOVE_TO_PICK_OBJECT
            return
        if not self.enable_raster_scan:
            self.get_logger().info("Raster scan disabled. Skipping subdoor pose request.")
            produce_event(self.fsm.event_data, EventID.E_SUBDOOR_DONE)
            ud["action_dispatched"] = True
            return
        self.get_logger().info("Requesting subdoor poses from perception action...")
        self.request_perception("subdoor_pose", "", self.on_subdoor_result)
        ud["action_dispatched"] = True

    def handle_get_objects(self):
        self.get_logger().info(f"Requesting car object poses from perception action for classes {self.car_object_classes}...")
        self.request_car_objects()
        self.user_data["action_dispatched"] = True

    def handle_raster_scan(self):
        ud = self.user_data
        if not self.enable_raster_scan:
            self.get_logger().info("Raster scan disabled. Skipping planner call.")
            self.fsm.current_state_index = StateID.S_EXECUTE_SCREWDRIVER_PROBE
            ud["action_dispatched"] = False
            return

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
        future = self.scan_client.call_async(req)
        future.add_done_callback(self.on_scan_response)
        ud["action_dispatched"] = True

    def handle_move_arm(self):
        ud = self.user_data
        target = None
        success_evt = None
        fail_evt = None
        context = "arm motion"

        if ud["arm_motion_mode"] == "VIEW_POSE":
            target = self.global_pose_to_relative_pose(ud["view_pose_global"], self.base_frame, self.ee_frame)
            success_evt = EventID.E_VIEW_POSE_DONE
            fail_evt = EventID.E_VIEW_POSE_FAIL
            context = "move to global view pose"
        elif ud["arm_motion_mode"] == "MOVE_TO_PRE_PLACE":
            target = self.global_pose_to_relative_pose(ud["table_drop_pose_global"], self.base_frame, self.ee_frame)
            if ud["pre_place_phase"] == "TABLE_PERCEIVE":
                success_evt = EventID.E_PRE_PLACE_DONE
                fail_evt = EventID.E_ARM_MOVE_FAIL
                context = "move to pre-place pose for table perception"
            elif ud["pre_place_phase"] == "BEFORE_PICK":
                fail_evt = EventID.E_ARM_MOVE_FAIL
                context = "return to pre-place pose before pick"
                self.get_logger().info(f"Executing arm motion: {context}")
                self._send_direct_arm_goal(target, None, fail_evt, context, result_callback=self._pre_place_before_pick_result)
                ud["action_dispatched"] = True
                return
            elif ud["pre_place_phase"] == "WITH_OBJECT":
                success_evt = EventID.E_PRE_PLACE_WITH_OBJECT_DONE
                fail_evt = EventID.E_ARM_MOVE_FAIL
                context = "return to pre-place pose with object"
            elif ud["pre_place_phase"] == "AFTER_DROP":
                success_evt = EventID.E_PRE_PLACE_AFTER_DROP_DONE
                fail_evt = EventID.E_PRE_PLACE_AFTER_DROP_FAIL
                context = "return to pre-place pose after drop"
        elif ud["arm_motion_mode"] == "PICK_OBJECT":
            target = self.object_pose_to_relative_pose(ud["active_object_detection"], z_offset=self.object_pick_z_offset)
            success_evt = EventID.E_PICK_OBJECT_DONE
            fail_evt = EventID.E_ARM_MOVE_FAIL
            context = "move to object pre-pick pose"
            if target is None:
                self.get_logger().error("Failed to resolve target during object pre-pick.")
                produce_event(self.fsm.event_data, fail_evt)
            else:
                self.get_logger().info("Executing arm motion: move to object pre-pick pose")
                self.send_pick_object_sequence(target, self.make_relative_offset_pose(dz=self.object_pick_z_offset), success_evt, fail_evt)
            ud["action_dispatched"] = True
            return
        elif ud["arm_motion_mode"] == "PICK_OBJECT_RETREAT":
            target = self.make_relative_offset_pose(dz=-self.object_pick_z_offset)
            success_evt = EventID.E_PICK_OBJECT_RETREAT_DONE
            fail_evt = EventID.E_ARM_MOVE_FAIL
            context = "retreat with grasped object"
        elif ud["arm_motion_mode"] == "MOVE_TO_PLACE":
            if ud["active_place_pose_global"] is None:
                self.get_logger().error("No active place pose available.")
                produce_event(self.fsm.event_data, EventID.E_ARM_MOVE_FAIL)
                ud["action_dispatched"] = True
                return
            place_target = self.get_place_target_pose_global()
            if place_target is None:
                self.get_logger().error("Failed to build place target pose.")
                produce_event(self.fsm.event_data, EventID.E_ARM_MOVE_FAIL)
                ud["action_dispatched"] = True
                return
            target = self.global_pose_to_relative_pose(place_target, self.base_frame, self.ee_frame)
            success_evt = EventID.E_MOVE_TO_PLACE_DONE
            fail_evt = EventID.E_ARM_MOVE_FAIL
            context = "move to place pose"

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

    def handle_execute_screwdriver_probe(self):
        self.execute_screwdriver_probe()
        self.user_data["action_dispatched"] = True

    def handle_select_next_object(self):
        ud = self.user_data
        if not self.select_next_car_object():
            self.get_logger().info("No more objects left to pick.")
            produce_event(self.fsm.event_data, EventID.E_NO_MORE_OBJECTS)
        else:
            self.get_logger().info(f"Selected next object pose from perception results class='{ud['active_object_class']}' with radius {ud['active_object_radius']}.")
            ud["pre_place_phase"] = "TABLE_PERCEIVE"
            ud["active_place_pose_global"] = None
            produce_event(self.fsm.event_data, EventID.E_OBJECT_READY)
        ud["action_dispatched"] = True

    def handle_move_to_pre_place_pose(self):
        self.get_logger().info(f"Moving to pre-place pose. phase={self.user_data['pre_place_phase']}")
        self.user_data["arm_motion_mode"] = "MOVE_TO_PRE_PLACE"
        produce_event(self.fsm.event_data, EventID.E_GO_MOVE_ARM)
        self.user_data["action_dispatched"] = True

    def handle_table_perceive(self):
        ud = self.user_data
        self.get_logger().info(f"Tilting end-effector 45 degrees downward for table perceive, then requesting place pose for class='{ud['active_object_class']}' with radius {ud['active_object_radius']}.")
        self.send_table_perceive_tilt()
        ud["action_dispatched"] = True

    def handle_move_to_pick_object(self):
        ud = self.user_data
        if ud["pick_motion_phase"] == "RETREAT":
            self.get_logger().info("Retreating 10 cm with grasped object...")
            ud["arm_motion_mode"] = "PICK_OBJECT_RETREAT"
        else:
            self.get_logger().info("Executing pick approach: pre-pick then advance 10 cm.")
            ud["pick_motion_phase"] = "APPROACH"
            ud["arm_motion_mode"] = "PICK_OBJECT"
        produce_event(self.fsm.event_data, EventID.E_GO_MOVE_ARM)
        ud["action_dispatched"] = True

    def handle_close_gripper(self):
        ud = self.user_data
        ud["pick_motion_phase"] = "RETREAT"
        ud["pre_place_phase"] = "WITH_OBJECT"
        position = 0.0
        current_object_to_grasp = ud["active_object_class"]
        if current_object_to_grasp == "unit":
            position = 0.08
        elif current_object_to_grasp == "motor_grip":
            position = 0.45
        elif current_object_to_grasp == "speaker":
            position = 0.47
        self.send_gripper_command(position, EventID.E_GRIPPER_CLOSE_DONE, EventID.E_GRIPPER_FAIL, "close gripper on object")
        ud["action_dispatched"] = True

    def handle_move_to_place_pose(self):
        self.get_logger().info("Moving to place pose...")
        self.user_data["arm_motion_mode"] = "MOVE_TO_PLACE"
        produce_event(self.fsm.event_data, EventID.E_GO_MOVE_ARM)
        self.user_data["action_dispatched"] = True

    def handle_open_gripper(self):
        self.user_data["pre_place_phase"] = "AFTER_DROP"
        self.send_gripper_command(0.0, EventID.E_GRIPPER_OPEN_DONE, EventID.E_GRIPPER_FAIL, "open gripper to drop object")
        self.user_data["action_dispatched"] = True

    def handle_confirm_data(self):
        ud = self.user_data
        self.get_logger().info("Confirm step reached. Stored data summary:")
        self.get_logger().info(f"Subdoor poses: {len(ud['subdoor_poses'])}")
        self.get_logger().info(f"Car objects: {list(ud['car_objects'].keys())}")
        self.get_logger().info(f"Raster scan message: {ud['scan_message']}")
        self.get_logger().info(f"Raster screws: {len(ud['scan_screw_poses'])}")
        produce_event(self.fsm.event_data, EventID.E_CONFIRM_DONE)
        ud["action_dispatched"] = True

    def global_pose_to_relative_pose(self, global_pose: Pose, global_frame: str, target_frame: str) -> Pose | None:
        return self.pose_utils.global_pose_to_relative_pose(global_pose, global_frame, target_frame)

    def object_pose_to_relative_pose(self, detection, z_offset=0.0) -> Pose | None:
        return self.pose_utils.object_pose_to_relative_pose(detection, z_offset=z_offset)

    def get_next_available_object_class(self) -> str | None:
        for object_class in self.car_object_classes:
            if object_class in self.user_data["car_objects"]:
                return object_class
        return None

    def check_system_readiness(self) -> bool:
        checks_ok = True

        checks_ok &= self._check_action_server(self.arm_client, "right_arm/arm_control")
        checks_ok &= self._check_action_server(self.gripper_client, gripper_action_name())
        checks_ok &= self._check_action_server(self.perception_client, self.perception_action_server)

        if self.enable_raster_scan:
            checks_ok &= self._check_service(self.scan_client, "plan_scan_path")
        else:
            self.get_logger().info("Skipping plan_scan_path readiness check because raster scan is disabled.")
        if self.enable_screwdriver_probe:
            checks_ok &= self._check_service(self.screwdriver_client, "/screwdriver_pick/run")

        publishers = self.get_publishers_info_by_topic("/robot_safety/status")
        if len(publishers) > 0:
            self.get_logger().info("Eddie Safety node detected. Enabling collision detetction")
            if self.safety_sub is None:
                self.safety_sub = self.create_subscription(
                    Bool, 
                    "/robot_safety/status", 
                    self.safety_status_callback, 
                    10, 
                    callback_group=self.cb_group
                )
        else:
            self.get_logger().warn("Eddie Safety node NOT detected. Running WITHOUT collision monitoring.")

        required_frames = [self.base_frame, self.ee_frame, self.camera_frame]
        for frame in required_frames:
            if not frame:
                self.get_logger().error("A required frame parameter is empty.")
                checks_ok = False

        checks_ok &= self._check_transform(self.base_frame, self.ee_frame)
        checks_ok &= self._check_transform(self.base_frame, self.camera_frame)
        return checks_ok

    def _check_action_server(self, client, name: str) -> bool:
        if client.wait_for_server(timeout_sec=2.0):
            self.get_logger().info(f"Action server ready: {name}")
            return True
        self.get_logger().error(f"Action server not available: {name}")
        return False

    def _check_service(self, client, name: str) -> bool:
        if client.wait_for_service(timeout_sec=2.0):
            self.get_logger().info(f"Service ready: {name}")
            return True
        self.get_logger().error(f"Service not available: {name}")
        return False

    def _check_transform(self, target_frame: str, source_frame: str) -> bool:
        try:
            if self.tf_buffer.can_transform(target_frame, source_frame, rclpy.time.Time(), timeout=Duration(seconds=2.0)):
                self.get_logger().info(f"Transform ready: {target_frame} <- {source_frame}")
                return True
        except Exception as e:
            self.get_logger().error(f"Transform check failed for {target_frame} <- {source_frame}: {e}")
            return False

        self.get_logger().error(f"Transform not available: {target_frame} <- {source_frame}")
        return False

    def select_next_car_object(self) -> bool:
        object_class = self.get_next_available_object_class()
        if object_class is None:
            return False

        active_object = self.user_data["car_objects"][object_class]
        self.user_data["active_object_class"] = object_class
        self.user_data["active_object_detection"] = active_object["pose"]
        self.user_data["active_object_radius"] = active_object["radius"]
        self.user_data["pick_motion_phase"] = ""
        return True

    def clear_active_car_object(self):
        self.user_data["active_object_detection"] = None
        self.user_data["active_object_radius"] = 0.0
        self.user_data["active_object_class"] = ""
        self.user_data["active_place_pose_global"] = None
        self.user_data["pick_motion_phase"] = ""

    def make_relative_offset_pose(self, dx=0.0, dy=0.0, dz=0.0) -> Pose:
        return self.pose_utils.make_relative_offset_pose(dx=dx, dy=dy, dz=dz)

    def make_relative_orientation_pose(self, qx=0.0, qy=0.0, qz=0.0, qw=1.0) -> Pose:
        return self.pose_utils.make_relative_orientation_pose(qx=qx, qy=qy, qz=qz, qw=qw)

    def make_table_perceive_tilt_pose(self) -> Pose:
        half_angle = math.radians(45.0) / 2.0
        # Tilt the tool downward in place around the local X axis.
        return self.make_relative_orientation_pose(
            qx=math.sin(half_angle),
            qw=math.cos(half_angle),
        )

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
                self.fsm.current_state_index = StateID.S_EXECUTE_SCREWDRIVER_PROBE
                self.user_data["action_dispatched"] = False
            else:
                self.get_logger().error(f"Raster scan failed: {resp.message}")
                produce_event(self.fsm.event_data, EventID.E_SCAN_FAIL)
        except Exception as e:
            self.get_logger().error(f"Raster scan response exception: {e}")
            produce_event(self.fsm.event_data, EventID.E_SCAN_FAIL)

    def execute_screwdriver_probe(self):
        if not self.enable_screwdriver_probe:
            self.get_logger().info("Screwdriver probe disabled. Skipping routine.")
            produce_event(self.fsm.event_data, EventID.E_SCREWDRIVER_PROBE_DONE)
            return

        if not self.screwdriver_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().error("Screwdriver routine service not available.")
            produce_event(self.fsm.event_data, EventID.E_SCREWDRIVER_PROBE_FAIL)
            return

        request = RunScrewdriverRoutine.Request()
        request.request_json = json.dumps({"screw_poses": self.user_data["scan_screw_poses"]})
        self.screwdriver_probe_pending = True
        future = self.screwdriver_client.call_async(request)
        future.add_done_callback(self._screwdriver_run_response)
        self.get_logger().info(f"Triggered screwdriver routine with {len(self.user_data['scan_screw_poses'])} screw poses.")

    def _screwdriver_run_response(self, future):
        try:
            response = future.result()
            if response is None or not response.accepted:
                self.screwdriver_probe_pending = False
                message = "no response" if response is None else response.message
                self.get_logger().error(f"Screwdriver routine request rejected: {message}")
                produce_event(self.fsm.event_data, EventID.E_SCREWDRIVER_PROBE_FAIL)
        except Exception as exc:
            self.screwdriver_probe_pending = False
            self.get_logger().error(f"Screwdriver routine service call failed: {exc}")
            produce_event(self.fsm.event_data, EventID.E_SCREWDRIVER_PROBE_FAIL)

    def request_perception(self, task_name, object_class, result_callback, time_duration=0.0):
        self.perception_helper.send_request(task_name, object_class, result_callback, time_duration=time_duration)

    def request_car_objects(self):
        self.user_data["car_objects"] = {}
        self.clear_active_car_object()
        self.user_data["pending_object_classes"] = list(self.car_object_classes)
        self._request_next_car_object_class()

    def request_place_pose(self):
        # Temporary transport for object radius until the perception action gets
        # a dedicated goal field for placement radius.
        self.request_perception("place_object", self.user_data["active_object_class"], self.on_place_pose_result, time_duration=self.user_data["active_object_radius"])

    def send_table_perceive_tilt(self):
        self._send_direct_arm_goal(self.make_table_perceive_tilt_pose(), None, None, "tilt end-effector down for table perceive", result_callback=self._table_perceive_tilt_result)

    def _request_next_car_object_class(self):
        if not self.user_data["pending_object_classes"]:
            self.get_logger().info(f"Stored car objects in {self.base_frame}: {list(self.user_data['car_objects'].keys())}.")
            produce_event(self.fsm.event_data, EventID.E_OBJECTS_DONE)
            return

        object_class = self.user_data["pending_object_classes"][0]
        view_pose = self.get_view_pose_for_object_class(object_class)
        target = self.global_pose_to_relative_pose(view_pose, self.base_frame, self.ee_frame)
        if target is None:
            self.get_logger().error(f"Failed to resolve view pose for object class '{object_class}'.")
            produce_event(self.fsm.event_data, EventID.E_OBJECTS_FAIL)
            return

        self.get_logger().info(f"Moving to view pose before requesting perception for class '{object_class}'.")
        self._send_object_view_pose_goal(target, object_class)

    def _send_object_view_pose_goal(self, pose, object_class):
        if not self.arm_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error(
                f"Arm action server not available for object view pose '{object_class}'."
            )
            produce_event(self.fsm.event_data, EventID.E_OBJECTS_FAIL)
            return

        goal = ArmControl.Goal()
        goal.target_pose = pose
        future = self.arm_client.send_goal_async(goal)
        future.add_done_callback(lambda fut: self._object_view_pose_goal_response(fut, object_class))

    def _object_view_pose_goal_response(self, future, object_class):
        try:
            goal_handle = future.result()
            if goal_handle is None or not goal_handle.accepted:
                self.get_logger().error(f"Arm goal rejected during object view move for '{object_class}'.")
                produce_event(self.fsm.event_data, EventID.E_OBJECTS_FAIL)
                return

            goal_handle.get_result_async().add_done_callback(lambda fut: self._object_view_pose_result(fut, object_class))
        except Exception as e:
            self.get_logger().error(f"Arm goal exception during object view move for '{object_class}': {e}")
            produce_event(self.fsm.event_data, EventID.E_OBJECTS_FAIL)

    def _object_view_pose_result(self, future, object_class):
        try:
            result = future.result().result
            if result.result_code != ArmControl.Result.SUCCESS:
                msg = (
                    result.result_message
                    if hasattr(result, "result_message")
                    else result.message
                )
                self.get_logger().error(f"Arm action failed during object view move for '{object_class}': {msg}")
                produce_event(self.fsm.event_data, EventID.E_OBJECTS_FAIL)
                return

            self.get_logger().info(f"Object view pose reached. Requesting perception for class '{object_class}'.")
            self.request_perception("car_objects", object_class, lambda result: self._handle_car_object_result(object_class, result))
        except Exception as e:
            self.get_logger().error(f"Arm result exception during object view move for '{object_class}': {e}")
            produce_event(self.fsm.event_data, EventID.E_OBJECTS_FAIL)

    def on_subdoor_result(self, result):
        transformed_poses = self.perception_helper.extract_transformed_poses(result, "subdoor", min_count=1)
        if transformed_poses is None:
            produce_event(self.fsm.event_data, EventID.E_SUBDOOR_FAIL)
            return

        self.user_data["subdoor_poses"] = transformed_poses
        self.get_logger().info(f"Stored {len(self.user_data['subdoor_poses'])} subdoor poses in {self.base_frame}.")
        produce_event(self.fsm.event_data, EventID.E_SUBDOOR_DONE)

    def on_place_pose_result(self, result):
        transformed_poses = self.perception_helper.extract_transformed_poses(result, "place pose", min_count=1)
        if transformed_poses is None:
            produce_event(self.fsm.event_data, EventID.E_TABLE_PERCEIVE_FAIL)
            return

        self.user_data["active_place_pose_global"] = transformed_poses[0].pose
        self.user_data["pre_place_phase"] = "BEFORE_PICK"
        self.get_logger().info(f"Stored place pose in {self.base_frame} for class='{self.user_data['active_object_class']}'.")
        produce_event(self.fsm.event_data, EventID.E_TABLE_PERCEIVE_DONE)

    def _handle_car_object_result(self, object_class, result):
        if not self.store_car_object(object_class, result):
            produce_event(self.fsm.event_data, EventID.E_OBJECTS_FAIL)
            return

        if self.user_data["pending_object_classes"]:
            self.user_data["pending_object_classes"].pop(0)
        self._request_next_car_object_class()

    def store_car_object(self, object_class, result):
        return self.perception_helper.store_car_object(object_class, result, self.user_data["car_objects"])

    def send_pick_object_sequence(self, pre_pick_pose, pick_offset_pose, success_evt, fail_evt):
        self.flow_logger.action("Move to pre-pick pose")
        ok = self.robot_actions.send_arm_goal(pre_pick_pose, "object pre-pick", lambda fut: self._handle_action_goal_response(
            fut, "object pre-pick", fail_evt, "Arm goal",
            lambda res_fut: self._handle_action_result(
                res_fut, "object pre-pick", fail_evt, "Arm action",
                lambda result: result.result_code == ArmControl.Result.SUCCESS,
                lambda result: result.result_message if hasattr(result, "result_message") else result.message,
                result_callback=lambda result: self._pick_pre_pose_result(result, pick_offset_pose, success_evt, fail_evt),
            ),
        ))
        if not ok:
            self.get_logger().error("Arm action server not available during object pre-pick.")
            produce_event(self.fsm.event_data, fail_evt)
            return

    def send_gripper_command(self, position, success_evt, fail_evt, context):
        self.flow_logger.action(context.capitalize())
        ok = self.robot_actions.send_gripper_goal(position, context, lambda fut: self._handle_action_goal_response(
            fut, context, fail_evt, "Gripper goal",
            lambda res_fut: self._handle_action_result(
                res_fut, context, fail_evt, "Gripper action",
                self.robot_actions.gripper_result_succeeded,
                self.robot_actions.gripper_failure_message,
                result_callback=lambda result: self._on_gripper_success(result, success_evt),
            ),
        ))
        if not ok:
            self.get_logger().error(f"Gripper action server not available during {context}.")
            produce_event(self.fsm.event_data, fail_evt)
            return

    def send_unit_pull_wrench(self, success_evt, fail_evt):
        self.flow_logger.action("Unit pull wrench")
        ok = self.robot_actions.send_force_goal("unit pull", lambda fut: self._handle_action_goal_response(
            fut, "unit pull", fail_evt, "Force control goal",
            lambda res_fut: self._handle_action_result(
                res_fut, "unit pull", fail_evt, "Force control",
                lambda result: result.result_code == ForceControl.Result.SUCCESS,
                lambda result: result.result_message if hasattr(result, "result_message") else "unknown force-control failure",
                success_evt=success_evt,
            ),
        ))
        if not ok:
            self.get_logger().error("Force action server not available during unit pull.")
            produce_event(self.fsm.event_data, fail_evt)
            return

    def _handle_action_goal_response(self, future, context, fail_evt, goal_label, result_future_callback, result_callback=None):
        try:
            goal_handle = future.result()
            if goal_handle is None or not goal_handle.accepted:
                self.get_logger().error(f"{goal_label} rejected during {context}.")
                self.flow_logger.result(False, "Goal rejected")
                if result_callback is not None:
                    result_callback(None)
                else:
                    produce_event(self.fsm.event_data, fail_evt)
                return

            goal_handle.get_result_async().add_done_callback(result_future_callback)
        except Exception as e:
            self.get_logger().error(f"{goal_label} exception during {context}: {e}")
            self.flow_logger.result(False, str(e))
            if result_callback is not None:
                result_callback(None)
            else:
                produce_event(self.fsm.event_data, fail_evt)

    def _handle_action_result(self, future, context, fail_evt, action_label, success_check, failure_message_fn, success_evt=None, result_callback=None):
        try:
            wrapped_result = future.result()
            if wrapped_result is None:
                self.get_logger().error(f"{action_label} returned no result during {context}.")
                self.flow_logger.result(False, "No result")
                if result_callback is not None:
                    result_callback(None)
                else:
                    produce_event(self.fsm.event_data, fail_evt)
                return

            result = wrapped_result.result
            if success_check(result):
                self.get_logger().info(f"{action_label} succeeded during {context}.")
                self.flow_logger.result(True)
                if result_callback is not None:
                    result_callback(result)
                elif success_evt is not None:
                    produce_event(self.fsm.event_data, success_evt)
            else:
                msg = failure_message_fn(result)
                self.get_logger().error(f"{action_label} failed during {context}: {msg}")
                self.flow_logger.result(False, msg)
                if result_callback is not None:
                    result_callback(None)
                else:
                    produce_event(self.fsm.event_data, fail_evt)
        except Exception as e:
            self.get_logger().error(f"{action_label} result exception during {context}: {e}")
            self.flow_logger.result(False, str(e))
            if result_callback is not None:
                result_callback(None)
            else:
                produce_event(self.fsm.event_data, fail_evt)

    def _send_direct_arm_goal(self, pose, success_evt, fail_evt, context, result_callback=None):
        self.flow_logger.action(context[:1].upper() + context[1:])
        ok = self.robot_actions.send_arm_goal(pose, context, lambda fut: self._handle_action_goal_response(
            fut, context, fail_evt, "Arm goal",
            lambda res_fut: self._handle_action_result(
                res_fut, context, fail_evt, "Arm action",
                lambda result: result.result_code == ArmControl.Result.SUCCESS,
                lambda result: result.result_message if hasattr(result, "result_message") else result.message,
                success_evt=success_evt, result_callback=result_callback,
            ),
            result_callback=result_callback,
        ))
        if not ok:
            self.get_logger().error(f"Arm action server not available during {context}.")
            self.flow_logger.result(False, "Arm action server not available")
            if result_callback is not None:
                result_callback(None)
            elif fail_evt is not None:
                produce_event(self.fsm.event_data, fail_evt)
            return

    def _table_perceive_tilt_result(self, result):
        if result is None:
            produce_event(self.fsm.event_data, EventID.E_TABLE_PERCEIVE_FAIL)
            return
        self.request_place_pose()

    def _pre_place_before_pick_result(self, result):
        if result is None:
            produce_event(self.fsm.event_data, EventID.E_ARM_MOVE_FAIL)
            return
        self.user_data["view_pose_phase"] = "BEFORE_PICK"
        self.fsm.current_state_index = StateID.S_MOVE_TO_VIEW_POSE
        self.user_data["action_dispatched"] = False

    def _pick_pre_pose_result(self, result, pick_offset_pose, success_evt, fail_evt):
        if result is None:
            produce_event(self.fsm.event_data, fail_evt)
            return
        self._send_direct_arm_goal(pick_offset_pose, success_evt, fail_evt, "advance to object pick pose")

    def _on_gripper_success(self, result, success_evt):
        #special case: after closing on "unit", do the pull action before continuing FSM.
        # Wrench part (Wasim) tested and works but decided not to include in final demo as 'unit' is replaced by dummy unit
        # if (
        #     success_evt == EventID.E_GRIPPER_CLOSE_DONE
        #     and self.user_data["active_object_class"] == "unit"
        # ):
        #     self.get_logger().info(
        #         "Unit grasped. Starting force-control pull before continuing FSM."
        #     )
        #     self.send_unit_pull_wrench(
        #         EventID.E_GRIPPER_CLOSE_DONE,
        #         EventID.E_GRIPPER_FAIL,
        #     )
        #     return
        if success_evt == EventID.E_GRIPPER_OPEN_DONE and self.user_data["active_object_class"]:
            self.user_data["car_objects"].pop(self.user_data["active_object_class"], None)
            self.get_logger().info("Dropped object and removed it from pending list.")
            self.clear_active_car_object()
        produce_event(self.fsm.event_data, success_evt)

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
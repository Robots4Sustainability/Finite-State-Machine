#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Optional
from std_msgs.msg import Bool
import threading

import rclpy
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.duration import Duration
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.task import Future

from control_msgs.action import GripperCommand
from eddie_ros.action import ArmControl, GripperControl
from geometry_msgs.msg import Pose, PoseStamped
from my_robot_interfaces.action import RunVision
from pick_place_fsm.srv import RunScrewdriverRoutine
from tf2_ros import Buffer, TransformListener
from common import NamedPoseStore, PoseUtils, RobotActionHelper, gripper_action_name, gripper_action_type


class ScrewdriverPickupFromJson(Node):

    def __init__(self) -> None:
        super().__init__("screwdriver_pick_from_json")

        self.is_busy = False
        self.trigger_received = False
        self.worker_thread = None
        self.run_service = self.create_service(
            RunScrewdriverRoutine,
            "/screwdriver_pick/run",
            self.run_service_callback,
        )

        self.done_pub = self.create_publisher(Bool, "/screwdriver_pick/done", 10)

        self.declare_parameter("base_frame", "eddie_base_link")
        self.declare_parameter("ee_frame", "eddie_right_arm_robotiq_85_grasp_link")
        self.declare_parameter("screwdriver_pose_topic", "/object_pose_screwdriver")
        self.declare_parameter("arm_action_server", "right_arm/arm_control")
        self.declare_parameter("gripper_action_server", gripper_action_name())
        self.declare_parameter("perception_action_server", "run_perception_pipeline")
        self.declare_parameter("pose_store_path", str("/home/ashlesh/r4s/src/Finite-State-Machine/src/named_poses.json"))
        self.declare_parameter("pickup_z_offset", 0.10)
        self.declare_parameter("probe_z_offset", 0.15)
        self.declare_parameter("gripper_close_position", 0.30)
        self.declare_parameter("gripper_max_effort", 20.0)
        self.declare_parameter("perception_wait_timeout_sec", 8.0)
        # self.declare_parameter("auto_run", True)

        self.base_frame = str(self.get_parameter("base_frame").value)
        self.ee_frame = str(self.get_parameter("ee_frame").value)
        self.screwdriver_pose_topic = str(self.get_parameter("screwdriver_pose_topic").value)
        self.arm_action_server = str(self.get_parameter("arm_action_server").value)
        self.gripper_action_server = str(self.get_parameter("gripper_action_server").value)
        self.perception_action_server = str(self.get_parameter("perception_action_server").value)
        self.pose_store_path = Path(str(self.get_parameter("pose_store_path").value)).expanduser()
        self.pickup_z_offset = float(self.get_parameter("pickup_z_offset").value)
        self.probe_z_offset = float(self.get_parameter("probe_z_offset").value)
        self.gripper_close_position = float(self.get_parameter("gripper_close_position").value)
        self.gripper_max_effort = float(self.get_parameter("gripper_max_effort").value)
        self.perception_wait_timeout_sec = float(self.get_parameter("perception_wait_timeout_sec").value)
        # self.auto_run = bool(self.get_parameter("auto_run").value)    

        self.cb_group = ReentrantCallbackGroup()
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.pose_utils = PoseUtils(self, self.tf_buffer, self.base_frame, self.ee_frame)
        self.named_pose_store = NamedPoseStore(self, self.base_frame, self.pose_store_path)

        self.arm_client = ActionClient(
            self, ArmControl, self.arm_action_server, callback_group=self.cb_group
        )
        self.gripper_client = ActionClient(
            self, gripper_action_type(), self.gripper_action_server, callback_group=self.cb_group
        )
        self.perception_client = ActionClient(
            self, RunVision, self.perception_action_server, callback_group=self.cb_group
        )
        self.robot_actions = RobotActionHelper(self, self.arm_client, self.gripper_client)

        self.latest_screwdriver_pose: Optional[PoseStamped] = None
        self.requested_screw_poses = []
        self.create_subscription(
            PoseStamped,
            self.screwdriver_pose_topic,
            self.screwdriver_pose_callback,
            10,
            callback_group=self.cb_group,
        )

        # self._started = False
        self._shutdown_timer = None
        # self.create_timer(0.25, self.start_once, callback_group=self.cb_group)
        self.main_timer = self.create_timer(0.1, self.main_loop, callback_group=self.cb_group)

        self.get_logger().info("Screwdriver pickup node ready.")

    def run_service_callback(self, request, response):
        if self.is_busy:
            response.accepted = False
            response.message = "Screwdriver routine already running."
            self.get_logger().warn(response.message)
            return response
        try:
            payload = json.loads(request.request_json) if request.request_json else {}
            screw_poses = payload.get("screw_poses", [])
            self.requested_screw_poses = screw_poses if isinstance(screw_poses, list) else []
            self.get_logger().info(
                f"Received screwdriver request with {len(self.requested_screw_poses)} screw poses."
            )
        except Exception as exc:
            message = f"Invalid screwdriver request payload: {exc}"
            self.get_logger().error(message)
            self.requested_screw_poses = []
            response.accepted = False
            response.message = message
            return response

        self.trigger_received = True
        response.accepted = True
        response.message = "Screwdriver routine accepted."
        return response

    def main_loop(self):
        if not self.trigger_received or self.is_busy:
            return

        self.trigger_received = False
        self.is_busy = True

        self.worker_thread = threading.Thread(
            target=self._run_sequence_worker,
            daemon=True,
        )
        self.worker_thread.start()

    def _run_sequence_worker(self):
        ok = False
        try:
            ok = self.run_sequence()
        except Exception as exc:
            self.get_logger().error(f"Unhandled exception during screwdriver routine: {exc}")
            ok = False
        finally:
            done_msg = Bool()
            done_msg.data = ok
            self.done_pub.publish(done_msg)

            self.get_logger().info(
                "Screwdriver routine finished." if ok else "Screwdriver routine failed."
            )

            self.is_busy = False
            self.worker_thread = None

    

    # ----------------------------
    # Named poses
    # ----------------------------
    def get_named_pose(self, key: str) -> Optional[Pose]:
        return self.named_pose_store.get_named_pose(key)

    def get_table_drop_pose_global(self) -> Pose:
        pose = self.get_named_pose("table_drop_pose")
        if pose is not None:
            self.get_logger().info("Using 'table_drop_pose' from named poses.")
            return pose

        pose = Pose()
        pose.position.x = 0.60
        pose.position.y = -0.66
        pose.position.z = 0.343951
        pose.orientation.x = 0.475857
        pose.orientation.y = 0.493639
        pose.orientation.z = 0.546011
        pose.orientation.w = 0.481407
        self.get_logger().warn("No table_drop_pose found in JSON. Using hardcoded fallback table pose.")
        return pose

    def get_home_pose_global(self) -> Pose:
        for key in ("home_pose", "view_pose", "view_pose_global"):
            pose = self.get_named_pose(key)
            if pose is not None:
                self.get_logger().info(f"Using '{key}' from named poses as home pose.")
                return pose

        pose = Pose()
        pose.position.x = 0.729990
        pose.position.y = -0.285972
        pose.position.z = 0.575513
        pose.orientation.x = 0.461884
        pose.orientation.y = 0.469245
        pose.orientation.z = 0.549966
        pose.orientation.w = 0.513819
        self.get_logger().warn("No home pose found in JSON. Using hardcoded fallback home pose.")
        return pose

    # ----------------------------
    # ROS / TF helpers
    # ----------------------------
    def screwdriver_pose_callback(self, msg: PoseStamped) -> None:
        self.latest_screwdriver_pose = msg

    def global_pose_to_relative_pose(
        self, global_pose: Pose, global_frame: str, target_frame: str
    ) -> Optional[Pose]:
        return self.pose_utils.global_pose_to_relative_pose(global_pose, global_frame, target_frame)

    def relative_pose_to_global_pose(
        self, relative_pose: Pose, relative_frame: str, global_frame: str
    ) -> Optional[Pose]:
        return self.pose_utils.relative_pose_to_global_pose(relative_pose, relative_frame, global_frame)

    def transform_pose_stamped_to_base(self, pose_stamped: PoseStamped) -> Optional[PoseStamped]:
        return self.pose_utils.transform_pose_stamped_to_base(pose_stamped)

    def object_pose_to_relative_pose(self, detection: PoseStamped, z_offset: float = 0.0) -> Optional[Pose]:
        return self.pose_utils.object_pose_to_relative_pose(detection, z_offset)

    def make_relative_offset_pose(self, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0) -> Pose:
        return self.pose_utils.make_relative_offset_pose(dx=dx, dy=dy, dz=dz)

    # ----------------------------
    # Action helpers
    # ----------------------------
    def wait_for_servers(self) -> bool:
        ok = True
        if not self.arm_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error(f"Arm action server not available: {self.arm_action_server}")
            ok = False
        if not self.gripper_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error(
                f"Gripper action server not available: {self.gripper_action_server}"
            )
            ok = False
        if not self.perception_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().error(
                f"Perception action server not available: {self.perception_action_server}"
            )
            ok = False
        return ok

    def send_arm_goal_sync(self, pose: Pose, context: str) -> bool:
        goal = ArmControl.Goal()
        goal.target_pose = pose
        self.get_logger().info(f"Sending arm goal: {context}")
        goal_future = self.arm_client.send_goal_async(goal)
        goal_handle = self.wait_future(goal_future)
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().error(f"Arm goal rejected during {context}.")
            return False

        result_future = goal_handle.get_result_async()
        wrapped_result = self.wait_future(result_future)
        if wrapped_result is None:
            self.get_logger().error(f"No arm result during {context}.")
            return False

        result = wrapped_result.result
        if result.result_code == ArmControl.Result.SUCCESS:
            self.get_logger().info(f"Arm action succeeded during {context}.")
            return True

        msg = result.result_message if hasattr(result, "result_message") else result.message
        self.get_logger().error(f"Arm action failed during {context}: {msg}")
        return False

    def send_gripper_goal_sync(self, position: float, context: str) -> bool:
        if gripper_action_type() is GripperControl:
            goal = GripperControl.Goal()
            goal.target_position = position
            goal.velocity = 20.0
            goal.force = self.gripper_max_effort
        else:
            goal = GripperCommand.Goal()
            goal.command.position = position
            goal.command.max_effort = self.gripper_max_effort
        self.get_logger().info(f"Sending gripper goal: {context} position={position:.3f}")
        goal_future = self.gripper_client.send_goal_async(goal)
        goal_handle = self.wait_future(goal_future)
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().error(f"Gripper goal rejected during {context}.")
            return False

        result_future = goal_handle.get_result_async()
        wrapped_result = self.wait_future(result_future)
        if wrapped_result is None:
            self.get_logger().error(f"No gripper result during {context}.")
            return False

        result = wrapped_result.result
        if self.robot_actions.gripper_result_succeeded(result):
            self.get_logger().info(f"Gripper action succeeded during {context}.")
            return True

        self.get_logger().error(f"Gripper action failed during {context}: {self.robot_actions.gripper_failure_message(result)}")
        return False

    def move_to_global_pose(self, pose_global: Pose, context: str) -> bool:
        rel_pose = self.global_pose_to_relative_pose(pose_global, self.base_frame, self.ee_frame)
        if rel_pose is None:
            self.get_logger().error(f"Failed to resolve target pose during {context}.")
            return False
        return self.send_arm_goal_sync(rel_pose, context)

    def send_pick_object_sequence(
        self,
        pre_pick_pose: Pose,
        pick_offset_pose: Pose,
        context_prefix: str,
    ) -> bool:
        if not self.send_arm_goal_sync(pre_pick_pose, f"{context_prefix}: pre-pick"):
            return False
        return self.send_arm_goal_sync(pick_offset_pose, f"{context_prefix}: advance to grasp")

    def request_screwdriver_pose(self) -> Optional[PoseStamped]:
        self.latest_screwdriver_pose = None

        goal = RunVision.Goal()
        goal.task_name = "detect_screwdriver"
        goal.object_class = ""
        goal.time_duration = 0.0

        self.get_logger().info("Requesting screwdriver pose from perception action...")
        goal_future = self.perception_client.send_goal_async(goal)
        goal_handle = self.wait_future(goal_future)
        if goal_handle is None or not goal_handle.accepted:
            self.get_logger().error("Perception goal rejected during detect_screwdriver.")
            return None

        wrapped_result = self.wait_future(goal_handle.get_result_async())
        if wrapped_result is None:
            self.get_logger().error("No perception result during detect_screwdriver.")
            return None

        result = wrapped_result.result
        if result is None or not result.success:
            message = "no response" if result is None else result.message
            self.get_logger().error(f"Screwdriver perception failed: {message}")
            return None

        perceived_pose = None
        if result.poses:
            perceived_pose = result.poses[0]
        elif self.latest_screwdriver_pose is not None:
            perceived_pose = self.latest_screwdriver_pose
        else:
            self.get_logger().error(
                "Perception succeeded but returned no screwdriver pose in action result or topic."
            )
            return None

        screwdriver_pose_base = self.transform_pose_stamped_to_base(perceived_pose)
        if screwdriver_pose_base is None:
            self.get_logger().error("Failed to transform perceived screwdriver pose to base frame.")
            return None
        return screwdriver_pose_base

    def pose_stamped_from_payload(self, payload: dict) -> Optional[PoseStamped]:
        try:
            pose_data = payload["pose"] if "pose" in payload else payload
            msg = PoseStamped()
            msg.header.frame_id = str(pose_data.get("frame_id", self.base_frame))
            msg.header.stamp = self.get_clock().now().to_msg()
            position = pose_data["position"]
            orientation = pose_data.get("orientation", {})
            msg.pose.position.x = float(position["x"])
            msg.pose.position.y = float(position["y"])
            msg.pose.position.z = float(position["z"])
            msg.pose.orientation.x = float(orientation.get("x", 0.0))
            msg.pose.orientation.y = float(orientation.get("y", 0.0))
            msg.pose.orientation.z = float(orientation.get("z", 0.0))
            msg.pose.orientation.w = float(orientation.get("w", 1.0))
            return msg
        except Exception as exc:
            self.get_logger().error(f"Invalid screw pose payload: {exc}")
            return None

    def move_to_probe_pose(self, screw_payload: dict, index: int) -> bool:
        screw_pose = self.pose_stamped_from_payload(screw_payload)
        if screw_pose is None:
            return False

        screw_pose_base = self.transform_pose_stamped_to_base(screw_pose)
        if screw_pose_base is None:
            self.get_logger().error(f"Failed to transform screw pose {index} to base frame.")
            return False

        probe_pose = Pose()
        probe_pose.position.x = screw_pose_base.pose.position.x
        probe_pose.position.y = screw_pose_base.pose.position.y
        probe_pose.position.z = screw_pose_base.pose.position.z - self.probe_z_offset
        probe_pose.orientation = screw_pose_base.pose.orientation
        return self.move_to_global_pose(probe_pose, f"probe screw {index}")

    # ----------------------------
    # Flow
    # ----------------------------
    # def start_once(self) -> None:
    #     if self._started or not self.auto_run:
    #         return
    #     self._started = True

    #     ok = False
    #     try:
    #         ok = self.run_sequence()
    #     except Exception as exc:
    #         self.get_logger().error(f"Unhandled exception during screwdriver routine: {exc}")
    #     finally:
    #         self.get_logger().info("Screwdriver routine finished." if ok else "Screwdriver routine failed.")
    #         self._shutdown_timer = self.create_timer(0.5, self.shutdown_once, callback_group=self.cb_group)

    # def shutdown_once(self) -> None:
    #     if self._shutdown_timer is not None:
    #         self._shutdown_timer.cancel()
    #         self._shutdown_timer = None
    #     raise SystemExit

    def wait_future(self, future: Future):
        while rclpy.ok() and not future.done():
            rclpy.spin_once(self, timeout_sec=0.1)
        if not future.done():
            return None
        try:
            return future.result()
        except Exception as exc:
            self.get_logger().error(f"Future failed: {exc}")
            return None

    def wait_for_screwdriver_pose(self, timeout_sec: float) -> Optional[PoseStamped]:
        deadline = self.get_clock().now() + Duration(seconds=timeout_sec)
        while rclpy.ok() and self.get_clock().now() < deadline:
            if self.latest_screwdriver_pose is not None:
                self.get_logger().info("Received perceived screwdriver pose.")
                return self.latest_screwdriver_pose
            rclpy.spin_once(self, timeout_sec=0.1)
        return None

    def run_sequence(self) -> bool:
        if not self.wait_for_servers():
            return False

        table_drop_pose = self.get_table_drop_pose_global()
        home_pose = self.get_home_pose_global()
        if not self.move_to_global_pose(table_drop_pose, "move to table drop pose before screwdriver perception"):
            return False

        screwdriver_pose_base = self.request_screwdriver_pose()
        if screwdriver_pose_base is None:
            return False

        pre_pick_pose = self.object_pose_to_relative_pose(screwdriver_pose_base, z_offset=self.pickup_z_offset)
        if pre_pick_pose is None:
            self.get_logger().error("Failed to build screwdriver pre-pick pose.")
            return False

        if not self.send_pick_object_sequence(pre_pick_pose, self.make_relative_offset_pose(dz=self.pickup_z_offset), "pick screwdriver"):
            return False

        if not self.send_gripper_goal_sync(self.gripper_close_position, "close gripper on screwdriver"):
            return False

        if not self.send_arm_goal_sync(self.make_relative_offset_pose(dz=-self.pickup_z_offset), "retreat with screwdriver"):
            return False

        if not self.move_to_global_pose(home_pose, "move screwdriver near home pose"):
            return False

        if self.requested_screw_poses:
            for index, screw_payload in enumerate(self.requested_screw_poses, start=1):
                if not self.move_to_probe_pose(screw_payload, index):
                    return False
                if not self.move_to_global_pose(home_pose, f"return to home pose after probing screw {index}"):
                    return False

        if not self.send_gripper_goal_sync(0.0, "open gripper after screwdriver routine"):
            return False

        self.get_logger().info("Screwdriver routine complete.")
        return True


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ScrewdriverPickupFromJson()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
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
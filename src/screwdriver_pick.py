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
from eddie_ros.action import ArmControl
from geometry_msgs.msg import Pose, PoseStamped
from tf2_geometry_msgs import do_transform_pose
from tf2_ros import Buffer, TransformListener


class ScrewdriverPickupFromJson(Node):
    """
    Standalone screwdriver pickup routine.

    Flow:
      1. Move to `screwdriver_pose` loaded from named_poses.json.
      2. Wait for the perceived screwdriver pose on `/object_pose_screwdriver`.
      3. Pick it using the same pre-grasp -> grasp -> close -> retreat pattern
         used for car objects in door_disassemble.py.
      4. Return to home pose from JSON (or a hardcoded fallback).
    """

    def __init__(self) -> None:
        super().__init__("screwdriver_pick_from_json")

        self.is_busy = False
        self.trigger_received = False
        self.worker_thread = None

        self.trigger_sub = self.create_subscription(
            Bool,
            "/screwdriver_pick/start",
            self.start_callback,
            10,
        )

        self.done_pub = self.create_publisher(Bool, "/screwdriver_pick/done", 10)

        self.declare_parameter("base_frame", "eddie_base_link")
        self.declare_parameter("ee_frame", "eddie_right_arm_robotiq_85_grasp_link")
        self.declare_parameter("screwdriver_pose_topic", "/object_pose_screwdriver")
        self.declare_parameter("arm_action_server", "right_arm/arm_control")
        self.declare_parameter("gripper_action_server", "robotiq_gripper_controller/gripper_cmd")
        self.declare_parameter("pose_store_path", "/home/r4s/r4s-ws/src/Finite-state-Machine/src/named_poses.json")
        self.declare_parameter("pickup_z_offset", 0.10)
        self.declare_parameter("gripper_close_position", 0.30)
        self.declare_parameter("gripper_max_effort", 20.0)
        self.declare_parameter("perception_wait_timeout_sec", 8.0)
        # self.declare_parameter("auto_run", True)

        self.base_frame = str(self.get_parameter("base_frame").value)
        self.ee_frame = str(self.get_parameter("ee_frame").value)
        self.screwdriver_pose_topic = str(self.get_parameter("screwdriver_pose_topic").value)
        self.arm_action_server = str(self.get_parameter("arm_action_server").value)
        self.gripper_action_server = str(self.get_parameter("gripper_action_server").value)
        self.pose_store_path = Path(str(self.get_parameter("pose_store_path").value)).expanduser()
        self.pickup_z_offset = float(self.get_parameter("pickup_z_offset").value)
        self.gripper_close_position = float(self.get_parameter("gripper_close_position").value)
        self.gripper_max_effort = float(self.get_parameter("gripper_max_effort").value)
        self.perception_wait_timeout_sec = float(self.get_parameter("perception_wait_timeout_sec").value)
        # self.auto_run = bool(self.get_parameter("auto_run").value)    

        self.cb_group = ReentrantCallbackGroup()
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.arm_client = ActionClient(
            self, ArmControl, self.arm_action_server, callback_group=self.cb_group
        )
        self.gripper_client = ActionClient(
            self, GripperCommand, self.gripper_action_server, callback_group=self.cb_group
        )

        self.latest_screwdriver_pose: Optional[PoseStamped] = None
        self.create_subscription(
            PoseStamped,
            self.screwdriver_pose_topic,
            self.screwdriver_pose_callback,
            10,
            callback_group=self.cb_group,
        )

        self.named_poses = self.load_named_poses()
        # self._started = False
        self._shutdown_timer = None
        # self.create_timer(0.25, self.start_once, callback_group=self.cb_group)
        self.main_timer = self.create_timer(0.1, self.main_loop, callback_group=self.cb_group)

        self.get_logger().info("Screwdriver pickup node ready.")

    def start_callback(self, msg: Bool):
        if not msg.data:
            return

        if self.is_busy:
            self.get_logger().warn("Screwdriver routine already running.")
            return

        self.get_logger().info("Received trigger on /screwdriver_pick/start")
        self.trigger_received = True


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
    def load_named_poses(self) -> dict:
        if not self.pose_store_path.exists():
            self.get_logger().warn(
                f"Named pose file not found at {self.pose_store_path}. Using empty pose set."
            )
            return {}

        try:
            data = json.loads(self.pose_store_path.read_text())
            if not isinstance(data, dict):
                raise ValueError("JSON root must be an object")
            self.get_logger().info(f"Loaded named poses from {self.pose_store_path}.")
            return data
        except Exception as exc:
            self.get_logger().error(f"Failed to load named poses: {exc}")
            return {}

    def pose_from_dict(self, pose_data: dict) -> Optional[Pose]:
        try:
            pose = Pose()
            position = pose_data["position"]
            orientation = pose_data["orientation"]
            pose.position.x = float(position["x"])
            pose.position.y = float(position["y"])
            pose.position.z = float(position["z"])
            pose.orientation.x = float(orientation["x"])
            pose.orientation.y = float(orientation["y"])
            pose.orientation.z = float(orientation["z"])
            pose.orientation.w = float(orientation["w"])
            return pose
        except Exception:
            return None

    def get_named_pose(self, key: str) -> Optional[Pose]:
        pose_data = self.named_poses.get(key)
        if not isinstance(pose_data, dict):
            return None

        frame_id = pose_data.get("frame_id")
        if frame_id and frame_id != self.base_frame:
            self.get_logger().warn(
                f"Named pose '{key}' uses frame '{frame_id}', expected '{self.base_frame}'. Ignoring it."
            )
            return None

        pose = self.pose_from_dict(pose_data)
        if pose is None:
            self.get_logger().warn(f"Named pose '{key}' is malformed. Ignoring it.")
        return pose

    def get_screwdriver_view_pose_global(self) -> Optional[Pose]:
        pose = self.get_named_pose("screwdriver_pose")
        if pose is not None:
            self.get_logger().info("Using 'screwdriver_pose' from named poses.")
            return pose
        self.get_logger().error("Missing 'screwdriver_pose' in named poses JSON.")
        return None

    def get_home_pose_global(self) -> Pose:
        for key in ("home_pose", "view_pose", "view_pose_global"):
            pose = self.get_named_pose(key)
            if pose is not None:
                self.get_logger().info(f"Using '{key}' from named poses as home pose.")
                return pose

        # Fallback to the current door_disassemble hardcoded home/view pose.
        pose = Pose()
        pose.position.x = 0.684225
        pose.position.y = -0.228704
        pose.position.z = 0.561060
        pose.orientation.x = 0.492322
        pose.orientation.y = 0.471536
        pose.orientation.z = 0.527013
        pose.orientation.w = 0.507474
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
        try:
            transform = self.tf_buffer.lookup_transform(
                target_frame, global_frame, rclpy.time.Time()
            )
            return do_transform_pose(global_pose, transform)
        except Exception as exc:
            self.get_logger().warn(f"Failed to transform global pose to relative: {exc}")
            return None

    def relative_pose_to_global_pose(
        self, relative_pose: Pose, relative_frame: str, global_frame: str
    ) -> Optional[Pose]:
        try:
            transform = self.tf_buffer.lookup_transform(
                global_frame, relative_frame, rclpy.time.Time()
            )
            return do_transform_pose(relative_pose, transform)
        except Exception as exc:
            self.get_logger().warn(f"Failed to transform relative pose to global: {exc}")
            return None

    def transform_pose_stamped_to_base(self, pose_stamped: PoseStamped) -> Optional[PoseStamped]:
        source_frame = pose_stamped.header.frame_id
        if (
            source_frame
            and source_frame != self.base_frame
            and not source_frame.startswith("eddie_right_arm_")
        ):
            source_frame = f"eddie_right_arm_{source_frame}"

        transformed_pose = self.relative_pose_to_global_pose(
            pose_stamped.pose, source_frame, self.base_frame
        )
        if transformed_pose is None:
            return None

        result = PoseStamped()
        result.header.frame_id = self.base_frame
        result.header.stamp = self.get_clock().now().to_msg()
        result.pose = transformed_pose
        return result

    def object_pose_to_relative_pose(self, detection: PoseStamped, z_offset: float = 0.0) -> Optional[Pose]:
        transformed_pose = self.global_pose_to_relative_pose(
            detection.pose, detection.header.frame_id, self.ee_frame
        )
        if transformed_pose is None:
            return None
        transformed_pose.position.z -= z_offset
        return transformed_pose

    def make_relative_offset_pose(self, dx: float = 0.0, dy: float = 0.0, dz: float = 0.0) -> Pose:
        pose = Pose()
        pose.position.x = dx
        pose.position.y = dy
        pose.position.z = dz
        pose.orientation.w = 1.0
        return pose

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
        if result.reached_goal or result.stalled:
            self.get_logger().info(f"Gripper action succeeded during {context}.")
            return True

        self.get_logger().error(
            f"Gripper action failed during {context}: "
            f"reached_goal={result.reached_goal}, stalled={result.stalled}, "
            f"position={result.position:.4f}, effort={result.effort:.4f}"
        )
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

        screwdriver_view_pose = self.get_screwdriver_view_pose_global()
        if screwdriver_view_pose is None:
            return False
        home_pose = self.get_home_pose_global()

        # Clear stale pose so we wait for a fresh perception result after reaching the view pose.
        self.latest_screwdriver_pose = None

        if not self.move_to_global_pose(screwdriver_view_pose, "move to screwdriver view pose"):
            return False

        perceived_pose = self.wait_for_screwdriver_pose(self.perception_wait_timeout_sec)
        if perceived_pose is None:
            self.get_logger().error(
                f"No screwdriver pose received on {self.screwdriver_pose_topic} within {self.perception_wait_timeout_sec:.1f}s."
            )
            return False

        screwdriver_pose_base = self.transform_pose_stamped_to_base(perceived_pose)
        if screwdriver_pose_base is None:
            self.get_logger().error("Failed to transform perceived screwdriver pose to base frame.")
            return False

        pre_pick_pose = self.object_pose_to_relative_pose(
            screwdriver_pose_base, z_offset=self.pickup_z_offset
        )
        if pre_pick_pose is None:
            self.get_logger().error("Failed to build screwdriver pre-pick pose.")
            return False

        if not self.send_pick_object_sequence(
            pre_pick_pose,
            self.make_relative_offset_pose(dz=self.pickup_z_offset),
            "pick screwdriver",
        ):
            return False

        if not self.send_gripper_goal_sync(self.gripper_close_position, "close gripper on screwdriver"):
            return False

        if not self.send_arm_goal_sync(
            self.make_relative_offset_pose(dz=-self.pickup_z_offset),
            "retreat with screwdriver",
        ):
            return False

        if not self.move_to_global_pose(home_pose, "return to home pose"):
            return False

        self.get_logger().info("Screwdriver pickup complete.")
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

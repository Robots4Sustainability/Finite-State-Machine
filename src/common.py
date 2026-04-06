#!/usr/bin/env python3
import json
from pathlib import Path

import rclpy
from geometry_msgs.msg import Pose, PoseStamped
from tf2_geometry_msgs import do_transform_pose

from control_msgs.action import GripperCommand
from eddie_ros.action import ArmControl, ForceControl, GripperControl
from my_robot_interfaces.action import RunVision

USE_SIM = True # Set to True to use GripperControl action, False to use GripperCommand action


def gripper_action_type():
    return GripperControl if USE_SIM else GripperCommand


def gripper_action_name() -> str:
    return "right_arm/gripper_control" if USE_SIM else "robotiq_gripper_controller/gripper_cmd"


class FlowLogger:
    SEPARATOR = "=" * 52

    def __init__(self, node):
        self.node = node
        self._last_line_was_result = False

    def state_banner(self, state_name: str, object_name: str = "", phase: str = ""):
        logger = self.node.get_logger()
        logger.info(" ")
        logger.info(self.SEPARATOR)
        logger.info(f"STATE: {state_name}")
        if object_name:
            logger.info(f"OBJECT: {object_name}")
        if phase:
            logger.info(f"PHASE: {phase}")
        logger.info(self.SEPARATOR)
        logger.info(" ")
        self._last_line_was_result = False

    def action(self, description: str):
        if self._last_line_was_result:
            self.node.get_logger().info(" ")
        self.node.get_logger().info(f"Action: {description}")
        self._last_line_was_result = False

    def result(self, success: bool, detail: str = ""):
        logger = self.node.get_logger()
        if detail:
            message = f"Result: {'Success' if success else 'Failure'} ({detail})"
        else:
            message = f"Result: {'Success' if success else 'Failure'}"
        if success:
            logger.info(message)
        else:
            logger.error(message)
        self._last_line_was_result = True


class NamedPoseStore:
    def __init__(self, node, base_frame: str, pose_store_path: Path):
        self.node = node
        self.base_frame = base_frame
        self.pose_store_path = Path(pose_store_path).expanduser()
        self.named_poses = self.load_named_poses()

    def load_named_poses(self) -> dict:
        if not self.pose_store_path.exists():
            self.node.get_logger().info(
                f"Named pose file not found at {self.pose_store_path}. Using hardcoded defaults."
            )
            return {}

        try:
            data = json.loads(self.pose_store_path.read_text())
            if not isinstance(data, dict):
                raise ValueError("named pose file root is not an object")
            self.node.get_logger().info(f"Loaded named poses from {self.pose_store_path}.")
            return data
        except Exception as exc:
            self.node.get_logger().warn(
                f"Could not load named poses from {self.pose_store_path}: {exc}. "
                "Using hardcoded defaults."
            )
            return {}

    def pose_from_dict(self, pose_data) -> Pose | None:
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

    def get_named_pose(self, key: str) -> Pose | None:
        pose_data = self.named_poses.get(key)
        if not isinstance(pose_data, dict):
            return None

        frame_id = pose_data.get("frame_id")
        if frame_id and frame_id != self.base_frame:
            self.node.get_logger().warn(
                f"Named pose '{key}' uses frame '{frame_id}', expected '{self.base_frame}'. "
                "Ignoring it."
            )
            return None

        pose = self.pose_from_dict(pose_data)
        if pose is None:
            self.node.get_logger().warn(f"Named pose '{key}' is malformed. Ignoring it.")
        return pose


class PoseUtils:
    def __init__(self, node, tf_buffer, base_frame: str, ee_frame: str):
        self.node = node
        self.tf_buffer = tf_buffer
        self.base_frame = base_frame
        self.ee_frame = ee_frame

    def global_pose_to_relative_pose(
        self, global_pose: Pose, global_frame: str, target_frame: str
    ) -> Pose | None:
        try:
            transform = self.tf_buffer.lookup_transform(
                target_frame, global_frame, rclpy.time.Time()
            )
            return do_transform_pose(global_pose, transform)
        except Exception as exc:
            self.node.get_logger().warn(f"Failed to transform global pose to relative: {exc}")
            return None

    def relative_pose_to_global_pose(
        self, relative_pose: Pose, relative_frame: str, global_frame: str
    ) -> Pose | None:
        try:
            transform = self.tf_buffer.lookup_transform(
                global_frame, relative_frame, rclpy.time.Time()
            )
            return do_transform_pose(relative_pose, transform)
        except Exception as exc:
            self.node.get_logger().warn(f"Failed to transform relative pose to global: {exc}")
            return None

    def transform_pose_stamped_to_base(self, pose_stamped: PoseStamped) -> PoseStamped | None:
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
        result.header.stamp = self.node.get_clock().now().to_msg()
        result.pose = transformed_pose
        return result

    def transform_pose_array_to_base(self, poses):
        transformed_poses = []
        for index, pose_stamped in enumerate(poses):
            transformed_pose = self.transform_pose_stamped_to_base(pose_stamped)
            if transformed_pose is None:
                self.node.get_logger().error(
                    f"Failed to transform perception pose {index} into {self.base_frame}."
                )
                return None
            transformed_poses.append(transformed_pose)
        return transformed_poses

    def make_relative_offset_pose(self, dx=0.0, dy=0.0, dz=0.0) -> Pose:
        pose = Pose()
        pose.position.x = dx
        pose.position.y = dy
        pose.position.z = dz
        pose.orientation.w = 1.0
        return pose

    def make_relative_orientation_pose(self, qx=0.0, qy=0.0, qz=0.0, qw=1.0) -> Pose:
        pose = Pose()
        pose.orientation.x = qx
        pose.orientation.y = qy
        pose.orientation.z = qz
        pose.orientation.w = qw
        return pose

    def object_pose_to_relative_pose(self, detection, z_offset=0.0) -> Pose | None:
        if detection is None:
            self.node.get_logger().error("Active object detection is missing pose data.")
            return None

        transformed_pose = self.global_pose_to_relative_pose(
            detection.pose, detection.header.frame_id, self.ee_frame
        )
        if transformed_pose is None:
            return None

        transformed_pose.position.z -= z_offset
        return transformed_pose


class RobotActionHelper:
    def __init__(self, node, arm_client, gripper_client, force_client=None):
        self.node = node
        self.arm_client = arm_client
        self.gripper_client = gripper_client
        self.force_client = force_client

    def send_arm_goal(self, pose: Pose, context: str, goal_response_callback) -> bool:
        if not self.arm_client.wait_for_server(timeout_sec=1.0):
            self.node.get_logger().error(f"Arm action server not available during {context}.")
            return False

        goal = ArmControl.Goal()
        goal.target_pose = pose
        future = self.arm_client.send_goal_async(goal)
        future.add_done_callback(goal_response_callback)
        return True

    def send_gripper_goal(
        self,
        position: float,
        context: str,
        goal_response_callback,
        max_effort: float = 20.0,
    ) -> bool:
        if not self.gripper_client.wait_for_server(timeout_sec=1.0):
            self.node.get_logger().error(
                f"Gripper action server not available during {context}."
            )
            return False

        if USE_SIM:
            goal = GripperControl.Goal()
            goal.target_position = position
            goal.velocity = 20.0
            goal.force = max_effort
        else:
            goal = GripperCommand.Goal()
            goal.command.position = position
            goal.command.max_effort = max_effort
        future = self.gripper_client.send_goal_async(goal)
        future.add_done_callback(goal_response_callback)
        return True

    def gripper_result_succeeded(self, result) -> bool:
        if USE_SIM:
            return result.result_code == GripperControl.Result.SUCCESS
        return result.reached_goal or result.stalled

    def gripper_failure_message(self, result) -> str:
        if USE_SIM:
            return (
                result.result_message
                if hasattr(result, "result_message")
                else "unknown gripper failure"
            )
        return (
            f"reached_goal={result.reached_goal}, "
            f"stalled={result.stalled}, "
            f"position={result.position:.4f}, "
            f"effort={result.effort:.4f}"
        )

    def send_force_goal(self, context: str, goal_response_callback) -> bool:
        if self.force_client is None:
            self.node.get_logger().error(f"Force action client not configured during {context}.")
            return False

        if not self.force_client.wait_for_server(timeout_sec=1.0):
            self.node.get_logger().error(f"Force action server not available during {context}.")
            return False

        goal = ForceControl.Goal()
        goal.wrench.force.x = 10.0
        goal.wrench.force.y = 0.0
        goal.wrench.force.z = 0.0
        goal.wrench.torque.x = 0.0
        goal.wrench.torque.y = 0.0
        goal.wrench.torque.z = 0.0
        goal.duration = 3.0

        self.node.get_logger().info(
            "Sending unit pull wrench goal: "
            f"Fx={goal.wrench.force.x:.2f}, "
            f"Fy={goal.wrench.force.y:.2f}, "
            f"Fz={goal.wrench.force.z:.2f}, "
            f"duration={goal.duration:.2f}s"
        )

        future = self.force_client.send_goal_async(goal)
        future.add_done_callback(goal_response_callback)
        return True


class PerceptionHelper:
    def __init__(self, node, perception_client, pose_utils: PoseUtils, base_frame: str):
        self.node = node
        self.perception_client = perception_client
        self.pose_utils = pose_utils
        self.base_frame = base_frame

    def send_request(self, task_name, object_class, result_callback, time_duration=0.0):
        if not self.perception_client.wait_for_server(timeout_sec=2.0):
            self.node.get_logger().error("Perception action server not available.")
            result_callback(None)
            return

        goal = RunVision.Goal()
        goal.task_name = task_name
        goal.object_class = object_class
        goal.time_duration = float(time_duration)
        future = self.perception_client.send_goal_async(goal)
        future.add_done_callback(
            lambda fut: self._goal_response(
                fut, task_name, object_class, result_callback
            )
        )

    def _goal_response(self, future, task_name, object_class, result_callback):
        try:
            goal_handle = future.result()
            if goal_handle is None or not goal_handle.accepted:
                self.node.get_logger().error(
                    "Perception goal rejected for task "
                    f"'{task_name}' object_class='{object_class}'."
                )
                result_callback(None)
                return

            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(
                lambda fut: result_callback(fut.result().result if fut.result() else None)
            )
        except Exception as exc:
            self.node.get_logger().error(
                "Perception goal exception for task "
                f"'{task_name}' object_class='{object_class}': {exc}"
            )
            result_callback(None)

    def extract_transformed_poses(self, result, label: str, min_count: int = 1):
        if result is None or not result.success:
            message = "no response" if result is None else result.message
            self.node.get_logger().error(f"{label.capitalize()} perception failed: {message}")
            return None

        transformed_poses = self.pose_utils.transform_pose_array_to_base(result.poses)
        if transformed_poses is None or len(transformed_poses) < min_count:
            self.node.get_logger().error(
                f"{label.capitalize()} perception returned no valid poses."
            )
            return None
        return transformed_poses

    def store_car_object(self, object_class, result, car_objects: dict) -> bool:
        transformed_poses = self.extract_transformed_poses(
            result, f"object '{object_class}'", min_count=1
        )
        if transformed_poses is None:
            return False

        if len(transformed_poses) > 1:
            self.node.get_logger().warn(
                f"Object perception returned {len(transformed_poses)} poses for class "
                f"'{object_class}'. Using the first one."
            )

        car_objects[object_class] = {
            "pose": transformed_poses[0],
            "radius": result.estimated_value,
        }
        self.node.get_logger().info(
            f"Stored {object_class} object pose in {self.base_frame} "
            f"with radius {result.estimated_value}."
        )
        return True

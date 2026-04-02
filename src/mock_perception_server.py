#!/usr/bin/env python3
import random
import time

import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionServer
from rclpy.node import Node

from my_robot_interfaces.action import RunVision


class MockPerceptionServer(Node):
    def __init__(self):
        super().__init__("mock_perception_server")

        self.declare_parameter("action_name", "run_perception_pipeline")
        self.declare_parameter("base_frame", "eddie_base_link")
        self.declare_parameter("camera_frame", "eddie_right_arm_camera_link")

        self.action_name = self.get_parameter("action_name").value
        self.base_frame = self.get_parameter("base_frame").value
        self.camera_frame = self.get_parameter("camera_frame").value
        self.place_request_index = 0

        self.server = ActionServer(
            self,
            RunVision,
            self.action_name,
            execute_callback=self.execute_callback,
        )

        self.get_logger().info(
            f"Mock perception action server ready on '{self.action_name}'."
        )

    def execute_callback(self, goal_handle):
        task_name = goal_handle.request.task_name.strip().lower()
        object_class = goal_handle.request.object_class.strip().lower()
        self.get_logger().info(
            "Received perception request for task "
            f"'{task_name}' object_class='{object_class}'."
        )
        delay = random.uniform(2.0, 3.0)
        self.get_logger().info(f"Mock perception delay: sleeping for {delay:.2f}s.")
        time.sleep(delay)

        result = RunVision.Result()
        result.estimated_value = 0.0

        if task_name in ("subdoor", "subdoor_pose"):
            result.success = True
            result.message = "Returned 4 mock subdoor poses"
            result.poses = self.mock_subdoor_poses()
            goal_handle.succeed()
            return result

        if task_name == "car_objects":
            mock_result = self.mock_car_object_result(object_class)
            if mock_result is None:
                result.success = False
                result.message = (
                    f"Unsupported mock object_class '{object_class}' for task '{task_name}'. "
                    "Supported classes: motor_grip, unit, speaker."
                )
                result.poses = []
                goal_handle.abort()
                return result

            poses, radius = mock_result
            result.success = True
            result.message = (
                f"Returned {len(poses)} mock car object poses for class '{object_class}'."
            )
            result.poses = poses
            result.estimated_value = radius
            goal_handle.succeed()
            return result

        if task_name == "place_object":
            poses = self.mock_place_object_poses(goal_handle.request.time_duration)
            result.success = True
            result.message = (
                f"Returned {len(poses)} mock place poses for class '{object_class}' "
                f"with requested radius {goal_handle.request.time_duration:.4f}."
            )
            result.poses = poses
            goal_handle.succeed()
            return result

        result.success = False
        result.message = (
            f"Unsupported mock perception task '{task_name}'. "
            "Supported tasks: subdoor_pose, car_objects, place_object."
        )
        result.poses = []
        goal_handle.abort()
        return result

    def mock_subdoor_poses(self):
        return [
            self.make_pose_stamped(self.base_frame, 0.62, 0.26, 0.84),
            self.make_pose_stamped(self.base_frame, 0.64, -0.08, 0.80),
            self.make_pose_stamped(self.base_frame, 0.67, -0.24, 0.44),
            self.make_pose_stamped(self.base_frame, 0.61, 0.30, 0.42),
        ]

    def mock_car_object_result(self, object_class: str):
        if object_class == "motor_grip":
            return (
                [
                    self.make_pose_stamped(
                        self.base_frame,
                        0.689018,
                        0.100537,
                        0.531908,
                        0.680738,
                        0.007456,
                        0.731865,
                        0.030235,
                    ),
                ],
                0.045,
            )

        if object_class == "unit":
            return (
                [
                    self.make_pose_stamped(
                        self.base_frame,
                        0.691119,
                        -0.137204,
                        0.403723,
                        0.418785,
                        0.536685,
                        0.432927,
                        0.590900,
                    ),
                ],
                0.065,
            )

        if object_class == "speaker":
            return (
                [
                    self.make_pose_stamped(
                        self.base_frame,
                        0.703098,
                        -0.348875,
                        0.433091,
                        0.487408,
                        0.475228,
                        0.508764,
                        0.527022,
                    ),
                ],
                0.055,
            )

        return None

    def mock_place_object_poses(self, radius: float):
        placements = [
            (0.62, -0.60, 0.343951),
            (0.62, -0.73, 0.343951),
            (0.74, -0.60, 0.343951),
            (0.74, -0.73, 0.343951),
        ]

        index = self.place_request_index % len(placements)
        self.place_request_index += 1
        x, y, z = placements[index]

        if radius > 0.0:
            z += min(radius, 0.1)

        return [self.make_pose_stamped(self.base_frame, x, y, z)]

    def make_pose_stamped(
        self,
        frame_id: str,
        x: float,
        y: float,
        z: float,
        qx: float = 0.0,
        qy: float = 0.0,
        qz: float = 0.0,
        qw: float = 1.0,
    ) -> PoseStamped:
        msg = PoseStamped()
        msg.header.frame_id = frame_id
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = z
        msg.pose.orientation.x = qx
        msg.pose.orientation.y = qy
        msg.pose.orientation.z = qz
        msg.pose.orientation.w = qw
        return msg


def main(args=None):
    rclpy.init(args=args)
    node = MockPerceptionServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Mock perception server stopped via KeyboardInterrupt")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()

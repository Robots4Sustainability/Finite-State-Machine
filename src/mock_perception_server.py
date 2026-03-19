#!/usr/bin/env python3
import random
import time

import rclpy
from geometry_msgs.msg import PoseStamped
from rclpy.action import ActionServer
from rclpy.node import Node

from pick_place_fsm.action import Perception


class MockPerceptionServer(Node):
    def __init__(self):
        super().__init__("mock_perception_server")

        self.declare_parameter("action_name", "perception")
        self.declare_parameter("base_frame", "eddie_base_link")
        self.declare_parameter("camera_frame", "eddie_right_arm_camera_link")

        self.action_name = self.get_parameter("action_name").value
        self.base_frame = self.get_parameter("base_frame").value
        self.camera_frame = self.get_parameter("camera_frame").value

        self.server = ActionServer(
            self,
            Perception,
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

        result = Perception.Result()
        result.estimated_value = 0.0

        if task_name == "subdoor":
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
                    "Supported classes: motor, unit."
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

        result.success = False
        result.message = (
            f"Unsupported mock perception task '{task_name}'. "
            "Supported tasks: subdoor, car_objects."
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
        if object_class == "motor":
            return (
                [
                    self.make_pose_stamped(self.base_frame, 0.75, 0.348875, 0.433091),
                ],
                0.045,
            )

        if object_class == "unit":
            return (
                [
                    self.make_pose_stamped(self.base_frame, 0.75, 0.000823, 0.426174),
                ],
                0.065,
            )

        return None

    def make_pose_stamped(self, frame_id: str, x: float, y: float, z: float) -> PoseStamped:
        msg = PoseStamped()
        msg.header.frame_id = frame_id
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.position.z = z
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.0
        msg.pose.orientation.w = 1.0
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

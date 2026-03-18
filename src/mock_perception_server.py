#!/usr/bin/env python3
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
        self.get_logger().info(f"Received perception request for task '{task_name}'.")

        result = Perception.Result()

        if task_name == "subdoor":
            result.success = True
            result.message = "Returned 4 mock subdoor poses"
            result.poses = self.mock_subdoor_poses()
            goal_handle.succeed()
            return result

        if task_name == "car_objects":
            result.success = True
            result.message = "Returned 2 mock car object pos"
            result.poses = self.mock_car_object_poses()
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

    def mock_car_object_poses(self):
        return [

            self.make_pose_stamped(self.base_frame, 0.75, 0.348875, 0.433091),
            self.make_pose_stamped(self.base_frame, 0.75, 0.000823, 0.426174),
        ]

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

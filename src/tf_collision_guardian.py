#!/usr/bin/env python3

import math

import rclpy
from rclpy.duration import Duration
from rclpy.node import Node
from std_msgs.msg import Bool
from tf2_ros import Buffer, TransformListener
from visualization_msgs.msg import Marker, MarkerArray


class TfCollisionGuardian(Node):
    def __init__(self):
        super().__init__("tf_collision_guardian")

        self.declare_parameter("base_frame", "eddie_base_link")
        self.declare_parameter("frame_filter", "right_arm")
        self.declare_parameter("check_period", 0.2)
        self.declare_parameter("base_radius", 0.38)
        self.declare_parameter("base_z_min", -0.10)
        self.declare_parameter("base_z_max", 0.2)
        self.declare_parameter("upper_radius", 0.2)
        self.declare_parameter("upper_z_min", 0.19)
        self.declare_parameter("upper_z_max", 0.68)
        self.declare_parameter("upper_x_offset", -0.15)
        self.declare_parameter("upper_y_offset", 0.0)

        self.base_frame = self.get_parameter("base_frame").value
        self.frame_filter = self.get_parameter("frame_filter").value
        self.check_period = float(self.get_parameter("check_period").value)
        self.base_radius = float(self.get_parameter("base_radius").value)
        self.base_z_min = float(self.get_parameter("base_z_min").value)
        self.base_z_max = float(self.get_parameter("base_z_max").value)
        self.upper_radius = float(self.get_parameter("upper_radius").value)
        self.upper_z_min = float(self.get_parameter("upper_z_min").value)
        self.upper_z_max = float(self.get_parameter("upper_z_max").value)
        self.upper_x_offset = float(self.get_parameter("upper_x_offset").value)
        self.upper_y_offset = float(self.get_parameter("upper_y_offset").value)

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.safety_pub = self.create_publisher(Bool, "/robot_safety/status", 10)
        self.marker_pub = self.create_publisher(MarkerArray, "/robot_safety/torso_zones", 10)
        self.last_collision_frames = set()

        self.get_logger().info(
            "TF collision guardian ready. "
            f"Monitoring TF frames containing '{self.frame_filter}' against torso cylinders."
        )
        self.publish_markers()
        self.create_timer(self.check_period, self.check_collision)

    def get_arm_frames(self) -> list[str]:
        frames_yaml = self.tf_buffer.all_frames_as_yaml()
        frames = []
        excluded_frames = {"eddie_right_arm_attachment_link", "eddie_right_arm_base_link"}
        for line in frames_yaml.splitlines():
            if not line or line.startswith(" "):
                continue
            if ":" not in line:
                continue
            frame = line.split(":", 1)[0].strip().strip('"').strip("'")
            if self.frame_filter in frame and frame != self.base_frame and frame not in excluded_frames:
                frames.append(frame)
        return sorted(set(frames))

    def point_in_cylinder(self, x: float, y: float, z: float, center_x: float, center_y: float, radius: float, z_min: float, z_max: float) -> bool:
        return z_min <= z <= z_max and math.hypot(x - center_x, y - center_y) <= radius

    def point_in_box(self, x: float, y: float, z: float, size_x: float, size_y: float, z_min: float, z_max: float) -> bool:
        return z_min <= z <= z_max and abs(x) <= size_x / 2.0 and abs(y) <= size_y / 2.0

    def make_cylinder_marker(
        self, marker_id: int, ns: str, center_x: float, center_y: float, radius: float, z_min: float, z_max: float, rgba: tuple[float, float, float, float]
    ) -> Marker:
        marker = Marker()
        marker.header.frame_id = self.base_frame
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = ns
        marker.id = marker_id
        marker.type = Marker.CYLINDER
        marker.action = Marker.ADD
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = center_x
        marker.pose.position.y = center_y
        marker.pose.position.z = (z_min + z_max) / 2.0
        marker.scale.x = radius * 2.0
        marker.scale.y = radius * 2.0
        marker.scale.z = z_max - z_min
        marker.color.r, marker.color.g, marker.color.b, marker.color.a = rgba
        return marker

    def make_box_marker(
        self, marker_id: int, ns: str, size_x: float, size_y: float, z_min: float, z_max: float, rgba: tuple[float, float, float, float]
    ) -> Marker:
        marker = Marker()
        marker.header.frame_id = self.base_frame
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = ns
        marker.id = marker_id
        marker.type = Marker.CUBE
        marker.action = Marker.ADD
        marker.pose.orientation.w = 1.0
        marker.pose.position.z = (z_min + z_max) / 2.0
        marker.scale.x = size_x
        marker.scale.y = size_y
        marker.scale.z = z_max - z_min
        marker.color.r, marker.color.g, marker.color.b, marker.color.a = rgba
        return marker

    def publish_markers(self):
        markers = MarkerArray()
        markers.markers.append(
            self.make_box_marker(
                0, "torso_zones", self.base_radius * 2.0, self.base_radius * 2.0, self.base_z_min, self.base_z_max, (1.0, 0.2, 0.2, 0.25)
            )
        )
        markers.markers.append(
            self.make_cylinder_marker(1, "torso_zones", self.upper_x_offset, self.upper_y_offset, self.upper_radius, self.upper_z_min, self.upper_z_max, (1.0, 0.8, 0.2, 0.25))
        )
        self.marker_pub.publish(markers)

    def check_collision(self):
        self.publish_markers()
        collision_frames = []
        for frame in self.get_arm_frames():
            try:
                tf = self.tf_buffer.lookup_transform(
                    self.base_frame, frame, rclpy.time.Time(), timeout=Duration(seconds=0.1)
                )
            except Exception:
                continue

            x = tf.transform.translation.x
            y = tf.transform.translation.y
            z = tf.transform.translation.z
            in_base = self.point_in_box(x, y, z, self.base_radius * 2.0, self.base_radius * 2.0, self.base_z_min, self.base_z_max)
            in_upper = self.point_in_cylinder(x, y, z, self.upper_x_offset, self.upper_y_offset, self.upper_radius, self.upper_z_min, self.upper_z_max)
            if in_base or in_upper:
                collision_frames.append(frame)

        is_safe = not collision_frames
        self.safety_pub.publish(Bool(data=is_safe))

        current_collision_frames = set(collision_frames)
        if current_collision_frames and current_collision_frames != self.last_collision_frames:
            frames = ", ".join(sorted(current_collision_frames))
            self.get_logger().error(f"COLLISION DETECTED! Frames inside torso safety zones: {frames}")
        elif not current_collision_frames and self.last_collision_frames:
            self.get_logger().info("Collision zone cleared.")
        self.last_collision_frames = current_collision_frames


def main(args=None):
    rclpy.init(args=args)
    node = TfCollisionGuardian()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

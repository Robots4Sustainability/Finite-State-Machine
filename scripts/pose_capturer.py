#!/usr/bin/env python3
import copy
import json
import threading
from pathlib import Path

import rclpy
from geometry_msgs.msg import Pose
from interactive_markers.interactive_marker_server import InteractiveMarkerServer
from interactive_markers.menu_handler import MenuHandler
from rclpy.action import ActionClient
from rclpy.node import Node
from tf2_geometry_msgs import do_transform_pose
from tf2_ros import Buffer, TransformListener
from visualization_msgs.msg import InteractiveMarker
from visualization_msgs.msg import InteractiveMarkerControl
from visualization_msgs.msg import InteractiveMarkerFeedback
from visualization_msgs.msg import Marker

from eddie_ros.action import ArmControl


class PoseCapturer(Node):
    def __init__(self):
        super().__init__("pose_capturer")

        self.declare_parameter("base_frame", "eddie_base_link")
        self.declare_parameter("camera_frame", "eddie_right_arm_camera_link")
        self.declare_parameter("record_frame", "eddie_right_arm_robotiq_85_grasp_link")
        self.declare_parameter("arm_action_server", "right_arm/arm_control")
        self.declare_parameter("marker_name", "pose_capturer_marker")
        self.declare_parameter("marker_scale", 0.18)

        script_path = Path(__file__).resolve()
        workspace_root = next(
            (parent.parent for parent in script_path.parents if parent.name == "install"),
            script_path.parents[3],
        )
        default_pose_store_path = workspace_root / "src" / "FSM" / "src" / "named_poses.json"

        self.declare_parameter(
        "pose_store_path",
            str(default_pose_store_path),
        )

        self.base_frame = self.get_parameter("base_frame").value
        self.camera_frame = self.get_parameter("camera_frame").value
        self.record_frame = self.get_parameter("record_frame").value
        self.arm_action_server = self.get_parameter("arm_action_server").value
        self.marker_name = self.get_parameter("marker_name").value
        self.marker_scale = float(self.get_parameter("marker_scale").value)
        self.pose_store_path = Path(self.get_parameter("pose_store_path").value).expanduser()

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.arm_client = ActionClient(self, ArmControl, self.arm_action_server)
        self.marker_server = InteractiveMarkerServer(self, "pose_capturer_marker_server")

        self.menu_handler = MenuHandler()
        self.print_current_entry = self.menu_handler.insert(
            "Print current robot pose", callback=self.on_menu_feedback
        )
        self.print_marker_entry = self.menu_handler.insert(
            "Print marker pose", callback=self.on_menu_feedback
        )
        self.sync_marker_entry = self.menu_handler.insert(
            "Sync marker to current robot pose", callback=self.on_menu_feedback
        )

        self.marker_initialized = False
        self.command_in_flight = False
        self.last_marker_pose = None

        self.init_timer = self.create_timer(0.5, self.try_initialize_marker)
        self.input_thread = threading.Thread(target=self.input_loop, daemon=True)
        self.input_thread.start()

        self.get_logger().info("Pose capturer ready.")
        self.get_logger().info(
            "Open RViz, add an InteractiveMarkers display, and subscribe to "
            "/pose_capturer_marker_server/update."
        )
        self.get_logger().info(
            "Drag the 6-DoF marker. Releasing the mouse sends the arm to that pose."
        )
        self.get_logger().info(
            "Right-click the marker to print the current robot pose or the marker pose."
        )
        self.get_logger().info(
            "Press 'b' to print the current pose in base frame or 'c' in camera frame."
        )
        self.get_logger().info(
            "Press 'h' to save home_pose, 't' to save table_drop_pose, "
            "'s' to save screwdriver_pose."
        )
        self.get_logger().info(
            f"Named poses will be written to: {self.pose_store_path}"
        )

    def try_initialize_marker(self):
        if self.marker_initialized:
            return

        pose = self.lookup_global_pose()
        if pose is None:
            return

        self.last_marker_pose = copy.deepcopy(pose)
        self.insert_marker(pose)
        self.marker_initialized = True
        self.init_timer.cancel()
        self.get_logger().info("Interactive marker initialized at current robot pose.")

    def lookup_global_pose(self):
        try:
            transform = self.tf_buffer.lookup_transform(
                self.base_frame,
                self.record_frame,
                rclpy.time.Time(),
            )
        except Exception as e:
            self.get_logger().debug(f"Waiting for TF {self.base_frame} <- {self.record_frame}: {e}")
            return None

        pose = Pose()
        pose.position.x = transform.transform.translation.x
        pose.position.y = transform.transform.translation.y
        pose.position.z = transform.transform.translation.z
        pose.orientation = transform.transform.rotation
        return pose

    def lookup_pose_in_frame(self, target_frame):
        try:
            transform = self.tf_buffer.lookup_transform(
                target_frame,
                self.record_frame,
                rclpy.time.Time(),
            )
        except Exception as e:
            self.get_logger().warn(
                f"Could not read current pose in {target_frame} from TF: {e}"
            )
            return None

        pose = Pose()
        pose.position.x = transform.transform.translation.x
        pose.position.y = transform.transform.translation.y
        pose.position.z = transform.transform.translation.z
        pose.orientation = transform.transform.rotation
        return pose

    def print_pose(self, pose, label):
        print("")
        print(f"# {label}")
        print(f"x: {pose.position.x:.6f}")
        print(f"y: {pose.position.y:.6f}")
        print(f"z: {pose.position.z:.6f}")
        print(f"qx: {pose.orientation.x:.6f}")
        print(f"qy: {pose.orientation.y:.6f}")
        print(f"qz: {pose.orientation.z:.6f}")
        print(f"qw: {pose.orientation.w:.6f}")
        print("")

    def pose_to_dict(self, pose):
        return {
            "frame_id": self.base_frame,
            "position": {
                "x": pose.position.x,
                "y": pose.position.y,
                "z": pose.position.z,
            },
            "orientation": {
                "x": pose.orientation.x,
                "y": pose.orientation.y,
                "z": pose.orientation.z,
                "w": pose.orientation.w,
            },
        }

    def save_named_pose(self, key):
        pose = self.lookup_pose_in_frame(self.base_frame)
        if pose is None:
            self.get_logger().warn(f"Could not capture pose for key '{key}'.")
            return

        self.print_pose(pose, f"{key} in {self.base_frame}")

        data = {}
        if self.pose_store_path.exists():
            try:
                data = json.loads(self.pose_store_path.read_text())
            except Exception as exc:
                self.get_logger().warn(
                    f"Could not parse existing pose store. Overwriting it: {exc}"
                )
                data = {}

        data[key] = self.pose_to_dict(pose)
        self.pose_store_path.parent.mkdir(parents=True, exist_ok=True)
        self.pose_store_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        self.get_logger().info(f"Saved '{key}' to {self.pose_store_path}")

    def make_box_control(self):
        control = InteractiveMarkerControl()
        control.always_visible = True

        marker = Marker()
        marker.type = Marker.CUBE
        marker.scale.x = 0.05
        marker.scale.y = 0.05
        marker.scale.z = 0.05
        marker.color.r = 0.1
        marker.color.g = 0.7
        marker.color.b = 0.9
        marker.color.a = 0.85

        control.markers.append(marker)
        return control

    def make_axis_control(self, name, orientation, interaction_mode):
        control = InteractiveMarkerControl()
        control.name = name
        control.orientation.w = orientation[0]
        control.orientation.x = orientation[1]
        control.orientation.y = orientation[2]
        control.orientation.z = orientation[3]
        control.interaction_mode = interaction_mode
        return control

    def build_marker(self, pose):
        marker = InteractiveMarker()
        marker.header.frame_id = self.base_frame
        marker.name = self.marker_name
        marker.description = "Pose Capturer"
        marker.scale = self.marker_scale
        marker.pose = pose

        marker.controls.append(self.make_box_control())

        # X axis controls
        marker.controls.append(
            self.make_axis_control("rotate_x", (1.0, 1.0, 0.0, 0.0), InteractiveMarkerControl.ROTATE_AXIS)
        )
        marker.controls.append(
            self.make_axis_control("move_x", (1.0, 1.0, 0.0, 0.0), InteractiveMarkerControl.MOVE_AXIS)
        )
        # Y axis controls
        marker.controls.append(
            self.make_axis_control("rotate_y", (1.0, 0.0, 1.0, 0.0), InteractiveMarkerControl.ROTATE_AXIS)
        )
        marker.controls.append(
            self.make_axis_control("move_y", (1.0, 0.0, 1.0, 0.0), InteractiveMarkerControl.MOVE_AXIS)
        )
        # Z axis controls
        marker.controls.append(
            self.make_axis_control("rotate_z", (1.0, 0.0, 0.0, 1.0), InteractiveMarkerControl.ROTATE_AXIS)
        )
        marker.controls.append(
            self.make_axis_control("move_z", (1.0, 0.0, 0.0, 1.0), InteractiveMarkerControl.MOVE_AXIS)
        )
        return marker

    def insert_marker(self, pose):
        marker = self.build_marker(pose)
        self.marker_server.insert(marker, feedback_callback=self.on_marker_feedback)
        self.menu_handler.apply(self.marker_server, self.marker_name)
        self.marker_server.applyChanges()

    def update_marker_pose(self, pose):
        self.last_marker_pose = copy.deepcopy(pose)
        self.marker_server.setPose(self.marker_name, pose)
        self.menu_handler.apply(self.marker_server, self.marker_name)
        self.marker_server.applyChanges()

    def on_menu_feedback(self, feedback):
        if feedback.menu_entry_id == self.print_current_entry:
            pose = self.lookup_global_pose()
            if pose is None:
                self.get_logger().warn("Could not read current robot pose from TF.")
                return
            self.print_pose(pose, f"{self.record_frame} in {self.base_frame}")
        elif feedback.menu_entry_id == self.print_marker_entry:
            if self.last_marker_pose is None:
                self.get_logger().warn("Marker pose is not initialized yet.")
                return
            self.print_pose(self.last_marker_pose, f"marker pose in {self.base_frame}")
        elif feedback.menu_entry_id == self.sync_marker_entry:
            pose = self.lookup_global_pose()
            if pose is None:
                self.get_logger().warn("Could not sync marker because TF is unavailable.")
                return
            self.update_marker_pose(pose)
            self.get_logger().info("Marker synced to current robot pose.")

    def input_loop(self):
        while rclpy.ok():
            try:
                cmd = input().strip().lower()
            except EOFError:
                break
            except Exception:
                continue

            if cmd == "b":
                pose = self.lookup_pose_in_frame(self.base_frame)
                if pose is not None:
                    self.print_pose(pose, f"{self.record_frame} in {self.base_frame}")
            elif cmd == "c":
                pose = self.lookup_pose_in_frame(self.camera_frame)
                if pose is not None:
                    self.print_pose(pose, f"{self.record_frame} in {self.camera_frame}")
            elif cmd == "h":
                self.save_named_pose("home_pose")
            elif cmd == "t":
                self.save_named_pose("table_drop_pose")
            elif cmd == "s":
                self.save_named_pose("screwdriver_pose")

    def on_marker_feedback(self, feedback):
        if feedback.event_type == InteractiveMarkerFeedback.POSE_UPDATE:
            self.last_marker_pose = copy.deepcopy(feedback.pose)
            return

        if feedback.event_type != InteractiveMarkerFeedback.MOUSE_UP:
            return

        if self.command_in_flight:
            self.get_logger().warn("Arm command already in flight. Ignoring marker release.")
            current_pose = self.lookup_global_pose()
            if current_pose is not None:
                self.update_marker_pose(current_pose)
            return

        self.last_marker_pose = copy.deepcopy(feedback.pose)
        relative_pose = self.global_pose_to_relative_pose(feedback.pose)
        if relative_pose is None:
            self.get_logger().error("Failed to convert marker pose into arm-relative target.")
            current_pose = self.lookup_global_pose()
            if current_pose is not None:
                self.update_marker_pose(current_pose)
            return

        self.send_relative_goal(relative_pose)

    def global_pose_to_relative_pose(self, global_pose):
        try:
            transform = self.tf_buffer.lookup_transform(
                self.record_frame,
                self.base_frame,
                rclpy.time.Time(),
            )
            return do_transform_pose(global_pose, transform)
        except Exception as e:
            self.get_logger().warn(f"Failed to transform marker pose to {self.record_frame}: {e}")
            return None

    def send_relative_goal(self, pose):
        if not self.arm_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error("Arm action server not available.")
            return

        goal = ArmControl.Goal()
        goal.target_pose = pose

        self.command_in_flight = True
        send_future = self.arm_client.send_goal_async(goal)
        send_future.add_done_callback(self.on_goal_response)

    def on_goal_response(self, future):
        try:
            goal_handle = future.result()
            if goal_handle is None or not goal_handle.accepted:
                self.command_in_flight = False
                self.get_logger().error("Arm goal rejected.")
                self.sync_marker_to_robot_pose()
                return

            result_future = goal_handle.get_result_async()
            result_future.add_done_callback(self.on_goal_result)
        except Exception as e:
            self.command_in_flight = False
            self.get_logger().error(f"Arm goal exception: {e}")
            self.sync_marker_to_robot_pose()

    def on_goal_result(self, future):
        self.command_in_flight = False
        try:
            result = future.result()
            if result is None:
                self.get_logger().error("Arm result missing.")
                self.sync_marker_to_robot_pose()
                return

            action_result = result.result
            if action_result.result_code != ArmControl.Result.SUCCESS:
                self.get_logger().error(f"Arm action failed: {action_result.result_message}")
                self.sync_marker_to_robot_pose()
                return

            self.get_logger().info("Arm action succeeded.")
            self.sync_marker_to_robot_pose()
        except Exception as e:
            self.get_logger().error(f"Arm result exception: {e}")
            self.sync_marker_to_robot_pose()

    def sync_marker_to_robot_pose(self):
        pose = self.lookup_global_pose()
        if pose is not None and self.marker_initialized:
            self.update_marker_pose(pose)


def main(args=None):
    rclpy.init(args=args)
    node = PoseCapturer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()

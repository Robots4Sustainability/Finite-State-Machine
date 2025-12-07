#!/usr/bin/env python3
import sys
import threading
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from geometry_msgs.msg import PoseStamped, Pose
from eddie_ros.action import ArmControl, GripperControl
from visualization_msgs.msg import Marker

# TF2 Imports
from tf2_ros import Buffer, TransformListener
import tf2_geometry_msgs # Imports the hook for buffer.transform

# FSM Imports
from coord_dsl.fsm import fsm_step
from coord_dsl.event_loop import reconfig_event_buffers, produce_event, consume_event
import os

# Helper to find the FSM module if it's not installed in the environment
current_dir = os.path.dirname(os.path.abspath(__file__))

# Check for source layout (src/pick_place.py -> ../include)
include_dir_src = os.path.join(current_dir, '../include')
# Check for install layout (lib/pkg_name/pick_place.py -> ../../include)
include_dir_install = os.path.join(current_dir, '../../include')

if os.path.exists(os.path.join(include_dir_src, 'fsm_pick_place.py')):
    if include_dir_src not in sys.path:
        sys.path.append(include_dir_src)
elif os.path.exists(os.path.join(include_dir_install, 'fsm_pick_place.py')):
    if include_dir_install not in sys.path:
        sys.path.append(include_dir_install)

from fsm_pick_place import create_fsm, StateID, EventID

class PickPlaceNode(Node):
    def __init__(self):
        super().__init__('pick_place_fsm_py')

        # FSM Setup
        self.fsm = create_fsm()
        self.user_data = {
            'target_pose': None,
            'action_dispatched': False,
            'last_state': StateID.S_IDLE,
            'place_pose': self.get_default_place_pose(),
            'home_pose': self.get_home_pose(),
            'detection_start_time': 0.0,
            'phase': 'PICK' # 'PICK' or 'PLACE'
        }

        # Parameters
        self.declare_parameter("ee_frame", "eddie_right_arm_robotiq_85_grasp_link")
        self.declare_parameter("base_frame", "eddie_base_link")
        
        self.ee_frame = self.get_parameter("ee_frame").get_parameter_value().string_value
        self.base_frame = self.get_parameter("base_frame").get_parameter_value().string_value

        # ROS Interfaces
        self.cb_group = ReentrantCallbackGroup()

        # TF Buffer
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Action Clients
        self.arm_client = ActionClient(self, ArmControl, 'right_arm/arm_control', callback_group=self.cb_group)
        self.gripper_client = ActionClient(self, GripperControl, 'right_arm/gripper_control', callback_group=self.cb_group)

        # Subscribers
        self.perception_sub = self.create_subscription(
            PoseStamped,
            '/object_pose',
            self.perception_callback,
            10,
            callback_group=self.cb_group
        )
        
        # Publishers
        self.marker_pub = self.create_publisher(Marker, '/visualization_marker', 10)

        # Timers
        self.fsm_timer = self.create_timer(0.1, self.fsm_loop, callback_group=self.cb_group) # 10Hz

        # User Input Thread
        self.input_thread = threading.Thread(target=self.input_loop, daemon=True)
        self.input_thread.start()

        self.get_logger().info("Pick & Place Python Node Ready. Waiting for 'Enter' to start...")

    def get_default_place_pose(self):
        # RELATIVE move for place
        p = Pose()
        p.position.x = 0.0
        p.position.y = -0.2
        p.position.z = 0.0
        # p.orientation.w = 1.0
        return p

    def get_home_pose(self):
        # ABSOLUTE move for home (Requires Action Server to support Absolute, 
        # but previously we saw it handled Relative for some goals. 
        # Let's assume HOME is absolute or we send a specific relative move to go up).
        # For safety in this specific context, let's make it a relative "Move Up" 
        p = Pose()
        p.position.x = 0.0
        p.position.y = 0.0
        p.position.z = 0.2 # Move up 20cm
        return p

    def publish_marker(self, pose_stamped):
        marker = Marker()
        marker.header = pose_stamped.header
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.scale.x = 0.05
        marker.scale.y = 0.05
        marker.scale.z = 0.05
        marker.color.a = 1.0
        marker.color.r = 0.0
        marker.color.g = 1.0
        marker.color.b = 1.0
        marker.pose = pose_stamped.pose
        self.marker_pub.publish(marker)

    def perception_callback(self, msg):
        # Only process pose if we are in the DETECTION state
        if self.fsm.current_state_index == StateID.S_POSE_DETECTION:
            try:
                self.publish_marker(msg)
                
                # Transform object pose from Camera Frame to End-Effector Frame
                target_pose_in_ee = self.tf_buffer.transform(msg, self.ee_frame, timeout=rclpy.duration.Duration(seconds=1.0))
                
                # Zero orientation for translation-only relative move
                target_pose_in_ee.pose.orientation.x = 0.0
                target_pose_in_ee.pose.orientation.y = 0.0
                target_pose_in_ee.pose.orientation.z = 0.0
                target_pose_in_ee.pose.orientation.w = 1.0

                self.get_logger().info(f"Object detected. Relative pose: {target_pose_in_ee.pose.position}")
                
                self.user_data['target_pose'] = target_pose_in_ee.pose
                produce_event(self.fsm.event_data, EventID.E_PERCEPTION_POSE)
                
            except Exception as e:
                self.get_logger().warn(f"TF Transform failed: {e}")

    def input_loop(self):
        while rclpy.ok():
            if self.fsm.current_state_index == StateID.S_IDLE:
                try:
                    input(">> Press Enter to START task...\n")
                    produce_event(self.fsm.event_data, EventID.E_START)
                    time.sleep(0.5) # Debounce
                except EOFError:
                    break
            else:
                time.sleep(0.5)

    def fsm_loop(self):
        # Check for exit
        if self.fsm.current_state_index == StateID.S_EXIT:
            self.get_logger().info("FSM Reached EXIT state. Shutting down.")
            # This raise will be caught by the loop or main to exit cleanly
            raise SystemExit

        # Log state changes
        if self.fsm.current_state_index != self.user_data['last_state']:
            state_name = StateID(self.fsm.current_state_index).name
            self.get_logger().info(f"State Changed to: {state_name}")
            
            self.user_data['last_state'] = self.fsm.current_state_index
            self.user_data['action_dispatched'] = False
            
            # State Entry Logic
            if self.fsm.current_state_index == StateID.S_POSE_DETECTION:
                self.user_data['detection_start_time'] = self.get_clock().now().nanoseconds / 1e9
                self.user_data['phase'] = 'PICK' # Reset phase
                self.get_logger().info("Listening for /object_pose for 6 seconds...")

        self.fsm_behavior()
        fsm_step(self.fsm)
        reconfig_event_buffers(self.fsm.event_data)

    def fsm_behavior(self):
        current_state = self.fsm.current_state_index
        ud = self.user_data

        # --- S_IDLE ---
        if current_state == StateID.S_IDLE:
            pass

        # --- S_POSE_DETECTION ---
        elif current_state == StateID.S_POSE_DETECTION:
            current_time = self.get_clock().now().nanoseconds / 1e9
            if (current_time - ud['detection_start_time']) > 6.0:
                self.get_logger().warn("Perception Timeout (6s exceeded). Aborting...")
                produce_event(self.fsm.event_data, EventID.E_PERCEPTION_FAIL)

        # --- S_MOVE_ARM ---
        elif current_state == StateID.S_MOVE_ARM:
            if not ud['action_dispatched']:
                target = None
                success_event = None
                
                if ud['phase'] == 'PICK':
                    target = ud['target_pose']
                    success_event = EventID.E_PICK_MOVE_DONE
                    self.get_logger().info("Moving to PICK pose...")
                elif ud['phase'] == 'PLACE':
                    target = ud['place_pose']
                    success_event = EventID.E_PLACE_MOVE_DONE
                    self.get_logger().info("Moving to PLACE pose...")
                
                if target is None:
                    self.get_logger().error("Target pose is None!")
                    produce_event(self.fsm.event_data, EventID.E_ARM_MOVE_DONE_FAIL)
                else:
                    self.send_arm_goal(target, success_event, EventID.E_ARM_MOVE_DONE_FAIL)
                
                ud['action_dispatched'] = True

        # --- S_CLOSE_GRIPPER ---
        elif current_state == StateID.S_CLOSE_GRIPPER:
            if not ud['action_dispatched']:
                # Prepare for next phase
                ud['phase'] = 'PLACE'
                self.send_gripper_command(100.0, EventID.E_GRIPPER_CLOSE_DONE_OK, EventID.E_GRIPPER_CLOSE_DONE_FAIL)
                ud['action_dispatched'] = True

        # --- S_OPEN_GRIPPER ---
        elif current_state == StateID.S_OPEN_GRIPPER:
            if not ud['action_dispatched']:
                self.send_gripper_command(0.0, EventID.E_OPEN_DONE_OK, EventID.E_OPEN_DONE_FAIL)
                ud['action_dispatched'] = True

        # --- S_FINISHED ---
        elif current_state == StateID.S_FINISHED:
            if not ud['action_dispatched']:
                self.get_logger().info("Task Finished. Returning Home...")
                produce_event(self.fsm.event_data, EventID.E_GO_HOME)
                ud['action_dispatched'] = True

        # --- S_MOVE_ARM_HOME ---
        elif current_state == StateID.S_MOVE_ARM_HOME:
            if not ud['action_dispatched']:
                self.get_logger().info("Moving Home...")
                self.send_arm_goal(ud['home_pose'], EventID.E_HOME_DONE_OK, EventID.E_HOME_DONE_FAIL)
                ud['action_dispatched'] = True

    # --- Action Helpers ---

    def send_arm_goal(self, pose, success_evt, fail_evt):
        if not self.arm_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error("Arm action server not available!")
            produce_event(self.fsm.event_data, fail_evt)
            return

        goal = ArmControl.Goal()
        goal.target_pose = pose

        future = self.arm_client.send_goal_async(goal)
        future.add_done_callback(lambda fut: self.arm_goal_response(fut, success_evt, fail_evt))

    def arm_goal_response(self, future, success_evt, fail_evt):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().error("Arm goal rejected")
                produce_event(self.fsm.event_data, fail_evt)
                return

            res_future = goal_handle.get_result_async()
            res_future.add_done_callback(lambda fut: self.arm_result(fut, success_evt, fail_evt))
        except Exception as e:
            self.get_logger().error(f"Arm Goal Exception: {e}")
            produce_event(self.fsm.event_data, fail_evt)

    def arm_result(self, future, success_evt, fail_evt):
        try:
            result = future.result().result
            if result.success:
                self.get_logger().info("Arm Action Succeeded")
                produce_event(self.fsm.event_data, success_evt)
            else:
                self.get_logger().error(f"Arm Action Failed: {result.message}")
                produce_event(self.fsm.event_data, fail_evt)
        except Exception as e:
            self.get_logger().error(f"Arm Result Exception: {e}")
            produce_event(self.fsm.event_data, fail_evt)

    def send_gripper_command(self, position, success_evt, fail_evt):
        if not self.gripper_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error("Gripper action server not available!")
            produce_event(self.fsm.event_data, fail_evt)
            return

        goal = GripperControl.Goal()
        goal.target_position = position
        goal.velocity = 20.0
        goal.force = 10.0

        future = self.gripper_client.send_goal_async(goal)
        future.add_done_callback(lambda fut: self.gripper_goal_response(fut, success_evt, fail_evt))

    def gripper_goal_response(self, future, success_evt, fail_evt):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().error("Gripper goal rejected")
                produce_event(self.fsm.event_data, fail_evt)
                return

            res_future = goal_handle.get_result_async()
            res_future.add_done_callback(lambda fut: self.gripper_result(fut, success_evt, fail_evt))
        except Exception as e:
            self.get_logger().error(f"Gripper Goal Exception: {e}")
            produce_event(self.fsm.event_data, fail_evt)

    def gripper_result(self, future, success_evt, fail_evt):
        try:
            result = future.result().result
            if result.success:
                self.get_logger().info("Gripper Action Succeeded")
                produce_event(self.fsm.event_data, success_evt)
            else:
                self.get_logger().error(f"Gripper Action Failed: {result.message}")
                produce_event(self.fsm.event_data, fail_evt)
        except Exception as e:
            self.get_logger().error(f"Gripper Result Exception: {e}")
            produce_event(self.fsm.event_data, fail_evt)


def main(args=None):
    rclpy.init(args=args)
    node = PickPlaceNode()
    try:
        rclpy.spin(node)
    except SystemExit:
        node.get_logger().info("Node stopped via SystemExit")
    except KeyboardInterrupt:
        node.get_logger().info("Node stopped via KeyboardInterrupt")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

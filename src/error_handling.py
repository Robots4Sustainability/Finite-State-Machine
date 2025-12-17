#!/usr/bin/env python3
"""
Listens to /joint_states and waits for a service call that tells it
the gripper-action is finished; only then is the encoder value latched.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool, Float32
from pick_place_fsm.srv import CaptureReference

class GripperSlipDetector(Node):
    def __init__(self):
        super().__init__('gripper_slip_detector')

        # ---------------- parameters ----------------
        self.declare_parameter('drift_thresh_percent', 5.0)   # %
        self.declare_parameter('min_cmd_for_check',   10.0)   # %
        self.declare_parameter('joint_name',
                               'eddie_right_arm_robotiq_85_left_knuckle_joint')
        # self.declare_parameter('cmd_topic', '/right_arm/gripper_pos_cmd')
        self.declare_parameter('slip_topic', '/gripper_slip')

        self.thresh = self.get_parameter('drift_thresh_percent').value / 100.0
        self.min_cmd = self.get_parameter('min_cmd_for_check').value
        self.joint_name = self.get_parameter('joint_name').value

        # ---------------- state ----------------
        self.msr_percent = None
        self.ref_percent = None          # will be set only after service call
        self.cmd_percent = None
        # ---------------- publishers ----------------
        self.slip_pub = self.create_publisher(Bool,
                                              self.get_parameter('slip_topic').value,
                                              10)

        # ---- subscribers ----
        self.create_subscription(JointState, '/joint_states',
                               self.on_joint_states, 10)
        self.create_subscription(Float32, '/right_arm/gripper_pos_cmd',
                               self.on_cmd, 10)

        # ---- NEW service ----
        self.srv = self.create_service(CaptureReference,
                                      '/gripper_slip/capture_reference',
                                      self.capture_reference_callback)

        self.get_logger().info('Slip detector ready (reference captured on service call).')

    # ---------------- callbacks ----------------
    def on_joint_states(self, msg: JointState):
        try:
            idx = msg.name.index(self.joint_name)
            rad = msg.position[idx]
            self.msr_percent = rad * 100.0 / 0.8  # 0-100 %
        except ValueError:
            # joint not in message – ignore
            pass

    def on_cmd(self, msg: Float32):
        self.cmd_percent = msg.data  # 0-100 %
        
    # ------------ NEW service ------------
    def capture_reference_callback(self, request, response):
        if self.msr_percent is None:
            self.get_logger().warn('No joint data yet, cannot capture reference.')
            response.success = False
            return response

        self.ref_percent = self.msr_percent
        self.get_logger().info(f'Reference captured: {self.ref_percent:.1f} %')
        response.success = True
        return response


    # ------------ main loop ------------
    def publish_slip(self):
        if self.ref_percent is None or self.msr_percent is None:
            return  # no reference yet → silent

        ref = self.ref_percent
        msr = self.msr_percent

        # ignore tiny commands (optional)
        if self.cmd_percent is not None and self.cmd_percent < self.min_cmd:
            slip = False
        else:
            drift = abs(msr - ref) / max(ref, 1e-3)
            slip = drift > self.thresh

        self.slip_pub.publish(Bool(data=slip))


def main():
    rclpy.init()
    node = GripperSlipDetector()
    # run at 20 Hz
    import threading
    def spin():
        while rclpy.ok():
            node.publish_slip()
            rclpy.spin_once(node, timeout_sec=0.05)
    threading.Thread(target=spin, daemon=True).start()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
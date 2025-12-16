#!/usr/bin/env python3
"""
Stand-alone gripper-slip detector (no C++ change required)
Listens to /joint_states and /right_arm/gripper_pos_cmd
Publishes /gripper_slip  (Bool)  when drift > threshold %
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool, Float32


class GripperSlipDetector(Node):
    def __init__(self):
        super().__init__('gripper_slip_detector')

        # ---------------- parameters ----------------
        self.declare_parameter('drift_thresh_percent', 5.0)   # %
        self.declare_parameter('min_cmd_for_check',   10.0)   # %
        self.declare_parameter('joint_name',
                               'eddie_right_arm_robotiq_85_left_knuckle_joint')
        self.declare_parameter('cmd_topic', '/right_arm/gripper_pos_cmd')
        self.declare_parameter('slip_topic', '/gripper_slip')

        self.thresh = self.get_parameter('drift_thresh_percent').value / 100.0
        self.min_cmd = self.get_parameter('min_cmd_for_check').value
        self.joint_name = self.get_parameter('joint_name').value

        # ---------------- state ----------------
        self.cmd_percent = None
        self.msr_percent = None

        # ---------------- publishers ----------------
        self.slip_pub = self.create_publisher(Bool,
                                              self.get_parameter('slip_topic').value,
                                              10)

        # ---------------- subscribers ----------------
        self.create_subscription(JointState,
                                 '/joint_states',
                                 self.on_joint_states,
                                 10)
        self.create_subscription(Float32,
                                 self.get_parameter('cmd_topic').value,
                                 self.on_cmd,
                                 10)

        self.get_logger().info(
            f'Slip detector ready: drift > {self.thresh*100:.1f} % of command '
            f'(ignored below {self.min_cmd:.1f} %)')

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

    # ---------------- main loop ----------------
    def publish_slip(self):
        if self.cmd_percent is None or self.msr_percent is None:
            return

        cmd = self.cmd_percent
        msr = self.msr_percent

        # ignore very small commands (releasing)
        if cmd < self.min_cmd:
            slip = False
        else:
            # relative drift: |measured - commanded| / commanded
            drift = abs(msr - cmd) / max(cmd, 1e-3)
            slip = drift > self.thresh

        # publish Bool
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
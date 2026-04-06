#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool


class GripperSlipDetector(Node):
    def __init__(self):
        super().__init__("gripper_slip_detector")

        self.declare_parameter(
            "joint_name",
            "eddie_right_arm_robotiq_85_left_knuckle_joint",
        )
        self.declare_parameter("joint_states_topic", "/joint_states")
        self.declare_parameter("slip_topic", "/gripper_slip")
        self.declare_parameter("abort_topic", "/door_disassemble/abort")

        # Slip threshold after reference is latched - I need to reconfirm this again
        self.declare_parameter("drift_thresh_percent", 1.0)

        # Ignore tiny values gripper considered open / not grasping
        self.declare_parameter("closed_min_percent", 2.0)

        # Number of settled cycles required before latching reference
        self.declare_parameter("stable_cycles_required", 8)

        # How close the measured value must be to one of the known object values
        self.declare_parameter("object_match_tolerance_percent", 1.0)

        # How little the measured value must change between samples
        # to be considered "settled"
        self.declare_parameter("settle_delta_percent", 0.2)

        self.declare_parameter("monitor_rate_hz", 20.0)

        self.joint_name = self.get_parameter("joint_name").value
        self.joint_states_topic = self.get_parameter("joint_states_topic").value
        self.slip_topic = self.get_parameter("slip_topic").value
        self.abort_topic = self.get_parameter("abort_topic").value

        self.drift_thresh = float(self.get_parameter("drift_thresh_percent").value)
        self.closed_min = float(self.get_parameter("closed_min_percent").value)
        self.stable_cycles_required = int(
            self.get_parameter("stable_cycles_required").value
        )
        self.object_match_tolerance = float(
            self.get_parameter("object_match_tolerance_percent").value
        )
        self.settle_delta = float(
            self.get_parameter("settle_delta_percent").value
        )
        self.monitor_rate_hz = float(self.get_parameter("monitor_rate_hz").value)

        # Current door_disassemble.py close commands:
        # unit = 0.08, motor_grip -> 0.45, speaker -> 0.47
        # We track them here in percent form.
        self.object_close_targets = {
            "unit": 8.0,
            "motor_grip": 45.0,
            "speaker": 47.0,
        }

        self.msr_percent = None
        self.prev_msr_percent = None
        self.ref_percent = None
        self.active_object = None
        self.candidate_object = None
        self.candidate_count = 0
        self.slip_latched = False
        self.last_reported_slip = False

        self.slip_pub = self.create_publisher(Bool, self.slip_topic, 10)
        self.abort_pub = self.create_publisher(Bool, self.abort_topic, 10)

        self.create_subscription(
            JointState,
            self.joint_states_topic,
            self.on_joint_states,
            10,
        )

        timer_period = 1.0 / max(self.monitor_rate_hz, 1.0)
        self.timer = self.create_timer(timer_period, self.monitor)

        self.get_logger().info("Gripper slip detector started.")
        self.get_logger().info(f"Listening to joint states on: {self.joint_states_topic}")
        self.get_logger().info(f"Using gripper joint: {self.joint_name}")
        self.get_logger().info(f"Slip topic: {self.slip_topic}")
        self.get_logger().info(f"Abort topic: {self.abort_topic}")
        self.get_logger().info(
            f"Targets: {self.object_close_targets}, "
            f"drift_thresh={self.drift_thresh:.2f}%, "
            f"match_tol={self.object_match_tolerance:.2f}%, "
            f"settle_delta={self.settle_delta:.2f}%"
        )

    def on_joint_states(self, msg: JointState):
        try:
            idx = msg.name.index(self.joint_name)
        except ValueError:
            return

        joint_rad = msg.position[idx]

        new_percent = joint_rad * 100.0 / 0.8

        self.prev_msr_percent = self.msr_percent
        self.msr_percent = new_percent

    def infer_object_from_measurement(self, msr_percent: float):
        best_name = None
        best_error = float("inf")

        for name, target in self.object_close_targets.items():
            err = abs(msr_percent - target)
            if err < best_error:
                best_error = err
                best_name = name

        if best_error <= self.object_match_tolerance:
            return best_name

        return None

    def reset_grasp_state(self):
        if self.active_object is not None or self.ref_percent is not None:
            self.get_logger().info("Gripper opened or grasp reset. Clearing reference.")

        self.prev_msr_percent = None
        self.ref_percent = None
        self.active_object = None
        self.candidate_object = None
        self.candidate_count = 0
        self.slip_latched = False

    def publish_slip_state(self, slip: bool):
        self.last_reported_slip = slip
        self.slip_pub.publish(Bool(data=slip))

    def trigger_abort(self, reason: str):
        self.get_logger().error(reason)
        self.publish_slip_state(True)
        self.abort_pub.publish(Bool(data=True))
        self.slip_latched = True

    def try_capture_reference(self, msr_percent: float):
        detected_object = self.infer_object_from_measurement(msr_percent)

        if detected_object is None:
            self.candidate_object = None
            self.candidate_count = 0
            return

        if self.prev_msr_percent is None:
            self.candidate_object = None
            self.candidate_count = 0
            return

        delta = abs(msr_percent - self.prev_msr_percent)

        # Do not latch while the gripper is still moving noticeably.
        if delta > self.settle_delta:
            if detected_object != self.candidate_object:
                self.candidate_object = detected_object
            self.candidate_count = 0
            return

        if detected_object != self.candidate_object:
            self.candidate_object = detected_object
            self.candidate_count = 1
            return

        self.candidate_count += 1

        if self.candidate_count >= self.stable_cycles_required:
            self.active_object = detected_object
            self.ref_percent = msr_percent
            self.get_logger().info(
                f"Captured reference for object '{self.active_object}' "
                f"at gripper value {self.ref_percent:.2f}%"
            )

    def monitor(self):
        if self.msr_percent is None:
            return

        msr = self.msr_percent

        # If gripper is basically open, clear everything.
        if msr < self.closed_min:
            self.reset_grasp_state()
            self.publish_slip_state(False)
            return

        # No reference yet: keep waiting until close value is both
        # near an object target and settled.
        if self.ref_percent is None or self.active_object is None:
            self.try_capture_reference(msr)
            self.publish_slip_state(False)
            return

        # Once slip is latched, keep reporting it until reset/open.
        if self.slip_latched:
            self.publish_slip_state(True)
            return

        drift = abs(msr - self.ref_percent)

        if drift > self.drift_thresh:
            self.trigger_abort(
                f"Slip detected for '{self.active_object}': "
                f"reference={self.ref_percent:.2f}% current={msr:.2f}% "
                f"drift={drift:.2f}% threshold={self.drift_thresh:.2f}%"
            )
        else:
            self.publish_slip_state(False)


def main(args=None):
    rclpy.init(args=args)
    node = GripperSlipDetector()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
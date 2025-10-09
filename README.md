# Pick and Place FSM

This ROS2 package implements a Finite-State Machine (FSM) for a pick-and-place task. It is designed to work with an "Eddie" robotic arm but includes mock servers for testing without the actual hardware.

## Functionality

The core of this package is the `pick_place_fsm_mock` node, which implements the following states:

-   **IDLE**: The FSM is waiting for a target pose.
-   **MOVE_TO_APPROACH**: Move the arm to an approach position near the object.
-   **MOVE_TO_GRASP**: Move the arm to the final grasping position.
-   **CLOSE_GRIPPER**: Close the gripper to grasp the object.
-   **MOVE_TO_PLACE**: Move the arm to a pre-defined placing position.
-   **OPEN_GRIPPER**: Open the gripper to release the object.
-   **FINISHED**: The sequence is complete, and the FSM returns to IDLE.
-   **ABORT**: The sequence was aborted due to an error.

The FSM is triggered by publishing a `geometry_msgs/msg/PoseStamped` message to the `/perception/target_pose` topic.

## ROS Topics and Actions

### Subscriptions

-   `/perception/target_pose` (`geometry_msgs/msg/PoseStamped`): The FSM subscribes to this topic to receive the target pose for the pick-and-place task.

### Actions

-   `right_arm/arm_control` (`eddie_ros/action/ArmControl`): The action server for controlling the arm movement.
-   `right_arm/gripper_control` (`eddie_ros/action/GripperControl`): The action server for controlling the gripper.


## Nodes

-   `pick_place_fsm_mock`: The main FSM client node.
-   `mock_servers_only`: A node that provides mock action servers for the arm and gripper, for testing purposes(without robot).

## Dependencies

This package depends on the following ROS2 packages:

-   `rclcpp`
-   `rclcpp_action`
-   `geometry_msgs`
-   `eddie_ros`: This is a custom package providing action definitions. You must have this package in your workspace and built before building this package.

## Building

To build this package, use `colcon`:

```bash
colcon build
```
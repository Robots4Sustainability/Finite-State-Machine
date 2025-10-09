# How to Run

This document provides instructions on how to run the Pick and Place FSM project.

## Prerequisites

-   A working ROS2 Jazzy installation.
-   The `eddie_ros` package must be in your workspace and built.
-   You have built the `pick_place_fsm` package.

## Running the FSM

You will need three terminals.

### 1. Source the Workspace

In each terminal, source your ROS2 workspace:

```bash
source install/setup.bash
```

### 2. Run the Mock Servers (Terminal 1)

This will start the mock action servers for the arm and gripper.

```bash
ros2 run pick_place_fsm mock_servers_only
```
**OR**
```bash
ros2 run eddie_ros eddie_ros_interface_test --ros-args -p arm_select:=right
```

### 3. Run the FSM (Terminal 2)

This will start the FSM client, which will wait for a perception message.

```bash
ros2 run pick_place_fsm pick_place_fsm_mock
```

### 4. Publish Perception Data (Terminal 3)

This will trigger the FSM to start the pick and place sequence. This example publishes a pose at (0.5, 0.5, 0.5).

```bash
ros2 topic pub --once /perception/target_pose geometry_msgs/msg/PoseStamped   "{header: {frame_id: camera}, pose: {position: {x: 0.5, y: 0.0, z: 0.2}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}"
```

#### You should then be able to see state transitions from FSM terminal

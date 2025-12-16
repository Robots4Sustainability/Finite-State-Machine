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

### 2. Run the Eddie interface (Terminal 1)
  #### 2.1 **Ensure Zenoh is running.**
  #### 2.2 refer docs from [Eddie-Ros Docs](https://github.com/Robots4Sustainability/eddie-ros/tree/dev)

### 3. Run the FSM (Terminal 2)

This will start the FSM client, which will wait for a perception message.

```bash
ros2 run pick_place_fsm pick_place
```
Press Enter key once perception node is ready.

### 4. Publish Perception Data (Terminal 3)

This will trigger the FSM to start the pick and place sequence..


Refer docs from [Perception docs](https://github.com/Robots4Sustainability/perception)

**OR**

```bash
ros2 topic pub --once /object_pose geometry_msgs/msg/PoseStamped "{header: {frame_id: 'eddie_right_arm_camera_link'}, pose: {position: {x: 0.0, y: 0.0, z: 0.4}, orientation: {}}}"

```

#### You should then be able to see state transitions from FSM terminal

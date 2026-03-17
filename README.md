# Finite State Machine Package

# Door Disassemble FSM

This document covers the `door_disassemble` workflow and the helper nodes used with it.

## Main Files

- [door_disassemble.py](src/door_disassemble.py)
  Python FSM node for the door workflow.
- [door_disassemble.fsm](include/door_disassemble.fsm)
  Source FSM definition.
- [fsm_door_disassemble.py](include/fsm_door_disassemble.py)
  Generated Python FSM datastructures.
- [mock_perception_server.py](src/mock_perception_server.py)
  Mock perception action server used during testing.
- [Perception.action](action/Perception.action)
  Mock Perception action definition used by the FSM.

## Flow

The `door_disassemble` FSM currently runs this loop:

1. Initialize.
2. Move to the default view pose.
3. Request subdoor poses from perception.
4. Request car object poses from perception.
5. Execute raster scan for screw detection (Needs raster scanner node to be running).
6. Return to the default home/view pose.
7. Select the next object.
8. Move to the object pre-pick pose.
9. Advance to the object pick pose.
10. Close gripper.
11. Retreat with object.
12. Move to the table drop pose.
13. Open gripper.
14. Return to home/view pose.
15. Repeat until no objects remain.

## Mock Perception

`mock_perception_server` provides a mock action server on `perception`.

Supported task names:
- `subdoor`
- `car_objects`

Run it with:

```bash
ros2 run pick_place_fsm mock_perception_server
```

Example calls:

```bash
ros2 action send_goal /perception pick_place_fsm/action/Perception "{task_name: subdoor}"
ros2 action send_goal /perception pick_place_fsm/action/Perception "{task_name: car_objects}"
```

## Quick Start

```bash
colcon build
source /opt/ros/jazzy/setup.bash
source ~/r4s/install/setup.bash
```

Run the door workflow:
Preferrably run each command in a new terminal

```bash
ros2 run rmw_zenoh_cpp rmw_zenohd
ros2 launch eddie_ros eddie.launch.py use_sim:=true arm_select:=right
ros2 launch eddie_ros rviz.launch.py
ros2 run cartesian_planner spline_planner
ros2 run pick_place_fsm mock_perception_server
ros2 run pick_place_fsm door_disassemble
```

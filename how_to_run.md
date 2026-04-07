# How To Run

This document covers the current **Door Disassemle** workflow in `r4s/src/Finite-State-Machine`.


## Prerequisites

- ROS 2 Jazzy is installed.
- The workspace contains and builds:
  - `pick_place_fsm`
  - `my_robot_interfaces`
  - `eddie_ros`
  - `cartesian_planner`
  - Ensure [`PyYAML`](https://pypi.org/project/PyYAML/) and [`coord-dsl`](https://github.com/secorolab/coord-dsl) are installed
- For real robot runs, the Eddie stack and TF tree must already be available.
- For real robot runs, perception must also already be running and exposing:
  - `/run_perception_pipeline`

## Build

From the workspace root:

```bash
cd ~/r4s
source /opt/ros/jazzy/setup.bash
colcon build
source ~/r4s/install/setup.bash
```

## Common sourcing

In every terminal used below:

```bash
cd ~/r4s
source /opt/ros/jazzy/setup.bash
source ~/r4s/install/setup.bash
```
## Control Panel
Start and stop FSM using the control panel
. Just run this in a new terminal and control everything using the launcher

```bash
ros2 run pick_place_fsm control_panel
```
This runs the main GUI launcher which you can use to run all the nodes.
More details on [control panel](https://github.com/Robots4Sustainability/Finite-State-Machine/wiki/Control-Panel)
### Alternativly you ran run each package/node in a different terminal, details below

## Named poses

Named poses are stored in:

[`src/named_poses.json`](src/named_poses.json)

Currently used keys include:

- `home_pose`
- `table_drop_pose`
- `screwdriver_pose`
- `view_pose_unit`
- `view_pose_motor_grip`
- `view_pose_speaker`

## Capture named poses

Run:

```bash
ros2 run pick_place_fsm pose_capturer
```

Useful keys inside `pose_capturer`:

- `h` saves `home_pose`
- `t` saves `table_drop_pose`
- `s` saves `screwdriver_pose`
- `u` saves `view_pose_unit`
- `m` saves `view_pose_motor_grip`
- `p` saves `view_pose_speaker`

### Note : These are already saved , do not rerun until change is needed

## Local mock test for `door_disassemble` in simulation

This is the simplest end-to-end local test path.

Terminal 1: eddie robot simulation

```bash
ros2 launch eddie_ros eddie.launch.py use_sim:=true arm_select:=right show_rviz:=true
```


Terminal 2: mock perception

```bash
ros2 run pick_place_fsm mock_perception_server
```

Terminal 3: screwdriver helper

```bash
ros2 run pick_place_fsm screwdriver_pick
```

Terminal 4: raster scanner

```bash
ros2 run cartesian_planner raster_scanner
```

Terminal 5: FSM

```bash
ros2 run pick_place_fsm door_disassemble
```

Then press `Enter` in the FSM terminal to start.

Useful parameter overrides for local runs:

```bash
ros2 run pick_place_fsm door_disassemble --ros-args -p enable_raster_scan:=false -p screwdriver_probe:=true
```

## Real robot run for `door_disassemble`

Use separate terminals for the robot stack, perception stack, and FSM.

### Terminal 1: Eddie ROS

Bring up Eddie ROS by following the instructions in the Eddie ROS repository:

- `https://github.com/Robots4Sustainability/eddie-ros`

This must provide the robot interfaces and TF tree.

### Terminal 2: Perception

Bring up perception by following the perception wiki:

- `https://github.com/Robots4Sustainability/perception/wiki`

This must provide the perception action server:

- `/run_perception_pipeline`

### Terminal 3: Optional screwdriver helper

If you want the screwdriver routine enabled, run:

```bash
ros2 run pick_place_fsm screwdriver_pick
```

### Terminal 4: Raster scanner

If raster scan is part of the run, start the scanner node too.

```bash
ros2 run cartesian_planner raster_scanner
```

### Terminal 5: FSM

Then run the FSM:

```bash
ros2 run pick_place_fsm door_disassemble
```

At minimum, the following must already be available from Eddie ROS and perception:

- arm action server:
  - `right_arm/arm_control`
- force action server if you use it:
  - `right_arm/force_control`
- gripper action server:
  - simulation backend or Robotiq backend, depending on `src/common.py`
- TF frames such as:
  - `eddie_base_link`
  - `eddie_right_arm_camera_link`
  - `eddie_right_arm_robotiq_85_grasp_link`
- perception action server:
  - `/run_perception_pipeline`

Example with explicit parameters:

```bash
ros2 run pick_place_fsm door_disassemble --ros-args \
  -p enable_raster_scan:=false \
  -p screwdriver_probe:=true
```

## Standalone screwdriver routine

Run the helper node:

```bash
ros2 run pick_place_fsm screwdriver_pick
```

It exposes the service:

- `/screwdriver_pick/run`

You normally do not call it manually because `door_disassemble` calls it. If needed, inspect it with:

```bash
ros2 service type /screwdriver_pick/run
ros2 interface show pick_place_fsm/srv/RunScrewdriverRoutine
```

## Mock perception action check

List action servers:

```bash
ros2 action list
ros2 action info /run_perception_pipeline
```

Manual subdoor request:

```bash
ros2 action send_goal /run_perception_pipeline my_robot_interfaces/action/RunVision "{task_name: subdoor_pose, object_class: '', time_duration: 0.0}"
```

Manual screwdriver request:

```bash
ros2 action send_goal /run_perception_pipeline my_robot_interfaces/action/RunVision "{task_name: detect_screwdriver, object_class: '', time_duration: 0.0}"
```

## FSM diagram generation

Generate the door disassemble diagram PNG:

```bash
cd ~/r4s
python3 src/Finite-State-Machine/scripts/generate_fsm_diagram.py src/Finite-State-Machine/include/door_disassemble.fsm
```

The PNG is written next to the `.fsm` file:

[`include/door_disassemble_diagram.png`](include/door_disassemble_diagram.png)

## Notes

- `door_disassemble` waits for keyboard input on startup. Press `Enter` to start and `a` then `Enter` to abort.
- `door_disassemble` currently uses object-specific view poses for perception if those keys exist in `named_poses.json`.
- `screwdriver_pick` is a helper node used by `door_disassemble`; it is not launched automatically.
- The gripper backend is selected in:
  - [`src/common.py`](src/common.py)

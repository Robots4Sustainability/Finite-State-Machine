cmake_minimum_required(VERSION 3.8)
project(pick_place_fsm)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(geometry_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/CaptureReference.srv"
  "srv/RunScrewdriverRoutine.srv"
  "action/Perception.action"
  DEPENDENCIES geometry_msgs
)

install(PROGRAMS
  src/pick_place.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME pick_place
)

install(PROGRAMS
  src/door_disassemble.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME door_disassemble
)

install(PROGRAMS
  src/mock_perception_server.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME mock_perception_server
)

install(PROGRAMS
  src/screwdriver_pick.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME screwdriver_pick
)

install(PROGRAMS
  scripts/pose_capturer.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME pose_capturer
)

install(PROGRAMS
  include/fsm_pick_place.py
  include/fsm_door_disassemble.py
  src/common.py
  src/error_handling.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY include/
  DESTINATION include
)

ament_package()

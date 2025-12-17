cmake_minimum_required(VERSION 3.8)
project(pick_place_fsm)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  src/pick_place.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME pick_place
)

install(PROGRAMS
  include/fsm_pick_place.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY include/
  DESTINATION include
)

ament_package()

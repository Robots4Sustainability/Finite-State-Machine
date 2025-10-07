cmake_minimum_required(VERSION 3.8)
project(pick_place_fsm)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(eddie_ros REQUIRED)   # ← only for .action headers

# ----------  CLIENT NODE  ----------
add_executable(pick_place_fsm_mock
  src/pick_place_fsm_mock.cpp)
ament_target_dependencies(pick_place_fsm_mock
  rclcpp rclcpp_action geometry_msgs eddie_ros)
install(TARGETS pick_place_fsm_mock
  DESTINATION lib/${PROJECT_NAME})

# ----------  MOCK SERVER NODE  ----------
add_executable(mock_servers_only
  src/mock_servers_only.cpp)
ament_target_dependencies(mock_servers_only
  rclcpp rclcpp_action eddie_ros)   # geometry_msgs pulled in by eddie_ros
install(TARGETS mock_servers_only
  DESTINATION lib/${PROJECT_NAME})

ament_package()
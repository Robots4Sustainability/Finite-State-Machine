cmake_minimum_required(VERSION 3.8)
project(pick_place_fsm)

# --------------------------------------------------
# Compiler setup
# --------------------------------------------------
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# --------------------------------------------------
# Dependencies
# --------------------------------------------------
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(eddie_ros REQUIRED)
find_package(coord2b REQUIRED)

# --------------------------------------------------
# Include directories
# --------------------------------------------------
include_directories(
  include
  ${coord2b_INCLUDE_DIRS}
)

# --------------------------------------------------
# Executable: Pick & Place FSM mock
# --------------------------------------------------
add_executable(pick_place_fsm_mock
  src/pick_place_fsm_mock.cpp
)

ament_target_dependencies(pick_place_fsm_mock
  rclcpp
  rclcpp_action
  geometry_msgs
  eddie_ros
  coord2b
)

# Link against coord2b explicitly (if it exports targets)
target_link_libraries(pick_place_fsm_mock
  coord2b
)

install(TARGETS pick_place_fsm_mock
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

# --------------------------------------------------
# Executable: Mock servers only
# --------------------------------------------------
add_executable(mock_servers_only
  src/mock_servers_only.cpp
)

ament_target_dependencies(mock_servers_only
  rclcpp
  rclcpp_action
  eddie_ros
  coord2b
)

install(TARGETS mock_servers_only
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

# --------------------------------------------------
# Install headers
# --------------------------------------------------
install(
  DIRECTORY include/
  DESTINATION include
)

ament_package()

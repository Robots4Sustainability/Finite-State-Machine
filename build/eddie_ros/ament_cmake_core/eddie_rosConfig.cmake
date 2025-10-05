# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_eddie_ros_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED eddie_ros_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(eddie_ros_FOUND FALSE)
  elseif(NOT eddie_ros_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(eddie_ros_FOUND FALSE)
  endif()
  return()
endif()
set(_eddie_ros_CONFIG_INCLUDED TRUE)

# output package information
if(NOT eddie_ros_FIND_QUIETLY)
  message(STATUS "Found eddie_ros: 0.0.1 (${eddie_ros_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'eddie_ros' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT eddie_ros_DEPRECATED_QUIET)
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(eddie_ros_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "rosidl_cmake-extras.cmake;ament_cmake_export_dependencies-extras.cmake;ament_cmake_export_include_directories-extras.cmake;ament_cmake_export_libraries-extras.cmake;ament_cmake_export_targets-extras.cmake;rosidl_cmake_export_typesupport_targets-extras.cmake;rosidl_cmake_export_typesupport_libraries-extras.cmake")
foreach(_extra ${_extras})
  include("${eddie_ros_DIR}/${_extra}")
endforeach()

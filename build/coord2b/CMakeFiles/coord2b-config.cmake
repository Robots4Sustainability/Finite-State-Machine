# - Config file for the coord2b package
# It defines the following variables
#  coord2b_INCLUDE_DIRS - include directories for coord2b
#  coord2b_LIBRARIES    - libraries to link against

# Compute paths
get_filename_component(coord2b_CMAKE_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
set(coord2b_INCLUDE_DIRS "${coord2b_CMAKE_DIR}/../../../include")

# Our library dependencies (contains definitions for IMPORTED targets)
if(NOT coord2b_BINARY_DIR)
  include("${coord2b_CMAKE_DIR}/coord2b-targets.cmake")
endif()

# These are IMPORTED targets created by coord2b-targets.cmake
set(coord2b_LIBRARIES coord2b)

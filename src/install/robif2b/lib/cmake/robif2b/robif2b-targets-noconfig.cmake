#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "robif2b::2dof" for configuration ""
set_property(TARGET robif2b::2dof APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(robif2b::2dof PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/lib2dof.so"
  IMPORTED_SONAME_NOCONFIG "lib2dof.so"
  )

list(APPEND _cmake_import_check_targets robif2b::2dof )
list(APPEND _cmake_import_check_files_for_robif2b::2dof "${_IMPORT_PREFIX}/lib/lib2dof.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

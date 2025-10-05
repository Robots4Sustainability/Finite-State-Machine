#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "coord2b" for configuration ""
set_property(TARGET coord2b APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(coord2b PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libcoord2b.so"
  IMPORTED_SONAME_NOCONFIG "libcoord2b.so"
  )

list(APPEND _cmake_import_check_targets coord2b )
list(APPEND _cmake_import_check_files_for_coord2b "${_IMPORT_PREFIX}/lib/libcoord2b.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

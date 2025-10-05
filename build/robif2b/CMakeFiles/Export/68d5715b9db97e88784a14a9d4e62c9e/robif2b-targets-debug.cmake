#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "robif2b::2dof" for configuration "Debug"
set_property(TARGET robif2b::2dof APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(robif2b::2dof PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/lib2dof.so"
  IMPORTED_SONAME_DEBUG "lib2dof.so"
  )

list(APPEND _cmake_import_check_targets robif2b::2dof )
list(APPEND _cmake_import_check_files_for_robif2b::2dof "${_IMPORT_PREFIX}/lib/lib2dof.so" )

# Import target "robif2b::ethercat" for configuration "Debug"
set_property(TARGET robif2b::ethercat APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(robif2b::ethercat PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_DEBUG "soem"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libethercat.so"
  IMPORTED_SONAME_DEBUG "libethercat.so"
  )

list(APPEND _cmake_import_check_targets robif2b::ethercat )
list(APPEND _cmake_import_check_files_for_robif2b::ethercat "${_IMPORT_PREFIX}/lib/libethercat.so" )

# Import target "robif2b::kinova_gen3" for configuration "Debug"
set_property(TARGET robif2b::kinova_gen3 APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(robif2b::kinova_gen3 PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libkinova_gen3.so"
  IMPORTED_SONAME_DEBUG "libkinova_gen3.so"
  )

list(APPEND _cmake_import_check_targets robif2b::kinova_gen3 )
list(APPEND _cmake_import_check_files_for_robif2b::kinova_gen3 "${_IMPORT_PREFIX}/lib/libkinova_gen3.so" )

# Import target "robif2b::kelo" for configuration "Debug"
set_property(TARGET robif2b::kelo APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(robif2b::kelo PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libkelo.so"
  IMPORTED_SONAME_DEBUG "libkelo.so"
  )

list(APPEND _cmake_import_check_targets robif2b::kelo )
list(APPEND _cmake_import_check_files_for_robif2b::kelo "${_IMPORT_PREFIX}/lib/libkelo.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)

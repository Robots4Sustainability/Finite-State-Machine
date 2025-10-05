# Install script for directory: /home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/wasim/r4s/src/install/orocos_kdl")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/liborocos-kdl.so.1.5.2"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/liborocos-kdl.so.1.5"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHECK
           FILE "${file}"
           RPATH "$ORIGIN/../lib")
    endif()
  endforeach()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES
    "/home/wasim/r4s/src/build/orocos_kdl/src/liborocos-kdl.so.1.5.2"
    "/home/wasim/r4s/src/build/orocos_kdl/src/liborocos-kdl.so.1.5"
    )
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/liborocos-kdl.so.1.5.2"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/liborocos-kdl.so.1.5"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHANGE
           FILE "${file}"
           OLD_RPATH "::::::::::::::"
           NEW_RPATH "$ORIGIN/../lib")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/usr/bin/strip" "${file}")
      endif()
    endif()
  endforeach()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/wasim/r4s/src/build/orocos_kdl/src/liborocos-kdl.so")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kdl" TYPE FILE FILES
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/articulatedbodyinertia.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chain.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chaindynparam.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainexternalwrenchestimator.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainfdsolver.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainfdsolver_recursive_newton_euler.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainfksolver.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainfksolverpos_recursive.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainfksolvervel_recursive.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainhdsolver_vereshchagin.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainhdsolver_vereshchagin_fext.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainidsolver.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainidsolver_recursive_newton_euler.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainidsolver_vereshchagin.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainiksolver.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainiksolverpos_lma.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainiksolverpos_nr.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainiksolverpos_nr_jl.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainiksolvervel_pinv.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainiksolvervel_pinv_givens.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainiksolvervel_pinv_nso.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainiksolvervel_wdls.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainjnttojacdotsolver.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/chainjnttojacsolver.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/frameacc.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/frameacc.inl"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/frameacc_io.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/frames.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/frames.inl"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/frames_io.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/framevel.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/framevel.inl"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/framevel_io.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/jacobian.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/jntarray.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/jntarrayacc.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/jntarrayvel.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/jntspaceinertiamatrix.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/joint.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/kdl.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/kinfam.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/kinfam_io.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/motion.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/path.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/path_circle.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/path_composite.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/path_cyclic_closed.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/path_line.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/path_point.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/path_roundedcomposite.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/rigidbodyinertia.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/rotational_interpolation.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/rotational_interpolation_sa.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/rotationalinertia.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/segment.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/solveri.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/stiffness.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/trajectory.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/trajectory_composite.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/trajectory_segment.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/trajectory_stationary.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/tree.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/treefksolver.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/treefksolverpos_recursive.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/treeidsolver.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/treeidsolver_recursive_newton_euler.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/treeiksolver.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/treeiksolverpos_nr_jl.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/treeiksolverpos_online.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/treeiksolvervel_wdls.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/treejnttojacsolver.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/velocityprofile.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/velocityprofile_dirac.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/velocityprofile_rect.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/velocityprofile_spline.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/velocityprofile_trap.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/velocityprofile_traphalf.hpp"
    "/home/wasim/r4s/src/build/orocos_kdl/src/config.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/kdl/utilities" TYPE FILE FILES
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/error.h"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/error_stack.h"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/hash_combine.h"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/kdl-config.h"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/ldl_solver_eigen.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/rall1d.h"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/rall1d_io.h"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/rall2d.h"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/rall2d_io.h"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/rallNd.h"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/scoped_ptr.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/svd_HH.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/svd_eigen_HH.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/svd_eigen_Macie.hpp"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/traits.h"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/utility.h"
    "/home/wasim/r4s/src/orocos_kinematics_dynamics/orocos_kdl/src/utilities/utility_io.h"
    )
endif()


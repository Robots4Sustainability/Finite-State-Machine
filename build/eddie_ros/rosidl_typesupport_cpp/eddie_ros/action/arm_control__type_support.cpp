// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from eddie_ros:action/ArmControl.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "eddie_ros/action/detail/arm_control__functions.h"
#include "eddie_ros/action/detail/arm_control__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _ArmControl_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_Goal_type_support_ids_t;

static const _ArmControl_Goal_type_support_ids_t _ArmControl_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ArmControl_Goal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ArmControl_Goal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ArmControl_Goal_type_support_symbol_names_t _ArmControl_Goal_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, eddie_ros, action, ArmControl_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, eddie_ros, action, ArmControl_Goal)),
  }
};

typedef struct _ArmControl_Goal_type_support_data_t
{
  void * data[2];
} _ArmControl_Goal_type_support_data_t;

static _ArmControl_Goal_type_support_data_t _ArmControl_Goal_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ArmControl_Goal_message_typesupport_map = {
  2,
  "eddie_ros",
  &_ArmControl_Goal_message_typesupport_ids.typesupport_identifier[0],
  &_ArmControl_Goal_message_typesupport_symbol_names.symbol_name[0],
  &_ArmControl_Goal_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ArmControl_Goal_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_Goal_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_Goal__get_type_hash,
  &eddie_ros__action__ArmControl_Goal__get_type_description,
  &eddie_ros__action__ArmControl_Goal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<eddie_ros::action::ArmControl_Goal>()
{
  return &::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_Goal_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl_Goal)() {
  return get_message_type_support_handle<eddie_ros::action::ArmControl_Goal>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _ArmControl_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_Result_type_support_ids_t;

static const _ArmControl_Result_type_support_ids_t _ArmControl_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ArmControl_Result_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ArmControl_Result_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ArmControl_Result_type_support_symbol_names_t _ArmControl_Result_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, eddie_ros, action, ArmControl_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, eddie_ros, action, ArmControl_Result)),
  }
};

typedef struct _ArmControl_Result_type_support_data_t
{
  void * data[2];
} _ArmControl_Result_type_support_data_t;

static _ArmControl_Result_type_support_data_t _ArmControl_Result_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ArmControl_Result_message_typesupport_map = {
  2,
  "eddie_ros",
  &_ArmControl_Result_message_typesupport_ids.typesupport_identifier[0],
  &_ArmControl_Result_message_typesupport_symbol_names.symbol_name[0],
  &_ArmControl_Result_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ArmControl_Result_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_Result_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_Result__get_type_hash,
  &eddie_ros__action__ArmControl_Result__get_type_description,
  &eddie_ros__action__ArmControl_Result__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<eddie_ros::action::ArmControl_Result>()
{
  return &::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_Result_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl_Result)() {
  return get_message_type_support_handle<eddie_ros::action::ArmControl_Result>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _ArmControl_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_Feedback_type_support_ids_t;

static const _ArmControl_Feedback_type_support_ids_t _ArmControl_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ArmControl_Feedback_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ArmControl_Feedback_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ArmControl_Feedback_type_support_symbol_names_t _ArmControl_Feedback_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, eddie_ros, action, ArmControl_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, eddie_ros, action, ArmControl_Feedback)),
  }
};

typedef struct _ArmControl_Feedback_type_support_data_t
{
  void * data[2];
} _ArmControl_Feedback_type_support_data_t;

static _ArmControl_Feedback_type_support_data_t _ArmControl_Feedback_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ArmControl_Feedback_message_typesupport_map = {
  2,
  "eddie_ros",
  &_ArmControl_Feedback_message_typesupport_ids.typesupport_identifier[0],
  &_ArmControl_Feedback_message_typesupport_symbol_names.symbol_name[0],
  &_ArmControl_Feedback_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ArmControl_Feedback_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_Feedback_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_Feedback__get_type_hash,
  &eddie_ros__action__ArmControl_Feedback__get_type_description,
  &eddie_ros__action__ArmControl_Feedback__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<eddie_ros::action::ArmControl_Feedback>()
{
  return &::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl_Feedback)() {
  return get_message_type_support_handle<eddie_ros::action::ArmControl_Feedback>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _ArmControl_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_SendGoal_Request_type_support_ids_t;

static const _ArmControl_SendGoal_Request_type_support_ids_t _ArmControl_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ArmControl_SendGoal_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ArmControl_SendGoal_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ArmControl_SendGoal_Request_type_support_symbol_names_t _ArmControl_SendGoal_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, eddie_ros, action, ArmControl_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, eddie_ros, action, ArmControl_SendGoal_Request)),
  }
};

typedef struct _ArmControl_SendGoal_Request_type_support_data_t
{
  void * data[2];
} _ArmControl_SendGoal_Request_type_support_data_t;

static _ArmControl_SendGoal_Request_type_support_data_t _ArmControl_SendGoal_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ArmControl_SendGoal_Request_message_typesupport_map = {
  2,
  "eddie_ros",
  &_ArmControl_SendGoal_Request_message_typesupport_ids.typesupport_identifier[0],
  &_ArmControl_SendGoal_Request_message_typesupport_symbol_names.symbol_name[0],
  &_ArmControl_SendGoal_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ArmControl_SendGoal_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_SendGoal_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_SendGoal_Request__get_type_hash,
  &eddie_ros__action__ArmControl_SendGoal_Request__get_type_description,
  &eddie_ros__action__ArmControl_SendGoal_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<eddie_ros::action::ArmControl_SendGoal_Request>()
{
  return &::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl_SendGoal_Request)() {
  return get_message_type_support_handle<eddie_ros::action::ArmControl_SendGoal_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _ArmControl_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_SendGoal_Response_type_support_ids_t;

static const _ArmControl_SendGoal_Response_type_support_ids_t _ArmControl_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ArmControl_SendGoal_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ArmControl_SendGoal_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ArmControl_SendGoal_Response_type_support_symbol_names_t _ArmControl_SendGoal_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, eddie_ros, action, ArmControl_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, eddie_ros, action, ArmControl_SendGoal_Response)),
  }
};

typedef struct _ArmControl_SendGoal_Response_type_support_data_t
{
  void * data[2];
} _ArmControl_SendGoal_Response_type_support_data_t;

static _ArmControl_SendGoal_Response_type_support_data_t _ArmControl_SendGoal_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ArmControl_SendGoal_Response_message_typesupport_map = {
  2,
  "eddie_ros",
  &_ArmControl_SendGoal_Response_message_typesupport_ids.typesupport_identifier[0],
  &_ArmControl_SendGoal_Response_message_typesupport_symbol_names.symbol_name[0],
  &_ArmControl_SendGoal_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ArmControl_SendGoal_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_SendGoal_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_SendGoal_Response__get_type_hash,
  &eddie_ros__action__ArmControl_SendGoal_Response__get_type_description,
  &eddie_ros__action__ArmControl_SendGoal_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<eddie_ros::action::ArmControl_SendGoal_Response>()
{
  return &::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl_SendGoal_Response)() {
  return get_message_type_support_handle<eddie_ros::action::ArmControl_SendGoal_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _ArmControl_SendGoal_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_SendGoal_Event_type_support_ids_t;

static const _ArmControl_SendGoal_Event_type_support_ids_t _ArmControl_SendGoal_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ArmControl_SendGoal_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ArmControl_SendGoal_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ArmControl_SendGoal_Event_type_support_symbol_names_t _ArmControl_SendGoal_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, eddie_ros, action, ArmControl_SendGoal_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, eddie_ros, action, ArmControl_SendGoal_Event)),
  }
};

typedef struct _ArmControl_SendGoal_Event_type_support_data_t
{
  void * data[2];
} _ArmControl_SendGoal_Event_type_support_data_t;

static _ArmControl_SendGoal_Event_type_support_data_t _ArmControl_SendGoal_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ArmControl_SendGoal_Event_message_typesupport_map = {
  2,
  "eddie_ros",
  &_ArmControl_SendGoal_Event_message_typesupport_ids.typesupport_identifier[0],
  &_ArmControl_SendGoal_Event_message_typesupport_symbol_names.symbol_name[0],
  &_ArmControl_SendGoal_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ArmControl_SendGoal_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_SendGoal_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_SendGoal_Event__get_type_hash,
  &eddie_ros__action__ArmControl_SendGoal_Event__get_type_description,
  &eddie_ros__action__ArmControl_SendGoal_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<eddie_ros::action::ArmControl_SendGoal_Event>()
{
  return &::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_SendGoal_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl_SendGoal_Event)() {
  return get_message_type_support_handle<eddie_ros::action::ArmControl_SendGoal_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _ArmControl_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_SendGoal_type_support_ids_t;

static const _ArmControl_SendGoal_type_support_ids_t _ArmControl_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ArmControl_SendGoal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ArmControl_SendGoal_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ArmControl_SendGoal_type_support_symbol_names_t _ArmControl_SendGoal_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, eddie_ros, action, ArmControl_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, eddie_ros, action, ArmControl_SendGoal)),
  }
};

typedef struct _ArmControl_SendGoal_type_support_data_t
{
  void * data[2];
} _ArmControl_SendGoal_type_support_data_t;

static _ArmControl_SendGoal_type_support_data_t _ArmControl_SendGoal_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ArmControl_SendGoal_service_typesupport_map = {
  2,
  "eddie_ros",
  &_ArmControl_SendGoal_service_typesupport_ids.typesupport_identifier[0],
  &_ArmControl_SendGoal_service_typesupport_symbol_names.symbol_name[0],
  &_ArmControl_SendGoal_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t ArmControl_SendGoal_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_SendGoal_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<eddie_ros::action::ArmControl_SendGoal_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<eddie_ros::action::ArmControl_SendGoal_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<eddie_ros::action::ArmControl_SendGoal_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<eddie_ros::action::ArmControl_SendGoal>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<eddie_ros::action::ArmControl_SendGoal>,
  &eddie_ros__action__ArmControl_SendGoal__get_type_hash,
  &eddie_ros__action__ArmControl_SendGoal__get_type_description,
  &eddie_ros__action__ArmControl_SendGoal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<eddie_ros::action::ArmControl_SendGoal>()
{
  return &::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_SendGoal_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl_SendGoal)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<eddie_ros::action::ArmControl_SendGoal>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _ArmControl_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_GetResult_Request_type_support_ids_t;

static const _ArmControl_GetResult_Request_type_support_ids_t _ArmControl_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ArmControl_GetResult_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ArmControl_GetResult_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ArmControl_GetResult_Request_type_support_symbol_names_t _ArmControl_GetResult_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, eddie_ros, action, ArmControl_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, eddie_ros, action, ArmControl_GetResult_Request)),
  }
};

typedef struct _ArmControl_GetResult_Request_type_support_data_t
{
  void * data[2];
} _ArmControl_GetResult_Request_type_support_data_t;

static _ArmControl_GetResult_Request_type_support_data_t _ArmControl_GetResult_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ArmControl_GetResult_Request_message_typesupport_map = {
  2,
  "eddie_ros",
  &_ArmControl_GetResult_Request_message_typesupport_ids.typesupport_identifier[0],
  &_ArmControl_GetResult_Request_message_typesupport_symbol_names.symbol_name[0],
  &_ArmControl_GetResult_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ArmControl_GetResult_Request_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_GetResult_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_GetResult_Request__get_type_hash,
  &eddie_ros__action__ArmControl_GetResult_Request__get_type_description,
  &eddie_ros__action__ArmControl_GetResult_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<eddie_ros::action::ArmControl_GetResult_Request>()
{
  return &::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl_GetResult_Request)() {
  return get_message_type_support_handle<eddie_ros::action::ArmControl_GetResult_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _ArmControl_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_GetResult_Response_type_support_ids_t;

static const _ArmControl_GetResult_Response_type_support_ids_t _ArmControl_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ArmControl_GetResult_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ArmControl_GetResult_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ArmControl_GetResult_Response_type_support_symbol_names_t _ArmControl_GetResult_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, eddie_ros, action, ArmControl_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, eddie_ros, action, ArmControl_GetResult_Response)),
  }
};

typedef struct _ArmControl_GetResult_Response_type_support_data_t
{
  void * data[2];
} _ArmControl_GetResult_Response_type_support_data_t;

static _ArmControl_GetResult_Response_type_support_data_t _ArmControl_GetResult_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ArmControl_GetResult_Response_message_typesupport_map = {
  2,
  "eddie_ros",
  &_ArmControl_GetResult_Response_message_typesupport_ids.typesupport_identifier[0],
  &_ArmControl_GetResult_Response_message_typesupport_symbol_names.symbol_name[0],
  &_ArmControl_GetResult_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ArmControl_GetResult_Response_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_GetResult_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_GetResult_Response__get_type_hash,
  &eddie_ros__action__ArmControl_GetResult_Response__get_type_description,
  &eddie_ros__action__ArmControl_GetResult_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<eddie_ros::action::ArmControl_GetResult_Response>()
{
  return &::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl_GetResult_Response)() {
  return get_message_type_support_handle<eddie_ros::action::ArmControl_GetResult_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _ArmControl_GetResult_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_GetResult_Event_type_support_ids_t;

static const _ArmControl_GetResult_Event_type_support_ids_t _ArmControl_GetResult_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ArmControl_GetResult_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ArmControl_GetResult_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ArmControl_GetResult_Event_type_support_symbol_names_t _ArmControl_GetResult_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, eddie_ros, action, ArmControl_GetResult_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, eddie_ros, action, ArmControl_GetResult_Event)),
  }
};

typedef struct _ArmControl_GetResult_Event_type_support_data_t
{
  void * data[2];
} _ArmControl_GetResult_Event_type_support_data_t;

static _ArmControl_GetResult_Event_type_support_data_t _ArmControl_GetResult_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ArmControl_GetResult_Event_message_typesupport_map = {
  2,
  "eddie_ros",
  &_ArmControl_GetResult_Event_message_typesupport_ids.typesupport_identifier[0],
  &_ArmControl_GetResult_Event_message_typesupport_symbol_names.symbol_name[0],
  &_ArmControl_GetResult_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ArmControl_GetResult_Event_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_GetResult_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_GetResult_Event__get_type_hash,
  &eddie_ros__action__ArmControl_GetResult_Event__get_type_description,
  &eddie_ros__action__ArmControl_GetResult_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<eddie_ros::action::ArmControl_GetResult_Event>()
{
  return &::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_GetResult_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl_GetResult_Event)() {
  return get_message_type_support_handle<eddie_ros::action::ArmControl_GetResult_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _ArmControl_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_GetResult_type_support_ids_t;

static const _ArmControl_GetResult_type_support_ids_t _ArmControl_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ArmControl_GetResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ArmControl_GetResult_type_support_symbol_names_t;
#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ArmControl_GetResult_type_support_symbol_names_t _ArmControl_GetResult_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, eddie_ros, action, ArmControl_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, eddie_ros, action, ArmControl_GetResult)),
  }
};

typedef struct _ArmControl_GetResult_type_support_data_t
{
  void * data[2];
} _ArmControl_GetResult_type_support_data_t;

static _ArmControl_GetResult_type_support_data_t _ArmControl_GetResult_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ArmControl_GetResult_service_typesupport_map = {
  2,
  "eddie_ros",
  &_ArmControl_GetResult_service_typesupport_ids.typesupport_identifier[0],
  &_ArmControl_GetResult_service_typesupport_symbol_names.symbol_name[0],
  &_ArmControl_GetResult_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t ArmControl_GetResult_service_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_GetResult_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<eddie_ros::action::ArmControl_GetResult_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<eddie_ros::action::ArmControl_GetResult_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<eddie_ros::action::ArmControl_GetResult_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<eddie_ros::action::ArmControl_GetResult>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<eddie_ros::action::ArmControl_GetResult>,
  &eddie_ros__action__ArmControl_GetResult__get_type_hash,
  &eddie_ros__action__ArmControl_GetResult__get_type_description,
  &eddie_ros__action__ArmControl_GetResult__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<eddie_ros::action::ArmControl_GetResult>()
{
  return &::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_GetResult_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl_GetResult)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<eddie_ros::action::ArmControl_GetResult>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _ArmControl_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_FeedbackMessage_type_support_ids_t;

static const _ArmControl_FeedbackMessage_type_support_ids_t _ArmControl_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  }
};

typedef struct _ArmControl_FeedbackMessage_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _ArmControl_FeedbackMessage_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _ArmControl_FeedbackMessage_type_support_symbol_names_t _ArmControl_FeedbackMessage_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, eddie_ros, action, ArmControl_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, eddie_ros, action, ArmControl_FeedbackMessage)),
  }
};

typedef struct _ArmControl_FeedbackMessage_type_support_data_t
{
  void * data[2];
} _ArmControl_FeedbackMessage_type_support_data_t;

static _ArmControl_FeedbackMessage_type_support_data_t _ArmControl_FeedbackMessage_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _ArmControl_FeedbackMessage_message_typesupport_map = {
  2,
  "eddie_ros",
  &_ArmControl_FeedbackMessage_message_typesupport_ids.typesupport_identifier[0],
  &_ArmControl_FeedbackMessage_message_typesupport_symbol_names.symbol_name[0],
  &_ArmControl_FeedbackMessage_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t ArmControl_FeedbackMessage_message_type_support_handle = {
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_FeedbackMessage_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_FeedbackMessage__get_type_hash,
  &eddie_ros__action__ArmControl_FeedbackMessage__get_type_description,
  &eddie_ros__action__ArmControl_FeedbackMessage__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<eddie_ros::action::ArmControl_FeedbackMessage>()
{
  return &::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl_FeedbackMessage)() {
  return get_message_type_support_handle<eddie_ros::action::ArmControl_FeedbackMessage>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

#include "action_msgs/msg/goal_status_array.hpp"
#include "action_msgs/srv/cancel_goal.hpp"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_typesupport_cpp/action_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_cpp
{

static rosidl_action_type_support_t ArmControl_action_type_support_handle = {
  NULL, NULL, NULL, NULL, NULL,
  &eddie_ros__action__ArmControl__get_type_hash,
  &eddie_ros__action__ArmControl__get_type_description,
  &eddie_ros__action__ArmControl__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace eddie_ros

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
get_action_type_support_handle<eddie_ros::action::ArmControl>()
{
  using ::eddie_ros::action::rosidl_typesupport_cpp::ArmControl_action_type_support_handle;
  // Thread-safe by always writing the same values to the static struct
  ArmControl_action_type_support_handle.goal_service_type_support = get_service_type_support_handle<::eddie_ros::action::ArmControl::Impl::SendGoalService>();
  ArmControl_action_type_support_handle.result_service_type_support = get_service_type_support_handle<::eddie_ros::action::ArmControl::Impl::GetResultService>();
  ArmControl_action_type_support_handle.cancel_service_type_support = get_service_type_support_handle<::eddie_ros::action::ArmControl::Impl::CancelGoalService>();
  ArmControl_action_type_support_handle.feedback_message_type_support = get_message_type_support_handle<::eddie_ros::action::ArmControl::Impl::FeedbackMessage>();
  ArmControl_action_type_support_handle.status_message_type_support = get_message_type_support_handle<::eddie_ros::action::ArmControl::Impl::GoalStatusMessage>();
  return &ArmControl_action_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(rosidl_typesupport_cpp, eddie_ros, action, ArmControl)() {
  return ::rosidl_typesupport_cpp::get_action_type_support_handle<eddie_ros::action::ArmControl>();
}

#ifdef __cplusplus
}
#endif

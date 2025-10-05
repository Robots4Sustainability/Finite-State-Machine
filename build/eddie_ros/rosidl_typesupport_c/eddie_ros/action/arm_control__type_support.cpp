// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from eddie_ros:action/ArmControl.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "eddie_ros/action/detail/arm_control__struct.h"
#include "eddie_ros/action/detail/arm_control__type_support.h"
#include "eddie_ros/action/detail/arm_control__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ArmControl_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_Goal_type_support_ids_t;

static const _ArmControl_Goal_type_support_ids_t _ArmControl_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, eddie_ros, action, ArmControl_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, eddie_ros, action, ArmControl_Goal)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_Goal_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_Goal__get_type_hash,
  &eddie_ros__action__ArmControl_Goal__get_type_description,
  &eddie_ros__action__ArmControl_Goal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace eddie_ros

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, eddie_ros, action, ArmControl_Goal)() {
  return &::eddie_ros::action::rosidl_typesupport_c::ArmControl_Goal_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__type_support.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ArmControl_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_Result_type_support_ids_t;

static const _ArmControl_Result_type_support_ids_t _ArmControl_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, eddie_ros, action, ArmControl_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, eddie_ros, action, ArmControl_Result)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_Result_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_Result__get_type_hash,
  &eddie_ros__action__ArmControl_Result__get_type_description,
  &eddie_ros__action__ArmControl_Result__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace eddie_ros

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, eddie_ros, action, ArmControl_Result)() {
  return &::eddie_ros::action::rosidl_typesupport_c::ArmControl_Result_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__type_support.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ArmControl_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_Feedback_type_support_ids_t;

static const _ArmControl_Feedback_type_support_ids_t _ArmControl_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, eddie_ros, action, ArmControl_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, eddie_ros, action, ArmControl_Feedback)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_Feedback_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_Feedback__get_type_hash,
  &eddie_ros__action__ArmControl_Feedback__get_type_description,
  &eddie_ros__action__ArmControl_Feedback__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace eddie_ros

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, eddie_ros, action, ArmControl_Feedback)() {
  return &::eddie_ros::action::rosidl_typesupport_c::ArmControl_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__type_support.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ArmControl_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_SendGoal_Request_type_support_ids_t;

static const _ArmControl_SendGoal_Request_type_support_ids_t _ArmControl_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, eddie_ros, action, ArmControl_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, eddie_ros, action, ArmControl_SendGoal_Request)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_SendGoal_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_SendGoal_Request__get_type_hash,
  &eddie_ros__action__ArmControl_SendGoal_Request__get_type_description,
  &eddie_ros__action__ArmControl_SendGoal_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace eddie_ros

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, eddie_ros, action, ArmControl_SendGoal_Request)() {
  return &::eddie_ros::action::rosidl_typesupport_c::ArmControl_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__type_support.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ArmControl_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_SendGoal_Response_type_support_ids_t;

static const _ArmControl_SendGoal_Response_type_support_ids_t _ArmControl_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, eddie_ros, action, ArmControl_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, eddie_ros, action, ArmControl_SendGoal_Response)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_SendGoal_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_SendGoal_Response__get_type_hash,
  &eddie_ros__action__ArmControl_SendGoal_Response__get_type_description,
  &eddie_ros__action__ArmControl_SendGoal_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace eddie_ros

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, eddie_ros, action, ArmControl_SendGoal_Response)() {
  return &::eddie_ros::action::rosidl_typesupport_c::ArmControl_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__type_support.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ArmControl_SendGoal_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_SendGoal_Event_type_support_ids_t;

static const _ArmControl_SendGoal_Event_type_support_ids_t _ArmControl_SendGoal_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, eddie_ros, action, ArmControl_SendGoal_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, eddie_ros, action, ArmControl_SendGoal_Event)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_SendGoal_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_SendGoal_Event__get_type_hash,
  &eddie_ros__action__ArmControl_SendGoal_Event__get_type_description,
  &eddie_ros__action__ArmControl_SendGoal_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace eddie_ros

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, eddie_ros, action, ArmControl_SendGoal_Event)() {
  return &::eddie_ros::action::rosidl_typesupport_c::ArmControl_SendGoal_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
#include "service_msgs/msg/service_event_info.h"
#include "builtin_interfaces/msg/time.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_c
{
typedef struct _ArmControl_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_SendGoal_type_support_ids_t;

static const _ArmControl_SendGoal_type_support_ids_t _ArmControl_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, eddie_ros, action, ArmControl_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, eddie_ros, action, ArmControl_SendGoal)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_SendGoal_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &ArmControl_SendGoal_Request_message_type_support_handle,
  &ArmControl_SendGoal_Response_message_type_support_handle,
  &ArmControl_SendGoal_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    eddie_ros,
    action,
    ArmControl_SendGoal
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    eddie_ros,
    action,
    ArmControl_SendGoal
  ),
  &eddie_ros__action__ArmControl_SendGoal__get_type_hash,
  &eddie_ros__action__ArmControl_SendGoal__get_type_description,
  &eddie_ros__action__ArmControl_SendGoal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace eddie_ros

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, eddie_ros, action, ArmControl_SendGoal)() {
  return &::eddie_ros::action::rosidl_typesupport_c::ArmControl_SendGoal_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__type_support.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ArmControl_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_GetResult_Request_type_support_ids_t;

static const _ArmControl_GetResult_Request_type_support_ids_t _ArmControl_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, eddie_ros, action, ArmControl_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, eddie_ros, action, ArmControl_GetResult_Request)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_GetResult_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_GetResult_Request__get_type_hash,
  &eddie_ros__action__ArmControl_GetResult_Request__get_type_description,
  &eddie_ros__action__ArmControl_GetResult_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace eddie_ros

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, eddie_ros, action, ArmControl_GetResult_Request)() {
  return &::eddie_ros::action::rosidl_typesupport_c::ArmControl_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__type_support.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ArmControl_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_GetResult_Response_type_support_ids_t;

static const _ArmControl_GetResult_Response_type_support_ids_t _ArmControl_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, eddie_ros, action, ArmControl_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, eddie_ros, action, ArmControl_GetResult_Response)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_GetResult_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_GetResult_Response__get_type_hash,
  &eddie_ros__action__ArmControl_GetResult_Response__get_type_description,
  &eddie_ros__action__ArmControl_GetResult_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace eddie_ros

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, eddie_ros, action, ArmControl_GetResult_Response)() {
  return &::eddie_ros::action::rosidl_typesupport_c::ArmControl_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__type_support.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ArmControl_GetResult_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_GetResult_Event_type_support_ids_t;

static const _ArmControl_GetResult_Event_type_support_ids_t _ArmControl_GetResult_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, eddie_ros, action, ArmControl_GetResult_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, eddie_ros, action, ArmControl_GetResult_Event)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_GetResult_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_GetResult_Event__get_type_hash,
  &eddie_ros__action__ArmControl_GetResult_Event__get_type_description,
  &eddie_ros__action__ArmControl_GetResult_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace eddie_ros

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, eddie_ros, action, ArmControl_GetResult_Event)() {
  return &::eddie_ros::action::rosidl_typesupport_c::ArmControl_GetResult_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "service_msgs/msg/service_event_info.h"
// already included above
// #include "builtin_interfaces/msg/time.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_c
{
typedef struct _ArmControl_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_GetResult_type_support_ids_t;

static const _ArmControl_GetResult_type_support_ids_t _ArmControl_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, eddie_ros, action, ArmControl_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, eddie_ros, action, ArmControl_GetResult)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_GetResult_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &ArmControl_GetResult_Request_message_type_support_handle,
  &ArmControl_GetResult_Response_message_type_support_handle,
  &ArmControl_GetResult_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    eddie_ros,
    action,
    ArmControl_GetResult
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    eddie_ros,
    action,
    ArmControl_GetResult
  ),
  &eddie_ros__action__ArmControl_GetResult__get_type_hash,
  &eddie_ros__action__ArmControl_GetResult__get_type_description,
  &eddie_ros__action__ArmControl_GetResult__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace eddie_ros

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, eddie_ros, action, ArmControl_GetResult)() {
  return &::eddie_ros::action::rosidl_typesupport_c::ArmControl_GetResult_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__type_support.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace eddie_ros
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _ArmControl_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _ArmControl_FeedbackMessage_type_support_ids_t;

static const _ArmControl_FeedbackMessage_type_support_ids_t _ArmControl_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, eddie_ros, action, ArmControl_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, eddie_ros, action, ArmControl_FeedbackMessage)),
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
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_ArmControl_FeedbackMessage_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &eddie_ros__action__ArmControl_FeedbackMessage__get_type_hash,
  &eddie_ros__action__ArmControl_FeedbackMessage__get_type_description,
  &eddie_ros__action__ArmControl_FeedbackMessage__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace eddie_ros

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, eddie_ros, action, ArmControl_FeedbackMessage)() {
  return &::eddie_ros::action::rosidl_typesupport_c::ArmControl_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

#include "action_msgs/msg/goal_status_array.h"
#include "action_msgs/srv/cancel_goal.h"
#include "eddie_ros/action/arm_control.h"
// already included above
// #include "eddie_ros/action/detail/arm_control__type_support.h"

static rosidl_action_type_support_t _eddie_ros__action__ArmControl__typesupport_c = {
  NULL, NULL, NULL, NULL, NULL,
  &eddie_ros__action__ArmControl__get_type_hash,
  &eddie_ros__action__ArmControl__get_type_description,
  &eddie_ros__action__ArmControl__get_type_description_sources,
};

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(
  rosidl_typesupport_c, eddie_ros, action, ArmControl)()
{
  // Thread-safe by always writing the same values to the static struct
  _eddie_ros__action__ArmControl__typesupport_c.goal_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, eddie_ros, action, ArmControl_SendGoal)();
  _eddie_ros__action__ArmControl__typesupport_c.result_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, eddie_ros, action, ArmControl_GetResult)();
  _eddie_ros__action__ArmControl__typesupport_c.cancel_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, srv, CancelGoal)();
  _eddie_ros__action__ArmControl__typesupport_c.feedback_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, eddie_ros, action, ArmControl_FeedbackMessage)();
  _eddie_ros__action__ArmControl__typesupport_c.status_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, msg, GoalStatusArray)();

  return &_eddie_ros__action__ArmControl__typesupport_c;
}

#ifdef __cplusplus
}
#endif

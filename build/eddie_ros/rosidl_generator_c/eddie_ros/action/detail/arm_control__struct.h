// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from eddie_ros:action/ArmControl.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "eddie_ros/action/arm_control.h"


#ifndef EDDIE_ROS__ACTION__DETAIL__ARM_CONTROL__STRUCT_H_
#define EDDIE_ROS__ACTION__DETAIL__ARM_CONTROL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'target_pose'
#include "geometry_msgs/msg/detail/pose__struct.h"

/// Struct defined in action/ArmControl in the package eddie_ros.
typedef struct eddie_ros__action__ArmControl_Goal
{
  geometry_msgs__msg__Pose target_pose;
} eddie_ros__action__ArmControl_Goal;

// Struct for a sequence of eddie_ros__action__ArmControl_Goal.
typedef struct eddie_ros__action__ArmControl_Goal__Sequence
{
  eddie_ros__action__ArmControl_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__ArmControl_Goal__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"
// Member 'final_pose'
// already included above
// #include "geometry_msgs/msg/detail/pose__struct.h"

/// Struct defined in action/ArmControl in the package eddie_ros.
typedef struct eddie_ros__action__ArmControl_Result
{
  /// Success
  bool success;
  /// Result status message
  rosidl_runtime_c__String message;
  /// Final end effector pose achieved
  geometry_msgs__msg__Pose final_pose;
} eddie_ros__action__ArmControl_Result;

// Struct for a sequence of eddie_ros__action__ArmControl_Result.
typedef struct eddie_ros__action__ArmControl_Result__Sequence
{
  eddie_ros__action__ArmControl_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__ArmControl_Result__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'current_pose'
// already included above
// #include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'status_message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/ArmControl in the package eddie_ros.
typedef struct eddie_ros__action__ArmControl_Feedback
{
  /// Current end effector pose
  geometry_msgs__msg__Pose current_pose;
  /// Possible status
  rosidl_runtime_c__String status_message;
} eddie_ros__action__ArmControl_Feedback;

// Struct for a sequence of eddie_ros__action__ArmControl_Feedback.
typedef struct eddie_ros__action__ArmControl_Feedback__Sequence
{
  eddie_ros__action__ArmControl_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__ArmControl_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "eddie_ros/action/detail/arm_control__struct.h"

/// Struct defined in action/ArmControl in the package eddie_ros.
typedef struct eddie_ros__action__ArmControl_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  eddie_ros__action__ArmControl_Goal goal;
} eddie_ros__action__ArmControl_SendGoal_Request;

// Struct for a sequence of eddie_ros__action__ArmControl_SendGoal_Request.
typedef struct eddie_ros__action__ArmControl_SendGoal_Request__Sequence
{
  eddie_ros__action__ArmControl_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__ArmControl_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/ArmControl in the package eddie_ros.
typedef struct eddie_ros__action__ArmControl_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} eddie_ros__action__ArmControl_SendGoal_Response;

// Struct for a sequence of eddie_ros__action__ArmControl_SendGoal_Response.
typedef struct eddie_ros__action__ArmControl_SendGoal_Response__Sequence
{
  eddie_ros__action__ArmControl_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__ArmControl_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  eddie_ros__action__ArmControl_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  eddie_ros__action__ArmControl_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/ArmControl in the package eddie_ros.
typedef struct eddie_ros__action__ArmControl_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  eddie_ros__action__ArmControl_SendGoal_Request__Sequence request;
  eddie_ros__action__ArmControl_SendGoal_Response__Sequence response;
} eddie_ros__action__ArmControl_SendGoal_Event;

// Struct for a sequence of eddie_ros__action__ArmControl_SendGoal_Event.
typedef struct eddie_ros__action__ArmControl_SendGoal_Event__Sequence
{
  eddie_ros__action__ArmControl_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__ArmControl_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/ArmControl in the package eddie_ros.
typedef struct eddie_ros__action__ArmControl_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} eddie_ros__action__ArmControl_GetResult_Request;

// Struct for a sequence of eddie_ros__action__ArmControl_GetResult_Request.
typedef struct eddie_ros__action__ArmControl_GetResult_Request__Sequence
{
  eddie_ros__action__ArmControl_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__ArmControl_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.h"

/// Struct defined in action/ArmControl in the package eddie_ros.
typedef struct eddie_ros__action__ArmControl_GetResult_Response
{
  int8_t status;
  eddie_ros__action__ArmControl_Result result;
} eddie_ros__action__ArmControl_GetResult_Response;

// Struct for a sequence of eddie_ros__action__ArmControl_GetResult_Response.
typedef struct eddie_ros__action__ArmControl_GetResult_Response__Sequence
{
  eddie_ros__action__ArmControl_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__ArmControl_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  eddie_ros__action__ArmControl_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  eddie_ros__action__ArmControl_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/ArmControl in the package eddie_ros.
typedef struct eddie_ros__action__ArmControl_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  eddie_ros__action__ArmControl_GetResult_Request__Sequence request;
  eddie_ros__action__ArmControl_GetResult_Response__Sequence response;
} eddie_ros__action__ArmControl_GetResult_Event;

// Struct for a sequence of eddie_ros__action__ArmControl_GetResult_Event.
typedef struct eddie_ros__action__ArmControl_GetResult_Event__Sequence
{
  eddie_ros__action__ArmControl_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__ArmControl_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "eddie_ros/action/detail/arm_control__struct.h"

/// Struct defined in action/ArmControl in the package eddie_ros.
typedef struct eddie_ros__action__ArmControl_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  eddie_ros__action__ArmControl_Feedback feedback;
} eddie_ros__action__ArmControl_FeedbackMessage;

// Struct for a sequence of eddie_ros__action__ArmControl_FeedbackMessage.
typedef struct eddie_ros__action__ArmControl_FeedbackMessage__Sequence
{
  eddie_ros__action__ArmControl_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__ArmControl_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // EDDIE_ROS__ACTION__DETAIL__ARM_CONTROL__STRUCT_H_

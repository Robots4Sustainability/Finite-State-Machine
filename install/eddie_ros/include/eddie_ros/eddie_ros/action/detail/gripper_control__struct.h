// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from eddie_ros:action/GripperControl.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "eddie_ros/action/gripper_control.h"


#ifndef EDDIE_ROS__ACTION__DETAIL__GRIPPER_CONTROL__STRUCT_H_
#define EDDIE_ROS__ACTION__DETAIL__GRIPPER_CONTROL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/GripperControl in the package eddie_ros.
typedef struct eddie_ros__action__GripperControl_Goal
{
  /// 0.0 = fully closed, 1.0 = fully open
  double target_position;
  /// Maximum velocity (optional, use default if 0.0)
  double velocity;
  /// Maximum force/effort (optional, use default if 0.0)
  double force;
} eddie_ros__action__GripperControl_Goal;

// Struct for a sequence of eddie_ros__action__GripperControl_Goal.
typedef struct eddie_ros__action__GripperControl_Goal__Sequence
{
  eddie_ros__action__GripperControl_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__GripperControl_Goal__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/GripperControl in the package eddie_ros.
typedef struct eddie_ros__action__GripperControl_Result
{
  /// Success
  bool success;
  /// Result status message
  rosidl_runtime_c__String message;
  /// Final gripper position achieved
  double final_position;
} eddie_ros__action__GripperControl_Result;

// Struct for a sequence of eddie_ros__action__GripperControl_Result.
typedef struct eddie_ros__action__GripperControl_Result__Sequence
{
  eddie_ros__action__GripperControl_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__GripperControl_Result__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'status_message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/GripperControl in the package eddie_ros.
typedef struct eddie_ros__action__GripperControl_Feedback
{
  /// Current gripper position
  double current_position;
  /// Possible status message
  rosidl_runtime_c__String status_message;
} eddie_ros__action__GripperControl_Feedback;

// Struct for a sequence of eddie_ros__action__GripperControl_Feedback.
typedef struct eddie_ros__action__GripperControl_Feedback__Sequence
{
  eddie_ros__action__GripperControl_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__GripperControl_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "eddie_ros/action/detail/gripper_control__struct.h"

/// Struct defined in action/GripperControl in the package eddie_ros.
typedef struct eddie_ros__action__GripperControl_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  eddie_ros__action__GripperControl_Goal goal;
} eddie_ros__action__GripperControl_SendGoal_Request;

// Struct for a sequence of eddie_ros__action__GripperControl_SendGoal_Request.
typedef struct eddie_ros__action__GripperControl_SendGoal_Request__Sequence
{
  eddie_ros__action__GripperControl_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__GripperControl_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/GripperControl in the package eddie_ros.
typedef struct eddie_ros__action__GripperControl_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} eddie_ros__action__GripperControl_SendGoal_Response;

// Struct for a sequence of eddie_ros__action__GripperControl_SendGoal_Response.
typedef struct eddie_ros__action__GripperControl_SendGoal_Response__Sequence
{
  eddie_ros__action__GripperControl_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__GripperControl_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  eddie_ros__action__GripperControl_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  eddie_ros__action__GripperControl_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/GripperControl in the package eddie_ros.
typedef struct eddie_ros__action__GripperControl_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  eddie_ros__action__GripperControl_SendGoal_Request__Sequence request;
  eddie_ros__action__GripperControl_SendGoal_Response__Sequence response;
} eddie_ros__action__GripperControl_SendGoal_Event;

// Struct for a sequence of eddie_ros__action__GripperControl_SendGoal_Event.
typedef struct eddie_ros__action__GripperControl_SendGoal_Event__Sequence
{
  eddie_ros__action__GripperControl_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__GripperControl_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/GripperControl in the package eddie_ros.
typedef struct eddie_ros__action__GripperControl_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} eddie_ros__action__GripperControl_GetResult_Request;

// Struct for a sequence of eddie_ros__action__GripperControl_GetResult_Request.
typedef struct eddie_ros__action__GripperControl_GetResult_Request__Sequence
{
  eddie_ros__action__GripperControl_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__GripperControl_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "eddie_ros/action/detail/gripper_control__struct.h"

/// Struct defined in action/GripperControl in the package eddie_ros.
typedef struct eddie_ros__action__GripperControl_GetResult_Response
{
  int8_t status;
  eddie_ros__action__GripperControl_Result result;
} eddie_ros__action__GripperControl_GetResult_Response;

// Struct for a sequence of eddie_ros__action__GripperControl_GetResult_Response.
typedef struct eddie_ros__action__GripperControl_GetResult_Response__Sequence
{
  eddie_ros__action__GripperControl_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__GripperControl_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  eddie_ros__action__GripperControl_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  eddie_ros__action__GripperControl_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/GripperControl in the package eddie_ros.
typedef struct eddie_ros__action__GripperControl_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  eddie_ros__action__GripperControl_GetResult_Request__Sequence request;
  eddie_ros__action__GripperControl_GetResult_Response__Sequence response;
} eddie_ros__action__GripperControl_GetResult_Event;

// Struct for a sequence of eddie_ros__action__GripperControl_GetResult_Event.
typedef struct eddie_ros__action__GripperControl_GetResult_Event__Sequence
{
  eddie_ros__action__GripperControl_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__GripperControl_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "eddie_ros/action/detail/gripper_control__struct.h"

/// Struct defined in action/GripperControl in the package eddie_ros.
typedef struct eddie_ros__action__GripperControl_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  eddie_ros__action__GripperControl_Feedback feedback;
} eddie_ros__action__GripperControl_FeedbackMessage;

// Struct for a sequence of eddie_ros__action__GripperControl_FeedbackMessage.
typedef struct eddie_ros__action__GripperControl_FeedbackMessage__Sequence
{
  eddie_ros__action__GripperControl_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} eddie_ros__action__GripperControl_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // EDDIE_ROS__ACTION__DETAIL__GRIPPER_CONTROL__STRUCT_H_

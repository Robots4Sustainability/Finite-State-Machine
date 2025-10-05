// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from eddie_ros:action/GripperControl.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "eddie_ros/action/gripper_control.hpp"


#ifndef EDDIE_ROS__ACTION__DETAIL__GRIPPER_CONTROL__BUILDER_HPP_
#define EDDIE_ROS__ACTION__DETAIL__GRIPPER_CONTROL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "eddie_ros/action/detail/gripper_control__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace eddie_ros
{

namespace action
{

namespace builder
{

class Init_GripperControl_Goal_force
{
public:
  explicit Init_GripperControl_Goal_force(::eddie_ros::action::GripperControl_Goal & msg)
  : msg_(msg)
  {}
  ::eddie_ros::action::GripperControl_Goal force(::eddie_ros::action::GripperControl_Goal::_force_type arg)
  {
    msg_.force = std::move(arg);
    return std::move(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_Goal msg_;
};

class Init_GripperControl_Goal_velocity
{
public:
  explicit Init_GripperControl_Goal_velocity(::eddie_ros::action::GripperControl_Goal & msg)
  : msg_(msg)
  {}
  Init_GripperControl_Goal_force velocity(::eddie_ros::action::GripperControl_Goal::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_GripperControl_Goal_force(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_Goal msg_;
};

class Init_GripperControl_Goal_target_position
{
public:
  Init_GripperControl_Goal_target_position()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GripperControl_Goal_velocity target_position(::eddie_ros::action::GripperControl_Goal::_target_position_type arg)
  {
    msg_.target_position = std::move(arg);
    return Init_GripperControl_Goal_velocity(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::eddie_ros::action::GripperControl_Goal>()
{
  return eddie_ros::action::builder::Init_GripperControl_Goal_target_position();
}

}  // namespace eddie_ros


namespace eddie_ros
{

namespace action
{

namespace builder
{

class Init_GripperControl_Result_final_position
{
public:
  explicit Init_GripperControl_Result_final_position(::eddie_ros::action::GripperControl_Result & msg)
  : msg_(msg)
  {}
  ::eddie_ros::action::GripperControl_Result final_position(::eddie_ros::action::GripperControl_Result::_final_position_type arg)
  {
    msg_.final_position = std::move(arg);
    return std::move(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_Result msg_;
};

class Init_GripperControl_Result_message
{
public:
  explicit Init_GripperControl_Result_message(::eddie_ros::action::GripperControl_Result & msg)
  : msg_(msg)
  {}
  Init_GripperControl_Result_final_position message(::eddie_ros::action::GripperControl_Result::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_GripperControl_Result_final_position(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_Result msg_;
};

class Init_GripperControl_Result_success
{
public:
  Init_GripperControl_Result_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GripperControl_Result_message success(::eddie_ros::action::GripperControl_Result::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_GripperControl_Result_message(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::eddie_ros::action::GripperControl_Result>()
{
  return eddie_ros::action::builder::Init_GripperControl_Result_success();
}

}  // namespace eddie_ros


namespace eddie_ros
{

namespace action
{

namespace builder
{

class Init_GripperControl_Feedback_status_message
{
public:
  explicit Init_GripperControl_Feedback_status_message(::eddie_ros::action::GripperControl_Feedback & msg)
  : msg_(msg)
  {}
  ::eddie_ros::action::GripperControl_Feedback status_message(::eddie_ros::action::GripperControl_Feedback::_status_message_type arg)
  {
    msg_.status_message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_Feedback msg_;
};

class Init_GripperControl_Feedback_current_position
{
public:
  Init_GripperControl_Feedback_current_position()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GripperControl_Feedback_status_message current_position(::eddie_ros::action::GripperControl_Feedback::_current_position_type arg)
  {
    msg_.current_position = std::move(arg);
    return Init_GripperControl_Feedback_status_message(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::eddie_ros::action::GripperControl_Feedback>()
{
  return eddie_ros::action::builder::Init_GripperControl_Feedback_current_position();
}

}  // namespace eddie_ros


namespace eddie_ros
{

namespace action
{

namespace builder
{

class Init_GripperControl_SendGoal_Request_goal
{
public:
  explicit Init_GripperControl_SendGoal_Request_goal(::eddie_ros::action::GripperControl_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::eddie_ros::action::GripperControl_SendGoal_Request goal(::eddie_ros::action::GripperControl_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_SendGoal_Request msg_;
};

class Init_GripperControl_SendGoal_Request_goal_id
{
public:
  Init_GripperControl_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GripperControl_SendGoal_Request_goal goal_id(::eddie_ros::action::GripperControl_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_GripperControl_SendGoal_Request_goal(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::eddie_ros::action::GripperControl_SendGoal_Request>()
{
  return eddie_ros::action::builder::Init_GripperControl_SendGoal_Request_goal_id();
}

}  // namespace eddie_ros


namespace eddie_ros
{

namespace action
{

namespace builder
{

class Init_GripperControl_SendGoal_Response_stamp
{
public:
  explicit Init_GripperControl_SendGoal_Response_stamp(::eddie_ros::action::GripperControl_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::eddie_ros::action::GripperControl_SendGoal_Response stamp(::eddie_ros::action::GripperControl_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_SendGoal_Response msg_;
};

class Init_GripperControl_SendGoal_Response_accepted
{
public:
  Init_GripperControl_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GripperControl_SendGoal_Response_stamp accepted(::eddie_ros::action::GripperControl_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_GripperControl_SendGoal_Response_stamp(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::eddie_ros::action::GripperControl_SendGoal_Response>()
{
  return eddie_ros::action::builder::Init_GripperControl_SendGoal_Response_accepted();
}

}  // namespace eddie_ros


namespace eddie_ros
{

namespace action
{

namespace builder
{

class Init_GripperControl_SendGoal_Event_response
{
public:
  explicit Init_GripperControl_SendGoal_Event_response(::eddie_ros::action::GripperControl_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::eddie_ros::action::GripperControl_SendGoal_Event response(::eddie_ros::action::GripperControl_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_SendGoal_Event msg_;
};

class Init_GripperControl_SendGoal_Event_request
{
public:
  explicit Init_GripperControl_SendGoal_Event_request(::eddie_ros::action::GripperControl_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_GripperControl_SendGoal_Event_response request(::eddie_ros::action::GripperControl_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_GripperControl_SendGoal_Event_response(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_SendGoal_Event msg_;
};

class Init_GripperControl_SendGoal_Event_info
{
public:
  Init_GripperControl_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GripperControl_SendGoal_Event_request info(::eddie_ros::action::GripperControl_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_GripperControl_SendGoal_Event_request(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::eddie_ros::action::GripperControl_SendGoal_Event>()
{
  return eddie_ros::action::builder::Init_GripperControl_SendGoal_Event_info();
}

}  // namespace eddie_ros


namespace eddie_ros
{

namespace action
{

namespace builder
{

class Init_GripperControl_GetResult_Request_goal_id
{
public:
  Init_GripperControl_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::eddie_ros::action::GripperControl_GetResult_Request goal_id(::eddie_ros::action::GripperControl_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::eddie_ros::action::GripperControl_GetResult_Request>()
{
  return eddie_ros::action::builder::Init_GripperControl_GetResult_Request_goal_id();
}

}  // namespace eddie_ros


namespace eddie_ros
{

namespace action
{

namespace builder
{

class Init_GripperControl_GetResult_Response_result
{
public:
  explicit Init_GripperControl_GetResult_Response_result(::eddie_ros::action::GripperControl_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::eddie_ros::action::GripperControl_GetResult_Response result(::eddie_ros::action::GripperControl_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_GetResult_Response msg_;
};

class Init_GripperControl_GetResult_Response_status
{
public:
  Init_GripperControl_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GripperControl_GetResult_Response_result status(::eddie_ros::action::GripperControl_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_GripperControl_GetResult_Response_result(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::eddie_ros::action::GripperControl_GetResult_Response>()
{
  return eddie_ros::action::builder::Init_GripperControl_GetResult_Response_status();
}

}  // namespace eddie_ros


namespace eddie_ros
{

namespace action
{

namespace builder
{

class Init_GripperControl_GetResult_Event_response
{
public:
  explicit Init_GripperControl_GetResult_Event_response(::eddie_ros::action::GripperControl_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::eddie_ros::action::GripperControl_GetResult_Event response(::eddie_ros::action::GripperControl_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_GetResult_Event msg_;
};

class Init_GripperControl_GetResult_Event_request
{
public:
  explicit Init_GripperControl_GetResult_Event_request(::eddie_ros::action::GripperControl_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_GripperControl_GetResult_Event_response request(::eddie_ros::action::GripperControl_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_GripperControl_GetResult_Event_response(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_GetResult_Event msg_;
};

class Init_GripperControl_GetResult_Event_info
{
public:
  Init_GripperControl_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GripperControl_GetResult_Event_request info(::eddie_ros::action::GripperControl_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_GripperControl_GetResult_Event_request(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::eddie_ros::action::GripperControl_GetResult_Event>()
{
  return eddie_ros::action::builder::Init_GripperControl_GetResult_Event_info();
}

}  // namespace eddie_ros


namespace eddie_ros
{

namespace action
{

namespace builder
{

class Init_GripperControl_FeedbackMessage_feedback
{
public:
  explicit Init_GripperControl_FeedbackMessage_feedback(::eddie_ros::action::GripperControl_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::eddie_ros::action::GripperControl_FeedbackMessage feedback(::eddie_ros::action::GripperControl_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_FeedbackMessage msg_;
};

class Init_GripperControl_FeedbackMessage_goal_id
{
public:
  Init_GripperControl_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GripperControl_FeedbackMessage_feedback goal_id(::eddie_ros::action::GripperControl_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_GripperControl_FeedbackMessage_feedback(msg_);
  }

private:
  ::eddie_ros::action::GripperControl_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::eddie_ros::action::GripperControl_FeedbackMessage>()
{
  return eddie_ros::action::builder::Init_GripperControl_FeedbackMessage_goal_id();
}

}  // namespace eddie_ros

#endif  // EDDIE_ROS__ACTION__DETAIL__GRIPPER_CONTROL__BUILDER_HPP_

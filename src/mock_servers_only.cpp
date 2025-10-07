#include <memory>
#include <thread>
#include <chrono>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "eddie_ros/action/arm_control.hpp"
#include "eddie_ros/action/gripper_control.hpp"

using ArmControl     = eddie_ros::action::ArmControl;
using GripperControl = eddie_ros::action::GripperControl;
using ArmGH          = rclcpp_action::ServerGoalHandle<ArmControl>;
using GripperGH      = rclcpp_action::ServerGoalHandle<GripperControl>;

class MockServers : public rclcpp::Node
{
public:
  explicit MockServers(const rclcpp::NodeOptions & opt = rclcpp::NodeOptions{})
  : Node("mock_servers", opt)
  {
    arm_server_ = rclcpp_action::create_server<ArmControl>(
      this, "right_arm/arm_control",
      [](const rclcpp_action::GoalUUID &, std::shared_ptr<const ArmControl::Goal>)
      { return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE; },
      [](const std::shared_ptr<ArmGH>) { return rclcpp_action::CancelResponse::ACCEPT; },
      [this](const std::shared_ptr<ArmGH> gh)
      { std::thread(&MockServers::execute_arm, this, gh).detach(); });

    gripper_server_ = rclcpp_action::create_server<GripperControl>(
      this, "right_arm/gripper_control",
      [](const rclcpp_action::GoalUUID &, std::shared_ptr<const GripperControl::Goal>)
      { return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE; },
      [](const std::shared_ptr<GripperGH>) { return rclcpp_action::CancelResponse::ACCEPT; },
      [this](const std::shared_ptr<GripperGH> gh)
      { std::thread(&MockServers::execute_gripper, this, gh).detach(); });

    RCLCPP_INFO(get_logger(), "Mock action servers ready");
  }

private:
  void execute_arm(const std::shared_ptr<ArmGH> gh)
  {
    const auto goal = gh->get_goal();
    auto feedback = std::make_shared<ArmControl::Feedback>();
    auto result   = std::make_shared<ArmControl::Result>();

    RCLCPP_INFO(get_logger(), "Arm goal received – moving");
    for (int i = 0; i < 10; ++i) {
      if (gh->is_canceling()) {
        result->success = false;
        result->message = "Cancelled";
        gh->canceled(result); return;
      }
      feedback->current_pose = goal->target_pose;
      feedback->status_message = "Moving ...";
      gh->publish_feedback(feedback);
      std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    result->success = true;
    result->message = "arm success";
    result->final_pose = goal->target_pose;
    gh->succeed(result);
    RCLCPP_INFO(get_logger(), "Arm goal succeeded");
  }

  void execute_gripper(const std::shared_ptr<GripperGH> gh)
  {
    auto feedback = std::make_shared<GripperControl::Feedback>();
    auto result   = std::make_shared<GripperControl::Result>();
    RCLCPP_INFO(get_logger(), "Gripper goal received");
    for (int i = 0; i < 5; ++i) {
      if (gh->is_canceling()) {
        result->success = false; result->message = "Cancelled";
        gh->canceled(result); return;
      }
      feedback->current_position = 100.0;
      feedback->status_message = "Closing ...";
      gh->publish_feedback(feedback);
      std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    result->success = true;
    result->message = "gripper success";
    result->final_position = 100.0;
    gh->succeed(result);
    RCLCPP_INFO(get_logger(), "Gripper goal succeeded");
  }

  rclcpp_action::Server<ArmControl>::SharedPtr     arm_server_;
  rclcpp_action::Server<GripperControl>::SharedPtr gripper_server_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MockServers>());
  rclcpp::shutdown();
  return 0;
}
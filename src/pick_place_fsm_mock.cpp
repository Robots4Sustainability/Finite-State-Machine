
#include <memory>
#include <string>
#include <thread>
#include <chrono>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"

#include "eddie_ros/action/arm_control.hpp"
#include "eddie_ros/action/gripper_control.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"

#include "pick_place_fsm.hpp" 

// Forward declaration
void fsm_behavior(struct events *eventData, struct PickPlaceNode_user_data *ud);

// ============================================================================
// PickPlaceNode definition
// ============================================================================
class PickPlaceNode : public rclcpp::Node
{
public:
  using ArmControl     = eddie_ros::action::ArmControl;
  using GripperControl = eddie_ros::action::GripperControl;

  explicit PickPlaceNode(const rclcpp::NodeOptions & opt = rclcpp::NodeOptions{})
  : Node("pick_place_fsm_node", opt)
  {
    // ------------------------------------------------------------------------
    // Action clients
    // ------------------------------------------------------------------------
    arm_client_     = rclcpp_action::create_client<ArmControl>(this, "right_arm/arm_control");
    gripper_client_ = rclcpp_action::create_client<GripperControl>(this, "right_arm/gripper_control");

    // ------------------------------------------------------------------------
    // Perception subscriber
    // ------------------------------------------------------------------------
    perception_sub_ = create_subscription<geometry_msgs::msg::PoseStamped>(
      "/perception/target_pose", 10,
      std::bind(&PickPlaceNode::on_perception, this, std::placeholders::_1));

    // ------------------------------------------------------------------------
    // FSM timer
    // ------------------------------------------------------------------------
    timer_ = create_wall_timer(std::chrono::milliseconds(100),
      std::bind(&PickPlaceNode::fsm_loop, this));

    // ------------------------------------------------------------------------
    // User data initialization
    // ------------------------------------------------------------------------
    user_data_.node           = this;
    user_data_.arm_client     = arm_client_;
    user_data_.gripper_client = gripper_client_;

    // Hard-coded place pose
    user_data_.place_pose.position.x    = 0.60;
    user_data_.place_pose.position.y    = 0.0;
    user_data_.place_pose.position.z    = 0.20;
    user_data_.place_pose.orientation.x = 0.0;
    user_data_.place_pose.orientation.y = 0.0;
    user_data_.place_pose.orientation.z = 0.0;
    user_data_.place_pose.orientation.w = 1.0;

    RCLCPP_INFO(get_logger(), "PickPlace FSM node ready – waiting for /perception/target_pose");
  }

private:
  // --------------------------------------------------------------------------
  // FSM data
  // --------------------------------------------------------------------------
  struct user_data
  {
    PickPlaceNode * node;
    geometry_msgs::msg::Pose target_pose;
    geometry_msgs::msg::Pose place_pose;
    rclcpp_action::Client<ArmControl>::SharedPtr arm_client;
    rclcpp_action::Client<GripperControl>::SharedPtr gripper_client;
  } user_data_;

  // --------------------------------------------------------------------------
  // ROS interfaces
  // --------------------------------------------------------------------------
  rclcpp_action::Client<ArmControl>::SharedPtr arm_client_;
  rclcpp_action::Client<GripperControl>::SharedPtr gripper_client_;
  rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr perception_sub_;
  rclcpp::TimerBase::SharedPtr timer_;

  // --------------------------------------------------------------------------
  // FSM main loop
  // --------------------------------------------------------------------------
  void fsm_loop()
  {
    produce_event(fsm.eventData, E_STEP);
    fsm_behavior(fsm.eventData, &user_data_);
    fsm_step_nbx(&fsm);
    reconfig_event_buffers(fsm.eventData);
  }

  // --------------------------------------------------------------------------
  // Perception callback
  // --------------------------------------------------------------------------
  void on_perception(const geometry_msgs::msg::PoseStamped::SharedPtr msg)
  {
    RCLCPP_INFO(get_logger(), "Perception pose received – starting pick & place");
    user_data_.target_pose = msg->pose;
    produce_event(fsm.eventData, E_PERCEPTION_POSE);
  }

  // --------------------------------------------------------------------------
  // FSM helpers (actions)
  // --------------------------------------------------------------------------
  static void send_approach_goal(user_data *ud, struct events *ev)
  {
    auto node = ud->node;
    if (!ud->arm_client->wait_for_action_server(std::chrono::seconds(2))) {
      RCLCPP_ERROR(node->get_logger(), "Arm server not up – abort");
      produce_event(ev, E_APPROACH_DONE_FAIL);
      return;
    }

    ArmControl::Goal goal;
    goal.target_pose = ud->target_pose;
    goal.target_pose.position.z -= 0.10; // approach offset

    auto opt = rclcpp_action::Client<ArmControl>::SendGoalOptions();
    opt.result_callback = [node, ev](const auto &r) {
      if (r.code == rclcpp_action::ResultCode::SUCCEEDED)
        produce_event(ev, E_APPROACH_DONE_OK);
      else
        produce_event(ev, E_APPROACH_DONE_FAIL);
    };

    ud->arm_client->async_send_goal(goal, opt);
    RCLCPP_INFO(node->get_logger(), "[FSM] Approach goal sent");
  }

  static void send_grasp_goal(user_data *ud, struct events *ev)
  {
    auto node = ud->node;
    ArmControl::Goal goal;
    goal.target_pose = ud->target_pose;

    auto opt = rclcpp_action::Client<ArmControl>::SendGoalOptions();
    opt.result_callback = [node, ev](const auto &r) {
      if (r.code == rclcpp_action::ResultCode::SUCCEEDED)
        produce_event(ev, E_GRASP_DONE_OK);
      else
        produce_event(ev, E_GRASP_DONE_FAIL);
    };

    ud->arm_client->async_send_goal(goal, opt);
    RCLCPP_INFO(node->get_logger(), "[FSM] Grasp goal sent");
  }

  static void send_gripper_close(user_data *ud, struct events *ev)
  {
    auto node = ud->node;
    if (!ud->gripper_client->wait_for_action_server(std::chrono::seconds(2))) {
      RCLCPP_ERROR(node->get_logger(), "Gripper server not up – abort");
      produce_event(ev, E_GRIPPER_CLOSE_DONE_FAIL);
      return;
    }

    GripperControl::Goal goal;
    goal.target_position = 100.0;
    goal.velocity = 20.0;
    goal.force = 10.0;

    auto opt = rclcpp_action::Client<GripperControl>::SendGoalOptions();
    opt.result_callback = [node, ev](const auto &r) {
      if (r.code == rclcpp_action::ResultCode::SUCCEEDED)
        produce_event(ev, E_GRIPPER_CLOSE_DONE_OK);
      else
        produce_event(ev, E_GRIPPER_CLOSE_DONE_FAIL);
    };

    ud->gripper_client->async_send_goal(goal, opt);
    RCLCPP_INFO(node->get_logger(), "[FSM] Gripper close goal sent");
  }

  static void send_place_goal(user_data *ud, struct events *ev)
  {
    auto node = ud->node;
    ArmControl::Goal goal;
    goal.target_pose = ud->place_pose;
    goal.target_pose.position.z += 0.10; // above place

    auto opt = rclcpp_action::Client<ArmControl>::SendGoalOptions();
    opt.result_callback = [node, ev](const auto &r) {
      if (r.code == rclcpp_action::ResultCode::SUCCEEDED)
        produce_event(ev, E_PLACE_DONE_OK);
      else
        produce_event(ev, E_PLACE_DONE_FAIL);
    };

    ud->arm_client->async_send_goal(goal, opt);
    RCLCPP_INFO(node->get_logger(), "[FSM] Place goal sent");
  }

  static void send_open_gripper_goal(user_data *ud, struct events *ev)
  {
    auto node = ud->node;
    GripperControl::Goal goal;
    goal.target_position = 0.0;
    goal.velocity = 20.0;
    goal.force = 10.0;

    auto opt = rclcpp_action::Client<GripperControl>::SendGoalOptions();
    opt.result_callback = [node, ev](const auto &r) {
      if (r.code == rclcpp_action::ResultCode::SUCCEEDED)
        produce_event(ev, E_OPEN_DONE_OK);
      else
        produce_event(ev, E_OPEN_DONE_FAIL);
    };

    ud->gripper_client->async_send_goal(goal, opt);
    RCLCPP_INFO(node->get_logger(), "[FSM] Open-gripper goal sent");
  }

  // --------------------------------------------------------------------------
  // FSM friend declaration
  // --------------------------------------------------------------------------
  friend void fsm_behavior(struct events *eventData, struct user_data *ud);
};

// ============================================================================
// FSM behavior implementation
// ============================================================================
void fsm_behavior(struct events *eventData, struct PickPlaceNode::user_data *ud)
{
  if (consume_event(eventData, E_PERCEPTION_POSE)) {
    // Transition handled by FSM reaction
  }

  if (fsm.currentStateIndex == S_MOVE_TO_APPROACH)
    PickPlaceNode::send_approach_goal(ud, eventData);

  if (fsm.currentStateIndex == S_MOVE_TO_GRASP)
    PickPlaceNode::send_grasp_goal(ud, eventData);

  if (fsm.currentStateIndex == S_CLOSE_GRIPPER)
    PickPlaceNode::send_gripper_close(ud, eventData);

  if (fsm.currentStateIndex == S_MOVE_TO_PLACE)
    PickPlaceNode::send_place_goal(ud, eventData);

  if (fsm.currentStateIndex == S_OPEN_GRIPPER)
    PickPlaceNode::send_open_gripper_goal(ud, eventData);

  if (fsm.currentStateIndex == S_FINISHED) {
    RCLCPP_INFO(ud->node->get_logger(), "Pick & Place sequence complete – back to IDLE");
    produce_event(eventData, E_RESET);
  }

  if (fsm.currentStateIndex == S_ABORT) {
    RCLCPP_WARN(ud->node->get_logger(), "Sequence aborted – resetting FSM");
    produce_event(eventData, E_RESET);
  }
}

// ============================================================================
// MAIN
// ============================================================================
int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<PickPlaceNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}

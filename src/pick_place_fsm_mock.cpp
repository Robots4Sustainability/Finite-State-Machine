#include <memory>
#include <string>
#include <thread>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"

#include "eddie_ros/action/arm_control.hpp"
#include "eddie_ros/action/gripper_control.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"

// STATE ENUM
enum class State
{
  IDLE,
  MOVE_TO_APPROACH,
  WAIT_APPROACH_RESULT,
  MOVE_TO_GRASP,
  WAIT_GRASP_RESULT,
  CLOSE_GRIPPER,
  WAIT_GRIPPER_RESULT,
  MOVE_TO_PLACE,        
  WAIT_PLACE_RESULT,    
  OPEN_GRIPPER,         
  WAIT_OPEN_RESULT, 
  FINISHED,
  ABORT
};

//  MOCK CLIENT NODE  
class PickPlaceFSM : public rclcpp::Node
{
public:
  using ArmControl     = eddie_ros::action::ArmControl;
  using GripperControl = eddie_ros::action::GripperControl;

  explicit PickPlaceFSM(const rclcpp::NodeOptions & opt = rclcpp::NodeOptions{})
  : Node("pick_place_fsm", opt), state_(State::IDLE)
  {
    // clients 
    arm_client_     = rclcpp_action::create_client<ArmControl>(this, "right_arm/arm_control");
    gripper_client_ = rclcpp_action::create_client<GripperControl>(this, "right_arm/gripper_control");

    // perception sub 
    perception_sub_ = create_subscription<geometry_msgs::msg::PoseStamped>(
        "/perception/target_pose", 10,
        std::bind(&PickPlaceFSM::on_perception, this, std::placeholders::_1));

    // internal timer  
    timer_ = create_wall_timer(std::chrono::milliseconds(100),
                               std::bind(&PickPlaceFSM::tick, this));
    // hard-coded place pose (10 cm sideways same height)
    place_pose_.position.x    = 0.00;
    place_pose_.position.y    = 0.0;
    place_pose_.position.z    = 0.02;
    place_pose_.orientation.x = 0.0;
    place_pose_.orientation.y = 0.0;
    place_pose_.orientation.z = 0.0;
    place_pose_.orientation.w = 1.0;

    RCLCPP_INFO(get_logger(), "Mock FSM ready – waiting for /perception/target_pose");
  }

private:
  // STATE MACHINE DRIVER  
  void tick()
  {
    switch (state_)
    {
      case State::IDLE:
        /* nothing to do – perception callback will promote us */
        break;

      case State::MOVE_TO_APPROACH:
        send_approach_goal();
        break;

      case State::MOVE_TO_GRASP:
        send_grasp_goal();
        break;

      case State::CLOSE_GRIPPER:
        send_gripper_close();
        break;

      case State::MOVE_TO_PLACE:
        send_place_goal();
        break;

      case State::OPEN_GRIPPER:
        send_open_gripper_goal();
        break;

      case State::FINISHED:
        RCLCPP_INFO(get_logger(), "PICK & PLACE SEQUENCE COMPLETE – back to IDLE");
        state_ = State::IDLE;
        break;

      case State::ABORT:
        RCLCPP_WARN(get_logger(), "SEQUENCE ABORTED – back to IDLE");
        state_ = State::IDLE;
        break;

      default: /* waiting states – result callbacks will promote us */
        break;
    }
  }

  // 1. PERCEPTION TRIGGER  
  void on_perception(const geometry_msgs::msg::PoseStamped::SharedPtr msg)
  {
    if (state_ != State::IDLE) return;          // ignore if busy
    RCLCPP_INFO(get_logger(), "Perception pose received – starting sequence");
    target_pose_ = msg->pose;
    state_       = State::MOVE_TO_APPROACH;
  }

  // 2. APPROACH  
  void send_approach_goal()
  {
    if (!arm_client_->wait_for_action_server(std::chrono::seconds(2)))
    {
      RCLCPP_ERROR(get_logger(), "Arm server not up – abort");
      state_ = State::ABORT;
      return;
    }

    auto goal          = ArmControl::Goal();
    goal.target_pose   = target_pose_;
    // goal.target_pose.position.z += 0.10; // 10 cm away UPDATE CHECK
    goal.target_pose.position.y += 0.02;// UPDATE CHECK

    auto send_opt = rclcpp_action::Client<ArmControl>::SendGoalOptions();
    send_opt.result_callback =
        [this](const rclcpp_action::ClientGoalHandle<ArmControl>::WrappedResult & r)
        { on_arm_result(r, /*is_approach=*/true); };

    arm_client_->async_send_goal(goal, send_opt);
    RCLCPP_INFO(get_logger(), "[FSM] Approach goal sent");
    state_ = State::WAIT_APPROACH_RESULT;
  }

  // 3. GRASP  
  void send_grasp_goal()
  {
    auto goal        = ArmControl::Goal();
    goal.target_pose = target_pose_; // back to object

    auto send_opt = rclcpp_action::Client<ArmControl>::SendGoalOptions();
    send_opt.result_callback =
        [this](const rclcpp_action::ClientGoalHandle<ArmControl>::WrappedResult & r)
        { on_arm_result(r, /*is_approach=*/false); };

    arm_client_->async_send_goal(goal, send_opt);
    RCLCPP_INFO(get_logger(), "[FSM] Grasp goal sent");
    state_ = State::WAIT_GRASP_RESULT;
  }

  // 4. GRIPPER CLOSE  
  void send_gripper_close()
  {
    if (!gripper_client_->wait_for_action_server(std::chrono::seconds(2)))
    {
      RCLCPP_ERROR(get_logger(), "Gripper server not up – abort");
      state_ = State::ABORT;
      return;
    }

    auto goal           = GripperControl::Goal();
    goal.target_position = 100.0;
    goal.velocity        = 20.0;
    goal.force           = 10.0;

    auto send_opt = rclcpp_action::Client<GripperControl>::SendGoalOptions();
    send_opt.result_callback =
        [this](const rclcpp_action::ClientGoalHandle<GripperControl>::WrappedResult & r)
        { on_gripper_result(r); };

    gripper_client_->async_send_goal(goal, send_opt);
    RCLCPP_INFO(get_logger(), "[FSM] Gripper close goal sent");
    state_ = State::WAIT_GRIPPER_RESULT;
  }

  // RESULT CALLBACKS  
  void on_arm_result(const rclcpp_action::ClientGoalHandle<ArmControl>::WrappedResult & r,
                     bool is_approach)
  {
    if (r.code != rclcpp_action::ResultCode::SUCCEEDED)
    {
      RCLCPP_ERROR(get_logger(), "Arm motion failed – abort");
      state_ = State::ABORT;
      return;
    }
    RCLCPP_INFO(get_logger(), "Arm motion succeeded");
    // state_ = is_approach ? State::MOVE_TO_GRASP : State::CLOSE_GRIPPER;   UPDATE CHECK
    if (is_approach)                // we just finished the *approach* → go grasp
        state_ = State::MOVE_TO_GRASP;
    else                            // we just finished the *grasp* → close gripper
        state_ = State::CLOSE_GRIPPER;
  }

  void on_gripper_result(const rclcpp_action::ClientGoalHandle<GripperControl>::WrappedResult & r)
  {
    if (r.code != rclcpp_action::ResultCode::SUCCEEDED)
    {
      RCLCPP_ERROR(get_logger(), "Gripper motion failed – abort");
      state_ = State::ABORT;
      return;
    }
    RCLCPP_INFO(get_logger(), "Gripper motion succeeded");
    // state_ = State::MOVE_TO_PLACE;
        // now decide what comes next depending on *why* we closed/opened
    if (state_ == State::WAIT_GRIPPER_RESULT) {        // we just closed → go to place
        state_ = State::MOVE_TO_PLACE;
    } else if (state_ == State::WAIT_OPEN_RESULT) {    // we just opened → finished
        state_ = State::FINISHED;
    }
  }

  
  
  void send_place_goal()
  {
      auto goal          = ArmControl::Goal();
      goal.target_pose   = place_pose_;
      // goal.target_pose.position.z -= 0.10; // approach 10 cm down
      goal.target_pose.position.y -= 0.02; // approach 10 cm left
      auto opt = rclcpp_action::Client<ArmControl>::SendGoalOptions();
      opt.result_callback = [this](const auto & r){ on_place_result(r); };
      arm_client_->async_send_goal(goal, opt);
      RCLCPP_INFO(get_logger(), "[FSM] Place (approach) goal sent");
      state_ = State::WAIT_PLACE_RESULT;
  }

  void send_open_gripper_goal()
  {
      auto goal                 = GripperControl::Goal();
      goal.target_position      = 0.0;  // fully open
      goal.velocity             = 20.0;
      goal.force                = 10.0;
      auto opt = rclcpp_action::Client<GripperControl>::SendGoalOptions();
      opt.result_callback = [this](const auto & r){ on_open_result(r); };
      gripper_client_->async_send_goal(goal, opt);
      RCLCPP_INFO(get_logger(), "[FSM] Open-gripper goal sent");
      state_ = State::WAIT_OPEN_RESULT;
  }

  void on_place_result(const rclcpp_action::ClientGoalHandle<ArmControl>::WrappedResult & r)
  {
      if (r.code != rclcpp_action::ResultCode::SUCCEEDED){ state_ = State::ABORT; return; }
      RCLCPP_INFO(get_logger(), "Place motion succeeded");
      state_ = State::OPEN_GRIPPER;
  }

  void on_open_result(const rclcpp_action::ClientGoalHandle<GripperControl>::WrappedResult & r)
  {
      if (r.code != rclcpp_action::ResultCode::SUCCEEDED){ state_ = State::ABORT; return; }
      RCLCPP_INFO(get_logger(), "Gripper open succeeded");
      state_ = State::FINISHED;
  }

  // MEMBERS  
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr perception_sub_;
  rclcpp_action::Client<ArmControl>::SharedPtr     arm_client_;
  rclcpp_action::Client<GripperControl>::SharedPtr gripper_client_;

  State state_;
  geometry_msgs::msg::Pose target_pose_; // last perceived pose
  geometry_msgs::msg::Pose place_pose_;   

}; 

// MAIN  
int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PickPlaceFSM>());
  rclcpp::shutdown();
  return 0;
}
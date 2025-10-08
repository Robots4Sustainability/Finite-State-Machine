/*
 * This is an auto-generated file. Do not edit it directly.
 * 
 * FSM: pick_place
 * FSM Description: Pick and Place sequence control
 *
 * -----------------------------------------------------
 * Usage example:
 * -----------------------------------------------------

#include "pick_place_fsm.hpp"

struct user_data {
    // user-defined data
};

void fsm_behavior(struct events *eventData, struct user_data *userData) {
    // consume events and call user-defined behaviors
}

int main() {
    struct user_data userData = {};

    while (true) {
        produce_event(fsm.eventData, E_STEP);

        fsm_behavior(fsm.eventData, &userData);
        fsm_step_nbx(&fsm);
        reconfig_event_buffers(&eventData);
    }

    return 0;
}

 * -----------------------------------------------------
 */

#ifndef PICK_PLACE_FSM_HPP
#define PICK_PLACE_FSM_HPP

#include "coord2b/functions/fsm.h"
#include "coord2b/functions/event_loop.h"

// sm states
enum e_states {
    S_IDLE = 0,
    S_MOVE_TO_APPROACH,
    S_WAIT_APPROACH_RESULT,
    S_MOVE_TO_GRASP,
    S_WAIT_GRASP_RESULT,
    S_CLOSE_GRIPPER,
    S_WAIT_GRIPPER_RESULT,
    S_MOVE_TO_PLACE,
    S_WAIT_PLACE_RESULT,
    S_OPEN_GRIPPER,
    S_WAIT_OPEN_RESULT,
    S_FINISHED,
    S_ABORT,
    S_EXIT,
    NUM_STATES
};

// sm events
enum e_events {
    E_STEP = 0,
    E_PERCEPTION_POSE,
    E_APPROACH_DONE_OK,
    E_APPROACH_DONE_FAIL,
    E_GRASP_DONE_OK,
    E_GRASP_DONE_FAIL,
    E_GRIPPER_CLOSE_DONE_OK,
    E_GRIPPER_CLOSE_DONE_FAIL,
    E_PLACE_DONE_OK,
    E_PLACE_DONE_FAIL,
    E_OPEN_DONE_OK,
    E_OPEN_DONE_FAIL,
    E_RESET,
    NUM_EVENTS
};

// sm transitions
enum e_transitions {
    T_IDLE_MOVE_TO_APPROACH = 0,
    T_MOVE_TO_APPROACH_WAIT,
    T_WAIT_APPROACH_MOVE_TO_GRASP,
    T_WAIT_APPROACH_ABORT,
    T_MOVE_TO_GRASP_WAIT,
    T_WAIT_GRASP_CLOSE_GRIPPER,
    T_WAIT_GRASP_ABORT,
    T_CLOSE_GRIPPER_WAIT,
    T_WAIT_GRIPPER_MOVE_TO_PLACE,
    T_WAIT_GRIPPER_ABORT,
    T_MOVE_TO_PLACE_WAIT,
    T_WAIT_PLACE_OPEN_GRIPPER,
    T_WAIT_PLACE_ABORT,
    T_OPEN_GRIPPER_WAIT,
    T_WAIT_OPEN_FINISHED,
    T_WAIT_OPEN_ABORT,
    T_FINISHED_IDLE,
    T_ABORT_IDLE,
    NUM_TRANSITIONS
};

// sm reactions
enum e_reactions {
    R_E_PERCEPTION_POSE = 0,
    R_E_STEP1,
    R_E_APPROACH_DONE_OK,
    R_E_APPROACH_DONE_FAIL,
    R_E_STEP2,
    R_E_GRASP_DONE_OK,
    R_E_GRASP_DONE_FAIL,
    R_E_STEP3,
    R_E_GRIPPER_CLOSE_DONE_OK,
    R_E_GRIPPER_CLOSE_DONE_FAIL,
    R_E_STEP4,
    R_E_PLACE_DONE_OK,
    R_E_PLACE_DONE_FAIL,
    R_E_STEP5,
    R_E_OPEN_DONE_OK,
    R_E_OPEN_DONE_FAIL,
    R_E_RESET_FINISHED,
    R_E_RESET_ABORT,
    NUM_REACTIONS
};

// sm states
inline struct state states[NUM_STATES] = {
    {.name = "S_IDLE"},
    {.name = "S_MOVE_TO_APPROACH"},
    {.name = "S_WAIT_APPROACH_RESULT"},
    {.name = "S_MOVE_TO_GRASP"},
    {.name = "S_WAIT_GRASP_RESULT"},
    {.name = "S_CLOSE_GRIPPER"},
    {.name = "S_WAIT_GRIPPER_RESULT"},
    {.name = "S_MOVE_TO_PLACE"},
    {.name = "S_WAIT_PLACE_RESULT"},
    {.name = "S_OPEN_GRIPPER"},
    {.name = "S_WAIT_OPEN_RESULT"},
    {.name = "S_FINISHED"},
    {.name = "S_ABORT"},
    {.name = "S_EXIT"}
};

// sm transition table
inline struct transition transitions[NUM_TRANSITIONS] = {
    { .startStateIndex = S_IDLE,              .endStateIndex = S_MOVE_TO_APPROACH },
    { .startStateIndex = S_MOVE_TO_APPROACH,  .endStateIndex = S_WAIT_APPROACH_RESULT },
    { .startStateIndex = S_WAIT_APPROACH_RESULT, .endStateIndex = S_MOVE_TO_GRASP },
    { .startStateIndex = S_WAIT_APPROACH_RESULT, .endStateIndex = S_ABORT },
    { .startStateIndex = S_MOVE_TO_GRASP,     .endStateIndex = S_WAIT_GRASP_RESULT },
    { .startStateIndex = S_WAIT_GRASP_RESULT, .endStateIndex = S_CLOSE_GRIPPER },
    { .startStateIndex = S_WAIT_GRASP_RESULT, .endStateIndex = S_ABORT },
    { .startStateIndex = S_CLOSE_GRIPPER,     .endStateIndex = S_WAIT_GRIPPER_RESULT },
    { .startStateIndex = S_WAIT_GRIPPER_RESULT, .endStateIndex = S_MOVE_TO_PLACE },
    { .startStateIndex = S_WAIT_GRIPPER_RESULT, .endStateIndex = S_ABORT },
    { .startStateIndex = S_MOVE_TO_PLACE,     .endStateIndex = S_WAIT_PLACE_RESULT },
    { .startStateIndex = S_WAIT_PLACE_RESULT, .endStateIndex = S_OPEN_GRIPPER },
    { .startStateIndex = S_WAIT_PLACE_RESULT, .endStateIndex = S_ABORT },
    { .startStateIndex = S_OPEN_GRIPPER,      .endStateIndex = S_WAIT_OPEN_RESULT },
    { .startStateIndex = S_WAIT_OPEN_RESULT,  .endStateIndex = S_FINISHED },
    { .startStateIndex = S_WAIT_OPEN_RESULT,  .endStateIndex = S_ABORT },
    { .startStateIndex = S_FINISHED,          .endStateIndex = S_IDLE },
    { .startStateIndex = S_ABORT,             .endStateIndex = S_IDLE }
};

// sm reaction table
inline struct event_reaction reactions[NUM_REACTIONS] = {
    { .conditionEventIndex = E_PERCEPTION_POSE, .transitionIndex = T_IDLE_MOVE_TO_APPROACH },
    { .conditionEventIndex = E_STEP, .transitionIndex = T_MOVE_TO_APPROACH_WAIT },
    { .conditionEventIndex = E_APPROACH_DONE_OK, .transitionIndex = T_WAIT_APPROACH_MOVE_TO_GRASP },
    { .conditionEventIndex = E_APPROACH_DONE_FAIL, .transitionIndex = T_WAIT_APPROACH_ABORT },
    { .conditionEventIndex = E_STEP, .transitionIndex = T_MOVE_TO_GRASP_WAIT },
    { .conditionEventIndex = E_GRASP_DONE_OK, .transitionIndex = T_WAIT_GRASP_CLOSE_GRIPPER },
    { .conditionEventIndex = E_GRASP_DONE_FAIL, .transitionIndex = T_WAIT_GRASP_ABORT },
    { .conditionEventIndex = E_STEP, .transitionIndex = T_CLOSE_GRIPPER_WAIT },
    { .conditionEventIndex = E_GRIPPER_CLOSE_DONE_OK, .transitionIndex = T_WAIT_GRIPPER_MOVE_TO_PLACE },
    { .conditionEventIndex = E_GRIPPER_CLOSE_DONE_FAIL, .transitionIndex = T_WAIT_GRIPPER_ABORT },
    { .conditionEventIndex = E_STEP, .transitionIndex = T_MOVE_TO_PLACE_WAIT },
    { .conditionEventIndex = E_PLACE_DONE_OK, .transitionIndex = T_WAIT_PLACE_OPEN_GRIPPER },
    { .conditionEventIndex = E_PLACE_DONE_FAIL, .transitionIndex = T_WAIT_PLACE_ABORT },
    { .conditionEventIndex = E_STEP, .transitionIndex = T_OPEN_GRIPPER_WAIT },
    { .conditionEventIndex = E_OPEN_DONE_OK, .transitionIndex = T_WAIT_OPEN_FINISHED },
    { .conditionEventIndex = E_OPEN_DONE_FAIL, .transitionIndex = T_WAIT_OPEN_ABORT },
    { .conditionEventIndex = E_RESET, .transitionIndex = T_FINISHED_IDLE },
    { .conditionEventIndex = E_RESET, .transitionIndex = T_ABORT_IDLE }
};

// sm event data
inline struct events eventData = {
    .numEvents = NUM_EVENTS,
    .currentEvents = new _Bool[NUM_EVENTS]{false},
    .futureEvents = new _Bool[NUM_EVENTS]{false}
};

// sm fsm struct
inline struct fsm_nbx fsm = {
    .numReactions = NUM_REACTIONS,
    .numTransitions = NUM_TRANSITIONS,
    .numStates = NUM_STATES,

    .states = states,
    .startStateIndex = S_IDLE,
    .endStateIndex = S_EXIT,
    .currentStateIndex = S_IDLE,

    .eventData = &eventData,
    .reactions = reactions,
    .transitions = transitions
};

#endif // PICK_PLACE_FSM_HPP
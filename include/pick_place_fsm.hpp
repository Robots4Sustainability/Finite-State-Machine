/*
 * This is an auto-generated file. Do not edit it directly.
 * 
 * FSM: pick_place
 * FSM Description: 
 *
 * -----------------------------------------------------
 * Usage example:
 * -----------------------------------------------------

#include "pick_place.fsm.hpp"

struct user_data {

};

void yyyy_behavior(struct user_data *userData, struct events *eventData) {
    // ... do something

    produce_event(eventData, E_ZZZZ);
}

void fsm_behavior(struct events *eventData, struct user_data *userData) {
    if (consume_event(eventData, E_XXXX)) {
        yyyy_behavior(userData, eventData);
    }
    ...
}

int main() {

    struct user_data userData = {};

    while (true) {
        produce_event(fsm.eventData, E_STEP);

        // run state machine, event loop
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
    S_MOVE_TO_GRASP,
    S_CLOSE_GRIPPER,
    S_MOVE_TO_PLACE,
    S_OPEN_GRIPPER,
    S_FINISHED,
    S_ABORT,
    S_EXIT,
    NUM_STATES
};

// sm events
enum e_events {
    E_PERCEPTION_POSE = 0,
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
    T_APPROACH_MOVE_TO_GRASP,
    T_APPROACH_ABORT,
    T_GRASP_CLOSE_GRIPPER,
    T_GRASP_ABORT,
    T_CLOSE_GRIPPER_MOVE_TO_PLACE,
    T_CLOSE_GRIPPER_ABORT,
    T_PLACE_OPEN_GRIPPER,
    T_PLACE_ABORT,
    T_OPEN_FINISHED,
    T_OPEN_ABORT,
    T_FINISHED_IDLE,
    T_ABORT_IDLE,
    NUM_TRANSITIONS
};

// sm reactions
enum e_reactions {
    R_E_PERCEPTION_POSE = 0,
    R_E_APPROACH_DONE_OK,
    R_E_APPROACH_DONE_FAIL,
    R_E_GRASP_DONE_OK,
    R_E_GRASP_DONE_FAIL,
    R_E_GRIPPER_CLOSE_DONE_OK,
    R_E_GRIPPER_CLOSE_DONE_FAIL,
    R_E_PLACE_DONE_OK,
    R_E_PLACE_DONE_FAIL,
    R_E_OPEN_DONE_OK,
    R_E_OPEN_DONE_FAIL,
    R_E_RESET_FINISHED,
    R_E_RESET_ABORT,
    NUM_REACTIONS
};

// sm states
inline struct state states[NUM_STATES] = {
    {.name = "S_idle"}, 
    {.name = "S_move_to_approach"}, 
    {.name = "S_move_to_grasp"}, 
    {.name = "S_close_gripper"}, 
    {.name = "S_move_to_place"}, 
    {.name = "S_open_gripper"}, 
    {.name = "S_finished"}, 
    {.name = "S_abort"}, 
    {.name = "S_exit"} 
};

// sm transition table
inline struct transition transitions[NUM_TRANSITIONS] = {
    {
        .startStateIndex = S_IDLE,
        .endStateIndex = S_MOVE_TO_APPROACH,
    }, 
    {
        .startStateIndex = S_MOVE_TO_APPROACH,
        .endStateIndex = S_MOVE_TO_GRASP,
    }, 
    {
        .startStateIndex = S_MOVE_TO_APPROACH,
        .endStateIndex = S_ABORT,
    }, 
    {
        .startStateIndex = S_MOVE_TO_GRASP,
        .endStateIndex = S_CLOSE_GRIPPER,
    }, 
    {
        .startStateIndex = S_MOVE_TO_GRASP,
        .endStateIndex = S_ABORT,
    }, 
    {
        .startStateIndex = S_CLOSE_GRIPPER,
        .endStateIndex = S_MOVE_TO_PLACE,
    }, 
    {
        .startStateIndex = S_CLOSE_GRIPPER,
        .endStateIndex = S_ABORT,
    }, 
    {
        .startStateIndex = S_MOVE_TO_PLACE,
        .endStateIndex = S_OPEN_GRIPPER,
    }, 
    {
        .startStateIndex = S_MOVE_TO_PLACE,
        .endStateIndex = S_ABORT,
    }, 
    {
        .startStateIndex = S_OPEN_GRIPPER,
        .endStateIndex = S_FINISHED,
    }, 
    {
        .startStateIndex = S_OPEN_GRIPPER,
        .endStateIndex = S_ABORT,
    }, 
    {
        .startStateIndex = S_FINISHED,
        .endStateIndex = S_IDLE,
    }, 
    {
        .startStateIndex = S_ABORT,
        .endStateIndex = S_IDLE,
    } 
};

// sm reaction table
inline struct event_reaction reactions[NUM_REACTIONS] = {
    {
        .conditionEventIndex = E_PERCEPTION_POSE,
        .transitionIndex = T_IDLE_MOVE_TO_APPROACH,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    }, 
    {
        .conditionEventIndex = E_APPROACH_DONE_OK,
        .transitionIndex = T_APPROACH_MOVE_TO_GRASP,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    }, 
    {
        .conditionEventIndex = E_APPROACH_DONE_FAIL,
        .transitionIndex = T_APPROACH_ABORT,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    }, 
    {
        .conditionEventIndex = E_GRASP_DONE_OK,
        .transitionIndex = T_GRASP_CLOSE_GRIPPER,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    }, 
    {
        .conditionEventIndex = E_GRASP_DONE_FAIL,
        .transitionIndex = T_GRASP_ABORT,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    }, 
    {
        .conditionEventIndex = E_GRIPPER_CLOSE_DONE_OK,
        .transitionIndex = T_CLOSE_GRIPPER_MOVE_TO_PLACE,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    }, 
    {
        .conditionEventIndex = E_GRIPPER_CLOSE_DONE_FAIL,
        .transitionIndex = T_CLOSE_GRIPPER_ABORT,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    }, 
    {
        .conditionEventIndex = E_PLACE_DONE_OK,
        .transitionIndex = T_PLACE_OPEN_GRIPPER,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    }, 
    {
        .conditionEventIndex = E_PLACE_DONE_FAIL,
        .transitionIndex = T_PLACE_ABORT,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    }, 
    {
        .conditionEventIndex = E_OPEN_DONE_OK,
        .transitionIndex = T_OPEN_FINISHED,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    }, 
    {
        .conditionEventIndex = E_OPEN_DONE_FAIL,
        .transitionIndex = T_OPEN_ABORT,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    }, 
    {
        .conditionEventIndex = E_RESET,
        .transitionIndex = T_FINISHED_IDLE,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    }, 
    {
        .conditionEventIndex = E_RESET,
        .transitionIndex = T_ABORT_IDLE,
        .numFiredEvents = 0,
        .firedEventIndices = nullptr,

    } 
};

// sm event data
inline struct events eventData = {
    .numEvents = NUM_EVENTS,
    .currentEvents = new _Bool[NUM_EVENTS]{false},
    .futureEvents = new _Bool[NUM_EVENTS]{false},
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
    .transitions = transitions,
};

#endif // PICK_PLACE_FSM_HPP
"""
This is an auto-generated file. Do not edit it directly.

FSM: pick_place
FSM Description: 

Examples:

>>> from coord_dsl.fsm import fsm_step
>>> from coord_dsl.event_loop import reconfig_event_buffers
>>> from fsm_example import create_fsm
>>> fsm = create_fsm()
>>> while True:
...     if fsm.current_state_index == StateID.S_EXIT:
...         print("State machine completed successfully")
...         break
...     fsm_behavior(fsm, ud) # user-defined behaviour with user data
...     fsm_step(fsm)
...     reconfig_event_buffers(fsm.event_data)
"""
from enum import IntEnum, auto
from coord_dsl.event_loop import EventData
from coord_dsl.fsm import FSMData, Transition, EventReaction


# Event IDs
class EventID(IntEnum):
    E_START = 0
    E_GO_HOME = auto()
    E_PERCEPTION_POSE = auto()
    E_PERCEPTION_FAIL = auto()
    E_PICK_MOVE_DONE = auto()
    E_PLACE_MOVE_DONE = auto()
    E_ARM_MOVE_DONE_FAIL = auto()
    E_GRIPPER_CLOSE_DONE_OK = auto()
    E_GRIPPER_CLOSE_DONE_FAIL = auto()
    E_OPEN_DONE_OK = auto()
    E_OPEN_DONE_FAIL = auto()
    E_HOME_DONE_OK = auto()
    E_HOME_DONE_FAIL = auto()


# State IDs
class StateID(IntEnum):
    S_IDLE = 0
    S_POSE_DETECTION = auto()
    S_MOVE_ARM = auto()
    S_CLOSE_GRIPPER = auto()
    S_OPEN_GRIPPER = auto()
    S_FINISHED = auto()
    S_MOVE_ARM_HOME = auto()
    S_EXIT = auto()


# Transition IDs
class TransitionID(IntEnum):
    T_IDLE_POSE_DETECTION = 0
    T_IDLE_HOME = auto()
    T_POSE_DETECTION_MOVE_ARM = auto()
    T_POSE_DETECTION_IDLE = auto()
    T_MOVE_ARM_CLOSE_GRIPPER = auto()
    T_MOVE_ARM_OPEN_GRIPPER = auto()
    T_MOVE_ARM_EXIT = auto()
    T_CLOSE_GRIPPER_MOVE_ARM = auto()
    T_CLOSE_GRIPPER_EXIT = auto()
    T_OPEN_FINISHED = auto()
    T_OPEN_EXIT = auto()
    T_FINISHED_HOME = auto()
    T_FINISHED_IDLE = auto()
    T_HOME_IDLE = auto()
    T_HOME_EXIT = auto()


# Event reaction IDs
class ReactionID(IntEnum):
    R_E_START = 0
    R_E_GO_HOME_IDLE = auto()
    R_E_PERCEPTION_POSE = auto()
    R_E_PERCEPTION_FAIL = auto()
    R_E_PICK_MOVE_DONE = auto()
    R_E_PLACE_MOVE_DONE = auto()
    R_E_ARM_MOVE_DONE_FAIL = auto()
    R_E_GRIPPER_CLOSE_DONE_OK = auto()
    R_E_GRIPPER_CLOSE_DONE_FAIL = auto()
    R_E_OPEN_DONE_OK = auto()
    R_E_OPEN_DONE_FAIL = auto()
    R_E_GO_HOME_FINISHED = auto()
    R_E_HOME_DONE_OK = auto()
    R_E_HOME_DONE_FAIL = auto()


def create_fsm() -> FSMData:
    """Creates the FSM data structure."""
    # Transitions
    trans_dict = {
        TransitionID.T_IDLE_POSE_DETECTION: Transition(StateID.S_IDLE, StateID.S_POSE_DETECTION),
        TransitionID.T_IDLE_HOME: Transition(StateID.S_IDLE, StateID.S_MOVE_ARM_HOME),
        TransitionID.T_POSE_DETECTION_MOVE_ARM: Transition(StateID.S_POSE_DETECTION, StateID.S_MOVE_ARM),
        TransitionID.T_POSE_DETECTION_IDLE: Transition(StateID.S_POSE_DETECTION, StateID.S_IDLE),
        TransitionID.T_MOVE_ARM_CLOSE_GRIPPER: Transition(StateID.S_MOVE_ARM, StateID.S_CLOSE_GRIPPER),
        TransitionID.T_MOVE_ARM_OPEN_GRIPPER: Transition(StateID.S_MOVE_ARM, StateID.S_OPEN_GRIPPER),
        TransitionID.T_MOVE_ARM_EXIT: Transition(StateID.S_MOVE_ARM, StateID.S_EXIT),
        TransitionID.T_CLOSE_GRIPPER_MOVE_ARM: Transition(StateID.S_CLOSE_GRIPPER, StateID.S_MOVE_ARM),
        TransitionID.T_CLOSE_GRIPPER_EXIT: Transition(StateID.S_CLOSE_GRIPPER, StateID.S_EXIT),
        TransitionID.T_OPEN_FINISHED: Transition(StateID.S_OPEN_GRIPPER, StateID.S_FINISHED),
        TransitionID.T_OPEN_EXIT: Transition(StateID.S_OPEN_GRIPPER, StateID.S_EXIT),
        TransitionID.T_FINISHED_HOME: Transition(StateID.S_FINISHED, StateID.S_MOVE_ARM_HOME),
        TransitionID.T_FINISHED_IDLE: Transition(StateID.S_FINISHED, StateID.S_IDLE),
        TransitionID.T_HOME_IDLE: Transition(StateID.S_MOVE_ARM_HOME, StateID.S_IDLE),
        TransitionID.T_HOME_EXIT: Transition(StateID.S_MOVE_ARM_HOME, StateID.S_EXIT),
    }
    trans_list = [trans_dict[i] for i in TransitionID]

    # Event Reactions
    evt_reaction_dict = {
        ReactionID.R_E_START: EventReaction(
            condition_event_index=EventID.E_START,
            transition_index=TransitionID.T_IDLE_POSE_DETECTION,
            fired_event_indices=[],
        ),
        ReactionID.R_E_GO_HOME_IDLE: EventReaction(
            condition_event_index=EventID.E_GO_HOME,
            transition_index=TransitionID.T_IDLE_HOME,
            fired_event_indices=[],
        ),
        ReactionID.R_E_PERCEPTION_POSE: EventReaction(
            condition_event_index=EventID.E_PERCEPTION_POSE,
            transition_index=TransitionID.T_POSE_DETECTION_MOVE_ARM,
            fired_event_indices=[],
        ),
        ReactionID.R_E_PERCEPTION_FAIL: EventReaction(
            condition_event_index=EventID.E_PERCEPTION_FAIL,
            transition_index=TransitionID.T_POSE_DETECTION_IDLE,
            fired_event_indices=[],
        ),
        ReactionID.R_E_PICK_MOVE_DONE: EventReaction(
            condition_event_index=EventID.E_PICK_MOVE_DONE,
            transition_index=TransitionID.T_MOVE_ARM_CLOSE_GRIPPER,
            fired_event_indices=[],
        ),
        ReactionID.R_E_PLACE_MOVE_DONE: EventReaction(
            condition_event_index=EventID.E_PLACE_MOVE_DONE,
            transition_index=TransitionID.T_MOVE_ARM_OPEN_GRIPPER,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ARM_MOVE_DONE_FAIL: EventReaction(
            condition_event_index=EventID.E_ARM_MOVE_DONE_FAIL,
            transition_index=TransitionID.T_MOVE_ARM_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_GRIPPER_CLOSE_DONE_OK: EventReaction(
            condition_event_index=EventID.E_GRIPPER_CLOSE_DONE_OK,
            transition_index=TransitionID.T_CLOSE_GRIPPER_MOVE_ARM,
            fired_event_indices=[],
        ),
        ReactionID.R_E_GRIPPER_CLOSE_DONE_FAIL: EventReaction(
            condition_event_index=EventID.E_GRIPPER_CLOSE_DONE_FAIL,
            transition_index=TransitionID.T_CLOSE_GRIPPER_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_OPEN_DONE_OK: EventReaction(
            condition_event_index=EventID.E_OPEN_DONE_OK,
            transition_index=TransitionID.T_OPEN_FINISHED,
            fired_event_indices=[],
        ),
        ReactionID.R_E_OPEN_DONE_FAIL: EventReaction(
            condition_event_index=EventID.E_OPEN_DONE_FAIL,
            transition_index=TransitionID.T_OPEN_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_GO_HOME_FINISHED: EventReaction(
            condition_event_index=EventID.E_GO_HOME,
            transition_index=TransitionID.T_FINISHED_HOME,
            fired_event_indices=[],
        ),
        ReactionID.R_E_HOME_DONE_OK: EventReaction(
            condition_event_index=EventID.E_HOME_DONE_OK,
            transition_index=TransitionID.T_HOME_IDLE,
            fired_event_indices=[],
        ),
        ReactionID.R_E_HOME_DONE_FAIL: EventReaction(
            condition_event_index=EventID.E_HOME_DONE_FAIL,
            transition_index=TransitionID.T_HOME_EXIT,
            fired_event_indices=[],
        ),
    }
    evt_reaction_list = [evt_reaction_dict[i] for i in ReactionID]

    # Events
    events = EventData(len(EventID))

    # Return FSM Data
    return FSMData(
        event_data=events,
        num_states=len(StateID),
        start_state_index=StateID.S_IDLE,
        end_state_index=StateID.S_EXIT,
        transitions=trans_list,
        event_reactions=evt_reaction_list,
        current_state_index=StateID.S_IDLE,
    )
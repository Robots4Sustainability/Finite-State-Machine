"""
This is an auto-generated file. Do not edit it directly.

FSM: door_disassemble
FSM Description: FSM for door workflow staging with dummy perception data.

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
    E_ABORT = auto()
    E_INIT_DONE = auto()
    E_INIT_FAIL = auto()
    E_VIEW_POSE_DONE = auto()
    E_VIEW_POSE_FAIL = auto()
    E_SUBDOOR_DONE = auto()
    E_SUBDOOR_FAIL = auto()
    E_SCAN_DONE = auto()
    E_SCAN_FAIL = auto()
    E_SCREWDRIVER_PROBE_DONE = auto()
    E_SCREWDRIVER_PROBE_FAIL = auto()
    E_OBJECT_READY = auto()
    E_NO_MORE_OBJECTS = auto()
    E_PRE_PLACE_DONE = auto()
    E_TABLE_PERCEIVE_DONE = auto()
    E_TABLE_PERCEIVE_FAIL = auto()
    E_PRE_PLACE_BEFORE_PICK_DONE = auto()
    E_PICK_OBJECT_DONE = auto()
    E_PICK_OBJECT_RETREAT_DONE = auto()
    E_PRE_PLACE_WITH_OBJECT_DONE = auto()
    E_MOVE_TO_PLACE_DONE = auto()
    E_PRE_PLACE_AFTER_DROP_DONE = auto()
    E_PRE_PLACE_AFTER_DROP_FAIL = auto()
    E_ARM_MOVE_FAIL = auto()
    E_GRIPPER_CLOSE_DONE = auto()
    E_GRIPPER_OPEN_DONE = auto()
    E_GRIPPER_FAIL = auto()
    E_OBJECTS_DONE = auto()
    E_OBJECTS_FAIL = auto()
    E_GO_MOVE_ARM = auto()
    E_CONFIRM_DONE = auto()


# State IDs
class StateID(IntEnum):
    S_IDLE = 0
    S_INITIALIZE = auto()
    S_MOVE_TO_VIEW_POSE = auto()
    S_GET_SUBDOOR = auto()
    S_RASTER_SCAN = auto()
    S_GET_OBJECTS = auto()
    S_MOVE_ARM = auto()
    S_EXECUTE_SCREWDRIVER_PROBE = auto()
    S_SELECT_NEXT_OBJECT = auto()
    S_MOVE_TO_PRE_PLACE_POSE = auto()
    S_TABLE_PERCEIVE = auto()
    S_MOVE_TO_PICK_OBJECT = auto()
    S_CLOSE_GRIPPER = auto()
    S_MOVE_TO_PLACE_POSE = auto()
    S_OPEN_GRIPPER = auto()
    S_CONFIRM_DATA = auto()
    S_EXIT = auto()


# Transition IDs
class TransitionID(IntEnum):
    T_IDLE_INITIALIZE = 0
    T_IDLE_EXIT = auto()
    T_INITIALIZE_MOVE_TO_VIEW_POSE = auto()
    T_INITIALIZE_EXIT = auto()
    T_INITIALIZE_ABORT_EXIT = auto()
    T_MOVE_TO_VIEW_POSE_MOVE_ARM = auto()
    T_MOVE_TO_VIEW_POSE_EXIT = auto()
    T_MOVE_TO_VIEW_POSE_ABORT_EXIT = auto()
    T_GET_SUBDOOR_GET_OBJECTS = auto()
    T_GET_SUBDOOR_EXIT = auto()
    T_GET_SUBDOOR_ABORT_EXIT = auto()
    T_GET_OBJECTS_RASTER_SCAN = auto()
    T_GET_OBJECTS_EXIT = auto()
    T_GET_OBJECTS_ABORT_EXIT = auto()
    T_RASTER_SCAN_MOVE_TO_VIEW_POSE = auto()
    T_RASTER_SCAN_EXIT = auto()
    T_RASTER_SCAN_ABORT_EXIT = auto()
    T_EXECUTE_SCREWDRIVER_PROBE_SELECT_NEXT_OBJECT = auto()
    T_EXECUTE_SCREWDRIVER_PROBE_EXIT = auto()
    T_EXECUTE_SCREWDRIVER_PROBE_ABORT_EXIT = auto()
    T_MOVE_ARM_GET_SUBDOOR = auto()
    T_MOVE_ARM_EXECUTE_SCREWDRIVER_PROBE = auto()
    T_MOVE_ARM_TABLE_PERCEIVE = auto()
    T_MOVE_ARM_MOVE_TO_PRE_PLACE_POSE = auto()
    T_MOVE_ARM_MOVE_TO_PICK_OBJECT = auto()
    T_MOVE_ARM_CLOSE_GRIPPER = auto()
    T_MOVE_ARM_MOVE_TO_PLACE_POSE = auto()
    T_MOVE_ARM_OPEN_GRIPPER = auto()
    T_MOVE_ARM_SELECT_NEXT_OBJECT = auto()
    T_MOVE_ARM_CONFIRM_DATA = auto()
    T_MOVE_ARM_EXIT = auto()
    T_MOVE_ARM_ABORT_EXIT = auto()
    T_SELECT_NEXT_OBJECT_MOVE_TO_PRE_PLACE_POSE = auto()
    T_SELECT_NEXT_OBJECT_CONFIRM_DATA = auto()
    T_SELECT_NEXT_OBJECT_EXIT = auto()
    T_SELECT_NEXT_OBJECT_ABORT_EXIT = auto()
    T_MOVE_TO_PRE_PLACE_POSE_MOVE_ARM = auto()
    T_MOVE_TO_PRE_PLACE_POSE_EXIT = auto()
    T_MOVE_TO_PRE_PLACE_POSE_ABORT_EXIT = auto()
    T_TABLE_PERCEIVE_MOVE_TO_PRE_PLACE_POSE = auto()
    T_TABLE_PERCEIVE_EXIT = auto()
    T_TABLE_PERCEIVE_ABORT_EXIT = auto()
    T_MOVE_TO_PICK_OBJECT_MOVE_ARM = auto()
    T_MOVE_TO_PICK_OBJECT_EXIT = auto()
    T_MOVE_TO_PICK_OBJECT_ABORT_EXIT = auto()
    T_CLOSE_GRIPPER_RETREAT_ARM_WITH_OBJECT = auto()
    T_CLOSE_GRIPPER_EXIT = auto()
    T_CLOSE_GRIPPER_ABORT_EXIT = auto()
    T_MOVE_TO_PLACE_POSE_MOVE_ARM = auto()
    T_MOVE_TO_PLACE_POSE_EXIT = auto()
    T_MOVE_TO_PLACE_POSE_ABORT_EXIT = auto()
    T_OPEN_GRIPPER_MOVE_TO_PRE_PLACE_POSE = auto()
    T_OPEN_GRIPPER_EXIT = auto()
    T_OPEN_GRIPPER_ABORT_EXIT = auto()
    T_CONFIRM_DATA_IDLE = auto()
    T_CONFIRM_DATA_ABORT_EXIT = auto()


# Event reaction IDs
class ReactionID(IntEnum):
    R_E_START = 0
    R_E_ABORT_IDLE = auto()
    R_E_ABORT_INITIALIZE = auto()
    R_E_ABORT_MOVE_TO_VIEW_POSE = auto()
    R_E_ABORT_GET_SUBDOOR = auto()
    R_E_ABORT_RASTER_SCAN = auto()
    R_E_ABORT_MOVE_ARM = auto()
    R_E_ABORT_EXECUTE_SCREWDRIVER_PROBE = auto()
    R_E_ABORT_SELECT_NEXT_OBJECT = auto()
    R_E_ABORT_MOVE_TO_PRE_PLACE_POSE = auto()
    R_E_ABORT_TABLE_PERCEIVE = auto()
    R_E_ABORT_MOVE_TO_PICK_OBJECT = auto()
    R_E_ABORT_CLOSE_GRIPPER = auto()
    R_E_ABORT_MOVE_TO_PLACE_POSE = auto()
    R_E_ABORT_OPEN_GRIPPER = auto()
    R_E_ABORT_GET_OBJECTS = auto()
    R_E_ABORT_CONFIRM_DATA = auto()
    R_E_INIT_DONE = auto()
    R_E_INIT_FAIL = auto()
    R_E_VIEW_POSE_DONE = auto()
    R_E_VIEW_POSE_FAIL = auto()
    R_E_VIEW_POSE_FAIL_MOVE_ARM = auto()
    R_E_SUBDOOR_DONE = auto()
    R_E_SUBDOOR_FAIL = auto()
    R_E_OBJECTS_DONE = auto()
    R_E_OBJECTS_FAIL = auto()
    R_E_SCAN_DONE = auto()
    R_E_SCAN_FAIL = auto()
    R_E_SCREWDRIVER_PROBE_DONE = auto()
    R_E_SCREWDRIVER_PROBE_FAIL = auto()
    R_E_SCREWDRIVER_PROBE_FAIL_MOVE_ARM = auto()
    R_E_OBJECT_READY = auto()
    R_E_NO_MORE_OBJECTS = auto()
    R_E_PRE_PLACE_DONE = auto()
    R_E_TABLE_PERCEIVE_DONE = auto()
    R_E_TABLE_PERCEIVE_FAIL = auto()
    R_E_PRE_PLACE_BEFORE_PICK_DONE = auto()
    R_E_PICK_OBJECT_DONE = auto()
    R_E_PICK_OBJECT_RETREAT_DONE = auto()
    R_E_PRE_PLACE_WITH_OBJECT_DONE = auto()
    R_E_MOVE_TO_PLACE_DONE = auto()
    R_E_PRE_PLACE_AFTER_DROP_DONE = auto()
    R_E_ARM_MOVE_FAIL = auto()
    R_E_GRIPPER_CLOSE_DONE = auto()
    R_E_GRIPPER_CLOSE_FAIL = auto()
    R_E_GRIPPER_OPEN_DONE = auto()
    R_E_GRIPPER_OPEN_FAIL = auto()
    R_E_GO_MOVE_ARM_FROM_VIEW_POSE = auto()
    R_E_GO_MOVE_ARM_FROM_MOVE_TO_PRE_PLACE_POSE = auto()
    R_E_GO_MOVE_ARM_FROM_MOVE_TO_PICK_OBJECT = auto()
    R_E_GO_MOVE_ARM_FROM_MOVE_TO_PLACE_POSE = auto()
    R_E_PRE_PLACE_AFTER_DROP_FAIL = auto()
    R_E_CONFIRM_DONE = auto()


def create_fsm() -> FSMData:
    """Creates the FSM data structure."""
    # Transitions
    trans_dict = {
        TransitionID.T_IDLE_INITIALIZE: Transition(StateID.S_IDLE, StateID.S_INITIALIZE),
        TransitionID.T_IDLE_EXIT: Transition(StateID.S_IDLE, StateID.S_EXIT),
        TransitionID.T_INITIALIZE_MOVE_TO_VIEW_POSE: Transition(StateID.S_INITIALIZE, StateID.S_MOVE_TO_VIEW_POSE),
        TransitionID.T_INITIALIZE_EXIT: Transition(StateID.S_INITIALIZE, StateID.S_EXIT),
        TransitionID.T_INITIALIZE_ABORT_EXIT: Transition(StateID.S_INITIALIZE, StateID.S_EXIT),
        TransitionID.T_MOVE_TO_VIEW_POSE_MOVE_ARM: Transition(StateID.S_MOVE_TO_VIEW_POSE, StateID.S_MOVE_ARM),
        TransitionID.T_MOVE_TO_VIEW_POSE_EXIT: Transition(StateID.S_MOVE_TO_VIEW_POSE, StateID.S_EXIT),
        TransitionID.T_MOVE_TO_VIEW_POSE_ABORT_EXIT: Transition(StateID.S_MOVE_TO_VIEW_POSE, StateID.S_EXIT),
        TransitionID.T_GET_SUBDOOR_GET_OBJECTS: Transition(StateID.S_GET_SUBDOOR, StateID.S_GET_OBJECTS),
        TransitionID.T_GET_SUBDOOR_EXIT: Transition(StateID.S_GET_SUBDOOR, StateID.S_EXIT),
        TransitionID.T_GET_SUBDOOR_ABORT_EXIT: Transition(StateID.S_GET_SUBDOOR, StateID.S_EXIT),
        TransitionID.T_GET_OBJECTS_RASTER_SCAN: Transition(StateID.S_GET_OBJECTS, StateID.S_RASTER_SCAN),
        TransitionID.T_GET_OBJECTS_EXIT: Transition(StateID.S_GET_OBJECTS, StateID.S_EXIT),
        TransitionID.T_GET_OBJECTS_ABORT_EXIT: Transition(StateID.S_GET_OBJECTS, StateID.S_EXIT),
        TransitionID.T_RASTER_SCAN_MOVE_TO_VIEW_POSE: Transition(StateID.S_RASTER_SCAN, StateID.S_MOVE_TO_VIEW_POSE),
        TransitionID.T_RASTER_SCAN_EXIT: Transition(StateID.S_RASTER_SCAN, StateID.S_EXIT),
        TransitionID.T_RASTER_SCAN_ABORT_EXIT: Transition(StateID.S_RASTER_SCAN, StateID.S_EXIT),
        TransitionID.T_EXECUTE_SCREWDRIVER_PROBE_SELECT_NEXT_OBJECT: Transition(StateID.S_EXECUTE_SCREWDRIVER_PROBE, StateID.S_SELECT_NEXT_OBJECT),
        TransitionID.T_EXECUTE_SCREWDRIVER_PROBE_EXIT: Transition(StateID.S_EXECUTE_SCREWDRIVER_PROBE, StateID.S_EXIT),
        TransitionID.T_EXECUTE_SCREWDRIVER_PROBE_ABORT_EXIT: Transition(StateID.S_EXECUTE_SCREWDRIVER_PROBE, StateID.S_EXIT),
        TransitionID.T_MOVE_ARM_GET_SUBDOOR: Transition(StateID.S_MOVE_ARM, StateID.S_GET_SUBDOOR),
        TransitionID.T_MOVE_ARM_EXECUTE_SCREWDRIVER_PROBE: Transition(StateID.S_MOVE_ARM, StateID.S_EXECUTE_SCREWDRIVER_PROBE),
        TransitionID.T_MOVE_ARM_TABLE_PERCEIVE: Transition(StateID.S_MOVE_ARM, StateID.S_TABLE_PERCEIVE),
        TransitionID.T_MOVE_ARM_MOVE_TO_PRE_PLACE_POSE: Transition(StateID.S_MOVE_ARM, StateID.S_MOVE_TO_PRE_PLACE_POSE),
        TransitionID.T_MOVE_ARM_MOVE_TO_PICK_OBJECT: Transition(StateID.S_MOVE_ARM, StateID.S_MOVE_TO_PICK_OBJECT),
        TransitionID.T_MOVE_ARM_CLOSE_GRIPPER: Transition(StateID.S_MOVE_ARM, StateID.S_CLOSE_GRIPPER),
        TransitionID.T_MOVE_ARM_MOVE_TO_PLACE_POSE: Transition(StateID.S_MOVE_ARM, StateID.S_MOVE_TO_PLACE_POSE),
        TransitionID.T_MOVE_ARM_OPEN_GRIPPER: Transition(StateID.S_MOVE_ARM, StateID.S_OPEN_GRIPPER),
        TransitionID.T_MOVE_ARM_SELECT_NEXT_OBJECT: Transition(StateID.S_MOVE_ARM, StateID.S_SELECT_NEXT_OBJECT),
        TransitionID.T_MOVE_ARM_CONFIRM_DATA: Transition(StateID.S_MOVE_ARM, StateID.S_CONFIRM_DATA),
        TransitionID.T_MOVE_ARM_EXIT: Transition(StateID.S_MOVE_ARM, StateID.S_EXIT),
        TransitionID.T_MOVE_ARM_ABORT_EXIT: Transition(StateID.S_MOVE_ARM, StateID.S_EXIT),
        TransitionID.T_SELECT_NEXT_OBJECT_MOVE_TO_PRE_PLACE_POSE: Transition(StateID.S_SELECT_NEXT_OBJECT, StateID.S_MOVE_TO_PRE_PLACE_POSE),
        TransitionID.T_SELECT_NEXT_OBJECT_CONFIRM_DATA: Transition(StateID.S_SELECT_NEXT_OBJECT, StateID.S_CONFIRM_DATA),
        TransitionID.T_SELECT_NEXT_OBJECT_EXIT: Transition(StateID.S_SELECT_NEXT_OBJECT, StateID.S_EXIT),
        TransitionID.T_SELECT_NEXT_OBJECT_ABORT_EXIT: Transition(StateID.S_SELECT_NEXT_OBJECT, StateID.S_EXIT),
        TransitionID.T_MOVE_TO_PRE_PLACE_POSE_MOVE_ARM: Transition(StateID.S_MOVE_TO_PRE_PLACE_POSE, StateID.S_MOVE_ARM),
        TransitionID.T_MOVE_TO_PRE_PLACE_POSE_EXIT: Transition(StateID.S_MOVE_TO_PRE_PLACE_POSE, StateID.S_EXIT),
        TransitionID.T_MOVE_TO_PRE_PLACE_POSE_ABORT_EXIT: Transition(StateID.S_MOVE_TO_PRE_PLACE_POSE, StateID.S_EXIT),
        TransitionID.T_TABLE_PERCEIVE_MOVE_TO_PRE_PLACE_POSE: Transition(StateID.S_TABLE_PERCEIVE, StateID.S_MOVE_TO_PRE_PLACE_POSE),
        TransitionID.T_TABLE_PERCEIVE_EXIT: Transition(StateID.S_TABLE_PERCEIVE, StateID.S_EXIT),
        TransitionID.T_TABLE_PERCEIVE_ABORT_EXIT: Transition(StateID.S_TABLE_PERCEIVE, StateID.S_EXIT),
        TransitionID.T_MOVE_TO_PICK_OBJECT_MOVE_ARM: Transition(StateID.S_MOVE_TO_PICK_OBJECT, StateID.S_MOVE_ARM),
        TransitionID.T_MOVE_TO_PICK_OBJECT_EXIT: Transition(StateID.S_MOVE_TO_PICK_OBJECT, StateID.S_EXIT),
        TransitionID.T_MOVE_TO_PICK_OBJECT_ABORT_EXIT: Transition(StateID.S_MOVE_TO_PICK_OBJECT, StateID.S_EXIT),
        TransitionID.T_CLOSE_GRIPPER_RETREAT_ARM_WITH_OBJECT: Transition(StateID.S_CLOSE_GRIPPER, StateID.S_MOVE_TO_PICK_OBJECT),
        TransitionID.T_CLOSE_GRIPPER_EXIT: Transition(StateID.S_CLOSE_GRIPPER, StateID.S_EXIT),
        TransitionID.T_CLOSE_GRIPPER_ABORT_EXIT: Transition(StateID.S_CLOSE_GRIPPER, StateID.S_EXIT),
        TransitionID.T_MOVE_TO_PLACE_POSE_MOVE_ARM: Transition(StateID.S_MOVE_TO_PLACE_POSE, StateID.S_MOVE_ARM),
        TransitionID.T_MOVE_TO_PLACE_POSE_EXIT: Transition(StateID.S_MOVE_TO_PLACE_POSE, StateID.S_EXIT),
        TransitionID.T_MOVE_TO_PLACE_POSE_ABORT_EXIT: Transition(StateID.S_MOVE_TO_PLACE_POSE, StateID.S_EXIT),
        TransitionID.T_OPEN_GRIPPER_MOVE_TO_PRE_PLACE_POSE: Transition(StateID.S_OPEN_GRIPPER, StateID.S_MOVE_TO_PRE_PLACE_POSE),
        TransitionID.T_OPEN_GRIPPER_EXIT: Transition(StateID.S_OPEN_GRIPPER, StateID.S_EXIT),
        TransitionID.T_OPEN_GRIPPER_ABORT_EXIT: Transition(StateID.S_OPEN_GRIPPER, StateID.S_EXIT),
        TransitionID.T_CONFIRM_DATA_IDLE: Transition(StateID.S_CONFIRM_DATA, StateID.S_IDLE),
        TransitionID.T_CONFIRM_DATA_ABORT_EXIT: Transition(StateID.S_CONFIRM_DATA, StateID.S_EXIT),
    }
    trans_list = [trans_dict[i] for i in TransitionID]

    # Event Reactions
    evt_reaction_dict = {
        ReactionID.R_E_START: EventReaction(
            condition_event_index=EventID.E_START,
            transition_index=TransitionID.T_IDLE_INITIALIZE,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_IDLE: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_IDLE_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_INITIALIZE: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_INITIALIZE_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_MOVE_TO_VIEW_POSE: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_MOVE_TO_VIEW_POSE_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_GET_SUBDOOR: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_GET_SUBDOOR_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_RASTER_SCAN: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_RASTER_SCAN_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_MOVE_ARM: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_MOVE_ARM_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_EXECUTE_SCREWDRIVER_PROBE: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_EXECUTE_SCREWDRIVER_PROBE_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_SELECT_NEXT_OBJECT: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_SELECT_NEXT_OBJECT_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_MOVE_TO_PRE_PLACE_POSE: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_MOVE_TO_PRE_PLACE_POSE_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_TABLE_PERCEIVE: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_TABLE_PERCEIVE_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_MOVE_TO_PICK_OBJECT: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_MOVE_TO_PICK_OBJECT_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_CLOSE_GRIPPER: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_CLOSE_GRIPPER_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_MOVE_TO_PLACE_POSE: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_MOVE_TO_PLACE_POSE_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_OPEN_GRIPPER: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_OPEN_GRIPPER_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_GET_OBJECTS: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_GET_OBJECTS_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ABORT_CONFIRM_DATA: EventReaction(
            condition_event_index=EventID.E_ABORT,
            transition_index=TransitionID.T_CONFIRM_DATA_ABORT_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_INIT_DONE: EventReaction(
            condition_event_index=EventID.E_INIT_DONE,
            transition_index=TransitionID.T_INITIALIZE_MOVE_TO_VIEW_POSE,
            fired_event_indices=[],
        ),
        ReactionID.R_E_INIT_FAIL: EventReaction(
            condition_event_index=EventID.E_INIT_FAIL,
            transition_index=TransitionID.T_INITIALIZE_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_VIEW_POSE_DONE: EventReaction(
            condition_event_index=EventID.E_VIEW_POSE_DONE,
            transition_index=TransitionID.T_MOVE_ARM_GET_SUBDOOR,
            fired_event_indices=[],
        ),
        ReactionID.R_E_VIEW_POSE_FAIL: EventReaction(
            condition_event_index=EventID.E_VIEW_POSE_FAIL,
            transition_index=TransitionID.T_MOVE_TO_VIEW_POSE_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_VIEW_POSE_FAIL_MOVE_ARM: EventReaction(
            condition_event_index=EventID.E_VIEW_POSE_FAIL,
            transition_index=TransitionID.T_MOVE_ARM_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_SUBDOOR_DONE: EventReaction(
            condition_event_index=EventID.E_SUBDOOR_DONE,
            transition_index=TransitionID.T_GET_SUBDOOR_GET_OBJECTS,
            fired_event_indices=[],
        ),
        ReactionID.R_E_SUBDOOR_FAIL: EventReaction(
            condition_event_index=EventID.E_SUBDOOR_FAIL,
            transition_index=TransitionID.T_GET_SUBDOOR_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_OBJECTS_DONE: EventReaction(
            condition_event_index=EventID.E_OBJECTS_DONE,
            transition_index=TransitionID.T_GET_OBJECTS_RASTER_SCAN,
            fired_event_indices=[],
        ),
        ReactionID.R_E_OBJECTS_FAIL: EventReaction(
            condition_event_index=EventID.E_OBJECTS_FAIL,
            transition_index=TransitionID.T_GET_OBJECTS_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_SCAN_DONE: EventReaction(
            condition_event_index=EventID.E_SCAN_DONE,
            transition_index=TransitionID.T_RASTER_SCAN_MOVE_TO_VIEW_POSE,
            fired_event_indices=[],
        ),
        ReactionID.R_E_SCAN_FAIL: EventReaction(
            condition_event_index=EventID.E_SCAN_FAIL,
            transition_index=TransitionID.T_RASTER_SCAN_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_SCREWDRIVER_PROBE_DONE: EventReaction(
            condition_event_index=EventID.E_SCREWDRIVER_PROBE_DONE,
            transition_index=TransitionID.T_EXECUTE_SCREWDRIVER_PROBE_SELECT_NEXT_OBJECT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_SCREWDRIVER_PROBE_FAIL: EventReaction(
            condition_event_index=EventID.E_SCREWDRIVER_PROBE_FAIL,
            transition_index=TransitionID.T_EXECUTE_SCREWDRIVER_PROBE_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_SCREWDRIVER_PROBE_FAIL_MOVE_ARM: EventReaction(
            condition_event_index=EventID.E_SCREWDRIVER_PROBE_FAIL,
            transition_index=TransitionID.T_MOVE_ARM_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_OBJECT_READY: EventReaction(
            condition_event_index=EventID.E_OBJECT_READY,
            transition_index=TransitionID.T_SELECT_NEXT_OBJECT_MOVE_TO_PRE_PLACE_POSE,
            fired_event_indices=[],
        ),
        ReactionID.R_E_NO_MORE_OBJECTS: EventReaction(
            condition_event_index=EventID.E_NO_MORE_OBJECTS,
            transition_index=TransitionID.T_SELECT_NEXT_OBJECT_CONFIRM_DATA,
            fired_event_indices=[],
        ),
        ReactionID.R_E_PRE_PLACE_DONE: EventReaction(
            condition_event_index=EventID.E_PRE_PLACE_DONE,
            transition_index=TransitionID.T_MOVE_ARM_TABLE_PERCEIVE,
            fired_event_indices=[],
        ),
        ReactionID.R_E_TABLE_PERCEIVE_DONE: EventReaction(
            condition_event_index=EventID.E_TABLE_PERCEIVE_DONE,
            transition_index=TransitionID.T_TABLE_PERCEIVE_MOVE_TO_PRE_PLACE_POSE,
            fired_event_indices=[],
        ),
        ReactionID.R_E_TABLE_PERCEIVE_FAIL: EventReaction(
            condition_event_index=EventID.E_TABLE_PERCEIVE_FAIL,
            transition_index=TransitionID.T_TABLE_PERCEIVE_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_PRE_PLACE_BEFORE_PICK_DONE: EventReaction(
            condition_event_index=EventID.E_PRE_PLACE_BEFORE_PICK_DONE,
            transition_index=TransitionID.T_MOVE_ARM_MOVE_TO_PICK_OBJECT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_PICK_OBJECT_DONE: EventReaction(
            condition_event_index=EventID.E_PICK_OBJECT_DONE,
            transition_index=TransitionID.T_MOVE_ARM_CLOSE_GRIPPER,
            fired_event_indices=[],
        ),
        ReactionID.R_E_PICK_OBJECT_RETREAT_DONE: EventReaction(
            condition_event_index=EventID.E_PICK_OBJECT_RETREAT_DONE,
            transition_index=TransitionID.T_MOVE_ARM_MOVE_TO_PRE_PLACE_POSE,
            fired_event_indices=[],
        ),
        ReactionID.R_E_PRE_PLACE_WITH_OBJECT_DONE: EventReaction(
            condition_event_index=EventID.E_PRE_PLACE_WITH_OBJECT_DONE,
            transition_index=TransitionID.T_MOVE_ARM_MOVE_TO_PLACE_POSE,
            fired_event_indices=[],
        ),
        ReactionID.R_E_MOVE_TO_PLACE_DONE: EventReaction(
            condition_event_index=EventID.E_MOVE_TO_PLACE_DONE,
            transition_index=TransitionID.T_MOVE_ARM_OPEN_GRIPPER,
            fired_event_indices=[],
        ),
        ReactionID.R_E_PRE_PLACE_AFTER_DROP_DONE: EventReaction(
            condition_event_index=EventID.E_PRE_PLACE_AFTER_DROP_DONE,
            transition_index=TransitionID.T_MOVE_ARM_SELECT_NEXT_OBJECT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_ARM_MOVE_FAIL: EventReaction(
            condition_event_index=EventID.E_ARM_MOVE_FAIL,
            transition_index=TransitionID.T_MOVE_ARM_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_GRIPPER_CLOSE_DONE: EventReaction(
            condition_event_index=EventID.E_GRIPPER_CLOSE_DONE,
            transition_index=TransitionID.T_CLOSE_GRIPPER_RETREAT_ARM_WITH_OBJECT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_GRIPPER_CLOSE_FAIL: EventReaction(
            condition_event_index=EventID.E_GRIPPER_FAIL,
            transition_index=TransitionID.T_CLOSE_GRIPPER_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_GRIPPER_OPEN_DONE: EventReaction(
            condition_event_index=EventID.E_GRIPPER_OPEN_DONE,
            transition_index=TransitionID.T_OPEN_GRIPPER_MOVE_TO_PRE_PLACE_POSE,
            fired_event_indices=[],
        ),
        ReactionID.R_E_GRIPPER_OPEN_FAIL: EventReaction(
            condition_event_index=EventID.E_GRIPPER_FAIL,
            transition_index=TransitionID.T_OPEN_GRIPPER_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_GO_MOVE_ARM_FROM_VIEW_POSE: EventReaction(
            condition_event_index=EventID.E_GO_MOVE_ARM,
            transition_index=TransitionID.T_MOVE_TO_VIEW_POSE_MOVE_ARM,
            fired_event_indices=[],
        ),
        ReactionID.R_E_GO_MOVE_ARM_FROM_MOVE_TO_PRE_PLACE_POSE: EventReaction(
            condition_event_index=EventID.E_GO_MOVE_ARM,
            transition_index=TransitionID.T_MOVE_TO_PRE_PLACE_POSE_MOVE_ARM,
            fired_event_indices=[],
        ),
        ReactionID.R_E_GO_MOVE_ARM_FROM_MOVE_TO_PICK_OBJECT: EventReaction(
            condition_event_index=EventID.E_GO_MOVE_ARM,
            transition_index=TransitionID.T_MOVE_TO_PICK_OBJECT_MOVE_ARM,
            fired_event_indices=[],
        ),
        ReactionID.R_E_GO_MOVE_ARM_FROM_MOVE_TO_PLACE_POSE: EventReaction(
            condition_event_index=EventID.E_GO_MOVE_ARM,
            transition_index=TransitionID.T_MOVE_TO_PLACE_POSE_MOVE_ARM,
            fired_event_indices=[],
        ),
        ReactionID.R_E_PRE_PLACE_AFTER_DROP_FAIL: EventReaction(
            condition_event_index=EventID.E_PRE_PLACE_AFTER_DROP_FAIL,
            transition_index=TransitionID.T_MOVE_TO_PRE_PLACE_POSE_EXIT,
            fired_event_indices=[],
        ),
        ReactionID.R_E_CONFIRM_DONE: EventReaction(
            condition_event_index=EventID.E_CONFIRM_DONE,
            transition_index=TransitionID.T_CONFIRM_DATA_IDLE,
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
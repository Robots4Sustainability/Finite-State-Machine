#!/usr/bin/env python3
import argparse
import re
import subprocess
from pathlib import Path


SECTION_MARKERS = [
    "STATES:",
    "EVENTS:",
    "TRANSITIONS:",
    "REACTIONS:",
]


# Extract the text belonging to a named top-level FSM section.
def section_text(text: str, section_name: str) -> str:
    start = text.find(section_name)
    if start == -1:
        return ""
    start += len(section_name)
    end = len(text)
    for marker in SECTION_MARKERS:
        if marker == section_name:
            continue
        idx = text.find(marker, start)
        if idx != -1 and idx < end:
            end = idx
    return text[start:end]


# Parse all state identifiers from the FSM definition.
def parse_states(text: str):
    states_block = section_text(text, "STATES:")
    return re.findall(r"\bS_[A-Z0-9_]+\b", states_block)


# Parse a single @ReferencedName value for a scalar key.
def parse_scalar_ref(text: str, key: str):
    match = re.search(rf"{re.escape(key)}\s*:\s*@(\w+)", text)
    return match.group(1) if match else None


# Parse transition blocks and collect their source and target states.
def parse_transitions(text: str):
    transitions = {}
    pattern = re.compile(
        r"^\s*(T_[A-Z0-9_]+):\s*$"
        r"(.*?)"
        r"(?=^\s*T_[A-Z0-9_]+:\s*$|^\s*REACTIONS:|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    for name, block in pattern.findall(text):
        from_match = re.search(r"FROM:\s*@(\w+)", block)
        to_match = re.search(r"TO:\s*@(\w+)", block)
        if from_match and to_match:
            transitions[name] = {
                "from": from_match.group(1),
                "to": to_match.group(1),
            }
    return transitions


# Map each transition to the event names that trigger it.
def parse_reactions(text: str):
    transition_events = {}
    pattern = re.compile(
        r"^\s*(R_[A-Z0-9_]+):\s*$"
        r"(.*?)"
        r"(?=^\s*R_[A-Z0-9_]+:\s*$|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    for _, block in pattern.findall(section_text(text, "REACTIONS:")):
        when_match = re.search(r"WHEN:\s*@(\w+)", block)
        do_match = re.search(r"DO:\s*@(\w+)", block)
        if when_match and do_match:
            transition_events.setdefault(do_match.group(1), []).append(when_match.group(1))
    return transition_events


# Format a state name into a multi-line node label.
def state_label(state_name: str):
    return state_name.replace("S_", "").replace("_", "\\n")


# Format one or more event names into an edge label.
def event_label(event_names):
    if not event_names:
        return ""
    return "\\n".join(name.replace("E_", "") for name in event_names)


# Build the Graphviz DOT source for the FSM diagram.
def build_dot(states, start_state, end_state, transitions, transition_events, title):
    lines = [
        "digraph door_fsm {",
        '  graph [rankdir=LR, splines=true, overlap=false, pad="0.8", nodesep="1.3", ranksep="1.9"];',
        '  node [shape=box, style="rounded,filled", fillcolor="#F8FAFC", color="#334155", '
        'fontname="Helvetica", fontsize=24, penwidth=1.6, margin="0.35,0.25", width=2.6, height=1.2];',
        '  edge [color="#475569", fontname="Helvetica", fontsize=20, penwidth=1.5, arrowsize=1.1];',
        f'  labelloc="t";',
        f'  label="{title}";',
        '  fontsize=28;',
        '  start [shape=point, width=0.22, color="#16A34A"];',
    ]

    for state in states:
        attrs = []
        if state == start_state:
            attrs.append('fillcolor="#DCFCE7"')
            attrs.append('color="#16A34A"')
        elif state == end_state:
            attrs.append('fillcolor="#FEE2E2"')
            attrs.append('color="#DC2626"')
        else:
            attrs.append('fillcolor="#EFF6FF"')
        attr_text = ", ".join(attrs)
        lines.append(f'  {state} [label="{state_label(state)}", {attr_text}];')

    if start_state:
        lines.append(f"  start -> {start_state};")

    for transition_name, transition in transitions.items():
        source = transition["from"]
        target = transition["to"]
        label = event_label(transition_events.get(transition_name, []))
        edge_attrs = []
        if label:
            edge_attrs.append(f'label="{label}"')
        if target == end_state:
            edge_attrs.append('style="dashed"')
            edge_attrs.append('color="#94A3B8"')
            edge_attrs.append('fontcolor="#64748B"')
        elif source == "S_MOVE_ARM" or target == "S_MOVE_ARM":
            edge_attrs.append('color="#0F766E"')
            edge_attrs.append('fontcolor="#0F766E"')
        attr_text = ""
        if edge_attrs:
            attr_text = " [" + ", ".join(edge_attrs) + "]"
        lines.append(f"  {source} -> {target}{attr_text};")

    lines.append("}")
    return "\n".join(lines) + "\n"


# Parse arguments, build the diagram, and render the PNG.
def main():
    parser = argparse.ArgumentParser(description="Generate a clean Graphviz diagram for a coord_dsl FSM.")
    parser.add_argument("fsm_file", help="Path to the .fsm file")
    parser.add_argument("--png-output", help="Path to write the PNG image")
    args = parser.parse_args()

    fsm_path = Path(args.fsm_file).resolve()
    text = fsm_path.read_text(encoding="utf-8")

    states = parse_states(text)
    start_state = parse_scalar_ref(text, "START_STATE")
    end_state = parse_scalar_ref(text, "END_STATE")
    transitions = parse_transitions(text)
    transition_events = parse_reactions(text)

    stem = fsm_path.with_suffix("")
    png_output = Path(args.png_output).resolve() if args.png_output else stem.with_name(stem.name + "_diagram.png")

    dot_text = build_dot(
        states=states,
        start_state=start_state,
        end_state=end_state,
        transitions=transitions,
        transition_events=transition_events,
        title=fsm_path.stem,
    )
    subprocess.run(["dot", "-Tpng", "-Gdpi=220", "-o", str(png_output)], input=dot_text, text=True, check=True)
    print(f"PNG: {png_output}")


if __name__ == "__main__":
    main()

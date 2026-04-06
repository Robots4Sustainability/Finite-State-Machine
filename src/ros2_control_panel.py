#!/usr/bin/env python3
import os
import queue
import re
import shlex
import signal
import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Optional


@dataclass
class ProcessSpec:
    key: str
    label: str
    command: str
    category: str
    autostart: bool = False
    required_for: tuple[str, ...] = ()
    use_coord_venv: bool = False


class ManagedProcess:
    def __init__(
        self,
        spec: ProcessSpec,
        on_output: Optional[Callable[[str, str], None]] = None,
        on_exit: Optional[Callable[[str, int], None]] = None,
    ):
        self.spec = spec
        self.on_output = on_output
        self.on_exit = on_exit
        self.proc: Optional[subprocess.Popen] = None
        self.thread: Optional[threading.Thread] = None
        self.stop_requested = False
        self.log_lines: list[str] = []
        self.log_windows: list[tk.Text] = []

    def is_running(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    def attach_log_widget(self, widget: tk.Text) -> None:
        self.log_windows.append(widget)
        if self.log_lines:
            widget.insert(tk.END, "".join(self.log_lines))
            widget.see(tk.END)

    def detach_log_widget(self, widget: tk.Text) -> None:
        self.log_windows = [w for w in self.log_windows if w != widget]

    def append_log(self, text: str) -> None:
        self.log_lines.append(text)
        if len(self.log_lines) > 3000:
            self.log_lines = self.log_lines[-3000:]

        for widget in list(self.log_windows):
            try:
                widget.after(0, lambda w=widget, t=text: self._append_to_widget(w, t))
            except Exception:
                pass

        if self.on_output is not None:
            self.on_output(self.spec.key, text)

    def _append_to_widget(self, widget: tk.Text, text: str) -> None:
        widget.insert(tk.END, text)
        widget.see(tk.END)

    def start(self, setup_script: str, coord_venv_cmd: str = "") -> None:
        if self.is_running():
            self.append_log(f"[{self.spec.label}] already running.\n")
            return

        self.stop_requested = False
        setup_parts = [f"source {shlex.quote(setup_script)}"]
        if self.spec.use_coord_venv and coord_venv_cmd.strip():
            setup_parts.append(coord_venv_cmd.strip())
        setup_parts.append(self.spec.command)
        shell_cmd = " && ".join(setup_parts)

        self.proc = subprocess.Popen(
            ["/bin/bash", "-lc", shell_cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1,
            preexec_fn=os.setsid,
        )
        self.append_log(f"\n--- START {self.spec.label} ---\n$ {shell_cmd}\n")
        self.thread = threading.Thread(target=self._pump_output, daemon=True)
        self.thread.start()

    def _pump_output(self) -> None:
        if self.proc is None or self.proc.stdout is None:
            return

        for line in self.proc.stdout:
            self.append_log(f"[{self.spec.label}] {line}")

        rc = self.proc.wait()
        self.append_log(f"--- EXIT {self.spec.label} (code={rc}) ---\n")
        if self.on_exit is not None:
            self.on_exit(self.spec.key, rc)

    def send_stdin(self, text: str) -> None:
        if not self.is_running() or self.proc is None or self.proc.stdin is None:
            self.append_log(f"[{self.spec.label}] not running; stdin skipped.\n")
            return
        try:
            self.proc.stdin.write(text)
            self.proc.stdin.flush()
        except Exception as exc:
            self.append_log(f"[{self.spec.label}] stdin failed: {exc}\n")

    def stop(self) -> None:
        if not self.is_running() or self.proc is None:
            return
        self.stop_requested = True
        try:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGINT)
        except ProcessLookupError:
            pass

    def kill(self) -> None:
        if not self.is_running() or self.proc is None:
            return
        try:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass


class ControlPanelApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ROS 2 Control Panel")
        self.root.geometry("1680x900") # Not sure about the aspect ratio yet :( 

        self.ws_default = self._find_workspace_root()
        self.setup_default = str(Path(self.ws_default) / "install" / "setup.bash")

        self.process_specs = [
            ProcessSpec(
                key="zenoh",
                label="Zenoh",
                command="ros2 run rmw_zenoh_cpp rmw_zenohd",
                category="Core",
            ),
            ProcessSpec(
                key="simulation",
                label="Simulation",
                command="ros2 launch eddie_ros eddie.launch.py use_sim:=true arm_select:=right show_rviz:=true",
                category="Core",
            ),
            ProcessSpec(
                key="planner",
                label="Cartesian Planner",
                command="ros2 run cartesian_planner spline_planner",
                category="Core",
            ),
            ProcessSpec(
                key="mock_server",
                label="Mock Perception Server",
                command="ros2 run pick_place_fsm mock_perception_server",
                category="FSM",
            ),
            ProcessSpec(
                key="main_fsm_with_screwdriver",
                label="Main FSM (with screwdriver)",
                command="ros2 run pick_place_fsm door_disassemble",
                category="FSM",
                required_for=("screwdriver",),
                use_coord_venv=True,
            ),
            ProcessSpec(
                key="main_fsm_without_screwdriver",
                label="Main FSM (without screwdriver)",
                command="ros2 run pick_place_fsm door_disassemble --ros-args -p screwdriver_probe:=false",
                category="FSM",
                use_coord_venv=True,
            ),
            ProcessSpec(
                key="screwdriver",
                label="Screwdriver Probe",
                command="ros2 run pick_place_fsm screwdriver_pick",
                category="FSM",
            ),
            ProcessSpec(
                key="pose_capture",
                label="Pose Capture",
                command="ros2 run pick_place_fsm pose_capturer",
                category="Tools",
            ),
            ProcessSpec(
                key="slip_detection",
                label="Object Slip Detection",
                command="ros2 run pick_place_fsm error_handling",
                category="Tools",
            ),
        ]

        self.processes: Dict[str, ManagedProcess] = {}
        self.status_vars: Dict[str, tk.StringVar] = {}
        self.autostart_core_var = tk.BooleanVar(value=False)
        self.fsm_state_var = tk.StringVar(value="IDLE")
        self.fsm_phase_var = tk.StringVar(value="Waiting")
        self.fsm_detail_var = tk.StringVar(value="No FSM output yet")
        self.ui_queue: queue.Queue[tuple[str, str, str]] = queue.Queue()
        self.log_toplevels: Dict[str, tk.Toplevel] = {}

        self._build_ui()
        self._build_processes()
        self._tick_status()
        self._drain_ui_queue()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _find_workspace_root(self) -> str:
        cwd = Path.cwd()
        for candidate in [cwd, *cwd.parents]:
            if (candidate / "install" / "setup.bash").exists():
                return str(candidate)
        return str(cwd)

    def _build_ui(self) -> None:
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill=tk.X)

        ttk.Label(top, text="Workspace:").grid(row=0, column=0, sticky="w")
        self.ws_var = tk.StringVar(value=self.ws_default)
        ttk.Entry(top, textvariable=self.ws_var, width=72).grid(row=0, column=1, sticky="ew", padx=6)

        ttk.Label(top, text="Setup script:").grid(row=1, column=0, sticky="w")
        self.setup_var = tk.StringVar(value=self.setup_default)
        ttk.Entry(top, textvariable=self.setup_var, width=72).grid(row=1, column=1, sticky="ew", padx=6)

        ttk.Label(top, text="Coord DSL venv:").grid(row=2, column=0, sticky="w")
        self.coord_venv_var = tk.StringVar(value="source .venv_coord_dsl/bin/activate")
        ttk.Entry(top, textvariable=self.coord_venv_var, width=72).grid(row=2, column=1, sticky="ew", padx=6)

        ttk.Checkbutton(top, text="Autostart core on launch", variable=self.autostart_core_var).grid(row=0, column=2, padx=8)
        ttk.Button(top, text="Start core stack", command=self.start_core_stack).grid(row=0, column=3, padx=4)
        ttk.Button(top, text="Stop all", command=self.stop_all).grid(row=1, column=3, padx=4)

        top.columnconfigure(1, weight=1)

        middle = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        middle.pack(fill=tk.BOTH, expand=True)
        middle.columnconfigure(0, weight=0)
        middle.columnconfigure(1, weight=1)
        middle.rowconfigure(0, weight=1)

        left = ttk.Frame(middle, padding=8, width=780)
        right = ttk.Frame(middle, padding=8)
        left.grid(row=0, column=0, sticky="nsw")
        right.grid(row=0, column=1, sticky="nsew")
        left.grid_propagate(False)

        ttk.Label(left, text="Processes", font=("TkDefaultFont", 11, "bold")).pack(anchor="w", pady=(0, 6))
        self.process_frame = ttk.Frame(left)
        self.process_frame.pack(fill=tk.BOTH, expand=True)

        quick = ttk.LabelFrame(left, text="Quick actions", padding=8)
        quick.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(quick, text="Send ENTER to main FSM", command=self.send_enter_to_fsm).pack(fill=tk.X, pady=2)
        ttk.Button(quick, text="Abort main FSM (send 'a')", command=self.abort_fsm).pack(fill=tk.X, pady=2)
        ttk.Button(quick, text="Start screwdriver flow stack", command=self.start_screwdriver_stack).pack(fill=tk.X, pady=2)
        ttk.Button(quick, text="Start no-screwdriver flow stack", command=self.start_no_screwdriver_stack).pack(fill=tk.X, pady=2)

        status_box = ttk.LabelFrame(right, text="FSM status", padding=10)
        status_box.pack(fill=tk.BOTH, expand=True)

        ttk.Label(status_box, text="Current FSM state", font=("TkDefaultFont", 11, "bold")).pack(anchor="w")
        ttk.Label(status_box, textvariable=self.fsm_state_var, font=("TkDefaultFont", 18, "bold")).pack(anchor="w", pady=(0, 10))

        ttk.Label(status_box, text="Current phase", font=("TkDefaultFont", 11, "bold")).pack(anchor="w")
        ttk.Label(status_box, textvariable=self.fsm_phase_var, font=("TkDefaultFont", 14)).pack(anchor="w", pady=(0, 10))

        ttk.Label(status_box, text="Latest detail", font=("TkDefaultFont", 11, "bold")).pack(anchor="w")
        ttk.Label(status_box, textvariable=self.fsm_detail_var, wraplength=780, justify="left").pack(anchor="w", fill=tk.X, pady=(0, 16))

        ttk.Button(status_box, text="Open Simulation log", command=lambda: self.open_log_window("simulation")).pack(anchor="w", pady=8)

        if self.autostart_core_var.get():
            self.root.after(500, self.start_core_stack)

    def _build_processes(self) -> None:
        for spec in self.process_specs:
            self.processes[spec.key] = ManagedProcess(spec, self._handle_process_output, self._handle_process_exit)

        categories = ["Core", "FSM", "Tools"]
        row = 0
        for category in categories:
            box = ttk.LabelFrame(self.process_frame, text=category, padding=6)
            box.grid(row=row, column=0, sticky="ew", pady=4)
            row += 1

            entries = [s for s in self.process_specs if s.category == category]
            for i, spec in enumerate(entries):
                self.status_vars[spec.key] = tk.StringVar(value="STOPPED")
                ttk.Label(box, text=spec.label, width=28).grid(row=i, column=0, sticky="w", padx=4, pady=3)
                ttk.Label(box, textvariable=self.status_vars[spec.key], width=12).grid(row=i, column=1, sticky="w", padx=4)
                ttk.Button(box, text="Start", command=lambda s=spec: self.start_process(s.key)).grid(row=i, column=2, padx=2)
                ttk.Button(box, text="Stop", command=lambda s=spec: self.stop_process(s.key)).grid(row=i, column=3, padx=2)
                ttk.Button(box, text="Restart", command=lambda s=spec: self.restart_process(s.key)).grid(row=i, column=4, padx=2)
                ttk.Button(box, text="Open log", command=lambda s=spec: self.open_log_window(s.key)).grid(row=i, column=5, padx=2)

        self.process_frame.columnconfigure(0, weight=1)

    def _handle_process_output(self, key: str, text: str) -> None:
        self.ui_queue.put(("output", key, text))

    def _handle_process_exit(self, key: str, rc: int) -> None:
        self.ui_queue.put(("exit", key, str(rc)))

    def _drain_ui_queue(self) -> None:
        try:
            while True:
                event, key, payload = self.ui_queue.get_nowait()
                if event == "output":
                    self._update_fsm_status_from_output(key, payload)
        except queue.Empty:
            pass
        self.root.after(150, self._drain_ui_queue)

    def _update_fsm_status_from_output(self, key: str, text: str) -> None:
        if key not in {"main_fsm_with_screwdriver", "main_fsm_without_screwdriver"}:
            return

        match = re.search(r"State changed to:\s*([A-Z0-9_]+)", text)
        if match:
            self.fsm_state_var.set(match.group(1))
            self.fsm_detail_var.set(text.strip())
            return

        lowered = text.lower()
        phase_rules = [
            ("initializing", "Initialize"),
            ("moving arm to global view pose", "Move to view pose"),
            ("requesting subdoor poses", "Perceive subdoor"),
            ("requesting car object poses", "Perceive car objects"),
            ("calling raster scan service", "Raster scan"),
            ("triggered screwdriver routine", "Screwdriver probe"),
            ("moving to pre-place pose", "Move to pre-place pose"),
            ("requesting place pose", "Table perceive"),
            ("executing pick approach", "Pick object"),
            ("close gripper on object", "Close gripper"),
            ("moving to place pose", "Move to place pose"),
            ("open gripper to drop object", "Drop object"),
            ("confirm step reached", "Confirm data"),
            ("press enter to start", "Waiting for start"),
        ]
        for needle, phase in phase_rules:
            if needle in lowered:
                self.fsm_phase_var.set(phase)
                self.fsm_detail_var.set(text.strip())
                return

        if text.strip():
            self.fsm_detail_var.set(text.strip())

    def get_setup_script(self) -> str:
        setup_script = self.setup_var.get().strip()
        if not setup_script:
            raise RuntimeError("setup.bash path is empty")
        if not Path(setup_script).exists():
            raise RuntimeError(f"setup script not found: {setup_script}")
        return setup_script

    def get_coord_venv_command(self) -> str:
        return self.coord_venv_var.get().strip()

    def start_process(self, key: str) -> None:
        try:
            setup_script = self.get_setup_script()
        except RuntimeError as exc:
            messagebox.showerror("Invalid setup", str(exc))
            return

        spec = self.processes[key].spec
        for dependency in spec.required_for:
            if not self.processes[dependency].is_running():
                self.processes[dependency].start(setup_script, self.get_coord_venv_command())
                time.sleep(0.3)

        self.processes[key].start(setup_script, self.get_coord_venv_command())

    def stop_process(self, key: str) -> None:
        self.processes[key].stop()

    def restart_process(self, key: str) -> None:
        self.stop_process(key)
        self.root.after(800, lambda: self.start_process(key))

    def start_core_stack(self) -> None:
        for key in ["zenoh", "simulation", "planner"]:
            self.start_process(key)
            time.sleep(0.2)

    def start_screwdriver_stack(self) -> None:
        for key in ["mock_server", "screwdriver", "slip_detection", "main_fsm_with_screwdriver"]:
            self.start_process(key)
            time.sleep(0.2)

    def start_no_screwdriver_stack(self) -> None:
        for key in ["mock_server", "slip_detection", "main_fsm_without_screwdriver"]:
            self.start_process(key)
            time.sleep(0.2)

    def send_enter_to_fsm(self) -> None:
        if self.processes["main_fsm_with_screwdriver"].is_running():
            self.processes["main_fsm_with_screwdriver"].send_stdin("\n")
        elif self.processes["main_fsm_without_screwdriver"].is_running():
            self.processes["main_fsm_without_screwdriver"].send_stdin("\n")
        else:
            messagebox.showinfo("FSM", "No main FSM process is running.")

    def abort_fsm(self) -> None:
        if self.processes["main_fsm_with_screwdriver"].is_running():
            self.processes["main_fsm_with_screwdriver"].send_stdin("a\n")
        elif self.processes["main_fsm_without_screwdriver"].is_running():
            self.processes["main_fsm_without_screwdriver"].send_stdin("a\n")
        else:
            messagebox.showinfo("FSM", "No main FSM process is running.")

    def open_log_window(self, key: str) -> None:
        proc = self.processes[key]
        existing = self.log_toplevels.get(key)
        if existing is not None and existing.winfo_exists():
            existing.lift()
            return

        top = tk.Toplevel(self.root)
        top.title(f"Log - {proc.spec.label}")
        top.geometry("980x520")
        self.log_toplevels[key] = top

        header = ttk.Frame(top, padding=8)
        header.pack(fill=tk.X)
        ttk.Label(header, text=proc.spec.label, font=("TkDefaultFont", 11, "bold")).pack(side=tk.LEFT)

        text_widget = tk.Text(top, wrap="none")
        text_widget.pack(fill=tk.BOTH, expand=True)
        proc.attach_log_widget(text_widget)

        ttk.Button(header, text="Clear", command=lambda: self._clear_process_log(key, text_widget)).pack(side=tk.RIGHT)

        def _close() -> None:
            proc.detach_log_widget(text_widget)
            if key in self.log_toplevels:
                del self.log_toplevels[key]
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", _close)

    def _clear_process_log(self, key: str, widget: tk.Text) -> None:
        self.processes[key].log_lines.clear()
        widget.delete("1.0", tk.END)

    def stop_all(self) -> None:
        for proc in self.processes.values():
            proc.stop()

    def _tick_status(self) -> None:
        for key, managed in self.processes.items():
            self.status_vars[key].set("RUNNING" if managed.is_running() else "STOPPED")
        self.root.after(500, self._tick_status)

    def on_close(self) -> None:
        self.stop_all()
        self.root.after(1000, self.root.destroy)


def main() -> None:
    root = tk.Tk()
    app = ControlPanelApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

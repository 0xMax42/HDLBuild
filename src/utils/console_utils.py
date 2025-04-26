import threading
import time
import subprocess
from typing import List, Optional

from rich.console import Console
from rich.live import Live
from rich.text import Text

class ConsoleTask:
    def __init__(self, prefix:str, title: str, step_number: Optional[int] = None, total_steps: Optional[int] = None,  max_log_lines: int = 10):
        self.prefix = prefix
        self.title = title
        self.step_number = step_number
        self.total_steps = total_steps
        self.max_log_lines = max_log_lines
        self.spinner_cycle = ['|', '/', '-', '\\']
        self.stop_event = threading.Event()
        self.spinner_thread: Optional[threading.Thread] = None
        self.output_lines: List[str] = []
        self._stdout_lock = threading.Lock()
        self.console = Console()
        self.live: Optional[Live] = None
        self.spinner_idx = 0

    def start_spinner(self):
        self.live = Live(console=self.console, refresh_per_second=30, transient=True)
        self.live.start()
        self.spinner_thread = threading.Thread(target=self._spinner_task, daemon=True)
        self.spinner_thread.start()

    def _spinner_task(self):
        while not self.stop_event.is_set():
            with self._stdout_lock:
                self._redraw_spinner()
            self.spinner_idx += 1
            time.sleep(0.1)

    def _render_content(self) -> Text:
        visible_lines = self.output_lines[-self.max_log_lines:]

        prefix_text = f"[grey50]\[{self.prefix}][/grey50]" if self.prefix else ""
        step_text = f"[bold blue]Step {self.step_number}/{self.total_steps}[/bold blue]" if self.step_number and self.total_steps else ""
        title_text = f"[bold]{self.title}[/bold]" if self.title else ""

        spinner_markup = f"{prefix_text} {step_text} {title_text} {self.spinner_cycle[self.spinner_idx % len(self.spinner_cycle)]}"

        spinner_text = Text.from_markup(spinner_markup)
        log_text = Text("\n".join(visible_lines))

        full_text = spinner_text + Text("\n") + log_text

        return full_text

    def _redraw_spinner(self):
        if self.live:
            self.live.update(self._render_content())

    def log(self, message: str):
        with self._stdout_lock:
            self.output_lines.append(message)
            if len(self.output_lines) > self.max_log_lines:
                self.output_lines = self.output_lines[-self.max_log_lines:]
            
            if self.live:
                self.live.update(self._render_content())


    def run_command(self, cmd: List[str], cwd: Optional[str] = None, silent: bool = False) -> int:
        success = False
        start_time = time.time()

        self.start_spinner()

        try:
            if silent:
                subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                success = True
            else:
                process = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                if process.stdout is None:
                    raise ValueError("Failed to capture stdout")

                while True:
                    line = process.stdout.readline()
                    if not line and process.poll() is not None:
                        break
                    if line:
                        self.log(line.rstrip())

                success = (process.returncode == 0)
                if not success:
                    raise subprocess.CalledProcessError(process.returncode, cmd)

        except subprocess.CalledProcessError:
            success = False
            raise
        finally:
            self.stop_event.set()
            if self.spinner_thread:
                self.spinner_thread.join()

            duration = time.time() - start_time

            # Finalize output
            with self._stdout_lock:
                self._finalize_output(success, duration)

        return 0 if success else 1

    def _finalize_output(self, success: bool, duration: float):
        if self.live:
            self.live.stop()

        prefix_text = f"[grey50]\[{self.prefix}][/grey50]" if self.prefix else ""
        status_symbol = "[green]✅[/green]" if success else "[red]❌[/red]"
        step_text = f"[bold blue]Step {self.step_number}/{self.total_steps}[/bold blue]" if self.step_number and self.total_steps else ""
        status_title = f"[bold green]{self.title}[/bold green]" if success else f"[bold red]{self.title}[/bold red]"
        final_line = f"{prefix_text} {step_text} {status_title} {status_symbol} [bold green]({duration:.1f}s[/bold green])"

        # Final full output
        self.console.print(final_line)

class ConsoleUtils:
    def __init__(self,
        prefix: str = "",
        step_number: Optional[int] = None,
        total_steps: Optional[int] = None
    ):
        self.prefix = prefix
        self.step_number = step_number
        self.total_steps = total_steps
        self.console = Console()

    def print(self, message: str):
        prefix = f"[grey50]\[{self.prefix}][/grey50]" if self.prefix else ""
        step_info = f"[bold blue]Step {self.step_number}/{self.total_steps}[/bold blue]" if self.step_number and self.total_steps else ""
        message_text = f"{prefix} {step_info} {message}"
        self.console.print(message_text)
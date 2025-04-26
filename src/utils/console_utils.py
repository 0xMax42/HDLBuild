import sys
import threading
import time
import subprocess
from typing import List, Optional

class ConsoleTask:
    def __init__(self, title: str, max_log_lines: int = 10):
        self.title = title
        self.max_log_lines = max_log_lines
        self.spinner_cycle = ['|', '/', '-', '\\']
        self.stop_event = threading.Event()
        self.spinner_thread: Optional[threading.Thread] = None
        self.output_lines: List[str] = []
        self._stdout_lock = threading.Lock()
        self._drawn_lines = 0  # Track only real drawn lines, no pre-reservation anymore

    def start_spinner(self):
        self.spinner_thread = threading.Thread(target=self._spinner_task, daemon=True)
        self.spinner_thread.start()

    def _spinner_task(self):
        idx = 0
        while not self.stop_event.is_set():
            with self._stdout_lock:
                self._redraw_spinner(idx)
            idx += 1
            time.sleep(0.1)

    def _redraw_spinner(self, idx: int):
        visible_lines = self.output_lines[-self.max_log_lines:]

        # Clear only previously drawn lines
        if self._drawn_lines > 0:
            sys.stdout.write(f"\033[{self._drawn_lines}F")  # Move cursor up

            for _ in range(self._drawn_lines):
                sys.stdout.write("\r\033[K")  # Clear line
                sys.stdout.write("\033[1B")   # Move cursor one line down

            sys.stdout.write(f"\033[{self._drawn_lines}F")  # Move cursor up to redraw start

        # Draw fresh content
        self._drawn_lines = 0  # Reset counter

        # Draw spinner line
        sys.stdout.write(f"\r{self.title} {self.spinner_cycle[idx % len(self.spinner_cycle)]}\n")
        self._drawn_lines += 1

        # Draw log lines
        for line in visible_lines:
            sys.stdout.write(line + "\n")
            self._drawn_lines += 1

        sys.stdout.flush()

    def log(self, message: str):
        with self._stdout_lock:
            self.output_lines.append(message)
            if len(self.output_lines) > self.max_log_lines:
                self.output_lines = self.output_lines[-self.max_log_lines:]

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

            # Final redraw after stop
            with self._stdout_lock:
                self._finalize_output(success, duration)

        return 0 if success else 1

    def _finalize_output(self, success: bool, duration: float):
        visible_lines = self.output_lines[-self.max_log_lines:]

        # Clear last drawn area
        if self._drawn_lines > 0:
            sys.stdout.write(f"\033[{self._drawn_lines}F")
            for _ in range(self._drawn_lines):
                sys.stdout.write("\r\033[K")
                sys.stdout.write("\033[1B")
            sys.stdout.write(f"\033[{self._drawn_lines}F")

        self._drawn_lines = 0  # Reset

        # Write final status line
        status = "\033[92m✅\033[0m" if success else "\033[91m❌\033[0m"
        sys.stdout.write(f"\r{self.title} {status} ({duration:.1f}s)\n")
        self._drawn_lines += 1

        sys.stdout.flush()

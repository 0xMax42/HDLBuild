import shutil
import subprocess
import os
import threading
import time
import sys
from typing import Optional, List
from models.project import ProjectConfig
from models.config import DIRECTORIES
from utils.console_utils import ConsoleTask

def run_tool(
    project: ProjectConfig,
    tool_executable_name: str,
    mandatory_arguments: List[str],
    tool_option_attr: Optional[str] = None,
    working_dir: Optional[str] = None,
    silent: bool = False,
    step_number: Optional[int] = None,
    total_steps: Optional[int] = None
):
    if working_dir is None:
        working_dir = DIRECTORIES.build

    xilinx_bin_dir = os.path.join(project.xilinx_path, "bin", "lin64")
    tool_executable = os.path.join(xilinx_bin_dir, tool_executable_name)

    if not os.path.exists(tool_executable):
        raise FileNotFoundError(f"Executable nicht gefunden: {tool_executable}")

    step_info = f"[{step_number}/{total_steps}] " if step_number and total_steps else ""
    progress_line = f"{step_info}[hdlbuild] Starte {tool_executable_name.upper()}..."

    cmd = [tool_executable]

    if project.tool_options and project.tool_options.common:
        cmd.extend(project.tool_options.common)

    if tool_option_attr and project.tool_options:
        tool_opts = getattr(project.tool_options, tool_option_attr, [])
        if tool_opts:
            cmd.extend(tool_opts)

    cmd.extend(mandatory_arguments)

    task = ConsoleTask(progress_line)
    task.run_command(cmd, cwd=working_dir, silent=silent)


def copy_report_file(
    project: ProjectConfig,
    source_filename: str,
    destination_filename: str,
    description: str = "Report"
):
    """
    Kopiert eine beliebige Report-Datei vom Build- in das Report-Verzeichnis.

    Args:
        project (ProjectConfig): Geladene Projektkonfiguration
        source_filename (str): Name der Quelldatei im Build-Ordner
        destination_filename (str): Neuer Name der Zieldatei im Report-Ordner
        description (str): Optionale Beschreibung für die Ausgabe (z.B. "Synthesis Report")
    """
    src_path = os.path.join(DIRECTORIES.build, source_filename)
    dst_path = os.path.join(DIRECTORIES.report, destination_filename)

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"{description} nicht gefunden: {src_path}")

    os.makedirs(DIRECTORIES.report, exist_ok=True)

    shutil.copyfile(src_path, dst_path)
    print(f"[hdlbuild] {description} kopiert nach {dst_path} 🗎")
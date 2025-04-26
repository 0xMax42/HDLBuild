import shutil
import os
from typing import Optional, List
from hdlbuild.models.project import ProjectConfig
from hdlbuild.models.config import DIRECTORIES
from hdlbuild.utils.console_utils import ConsoleTask, ConsoleUtils
from rich.console import Console

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

    cmd = [tool_executable]

    if project.tool_options and project.tool_options.common:
        cmd.extend(project.tool_options.common)

    if tool_option_attr and project.tool_options:
        tool_opts = getattr(project.tool_options, tool_option_attr, [])
        if tool_opts:
            cmd.extend(tool_opts)

    cmd.extend(mandatory_arguments)

    task = ConsoleTask("hdlbuild", tool_executable_name.upper(), step_number, total_steps)
    task.run_command(cmd, cwd=working_dir, silent=silent)


def copy_file(
    project: ProjectConfig,
    source_filename: str,
    destination_filename: str,
    description: str = "Report",
    step_number: Optional[int] = None,
    total_steps: Optional[int] = None
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

    util = ConsoleUtils("hdlbuild", step_number, total_steps)
    util.print(f"{description} kopiert nach {dst_path}")
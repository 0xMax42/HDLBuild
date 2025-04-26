import subprocess
import os
import shutil
from typing import Optional
from models.project import ProjectConfig
from models.config import DIRECTORIES
from tools.xilinx_ise.common import run_tool

def run_bitgen(project: ProjectConfig):
    run_tool(
        project=project,
        tool_executable_name="bitgen",
        tool_option_attr="bitgen",
        mandatory_arguments=[
            "-w",
            f"{project.name}.ncd",
            f"{project.name}.bit"
        ], step_number=5, total_steps=6
    )


def copy_bitstream_file(project: ProjectConfig):
    """
    Kopiert die Bitstream-Datei (.bit) vom Build-Verzeichnis ins Output-Verzeichnis.
    
    Args:
        project (ProjectConfig): Geladene Projektkonfiguration.
    """
    src_path = os.path.join(DIRECTORIES.build, f"{project.name}.bit")
    dst_path = os.path.join(DIRECTORIES.copy_target, f"{project.name}.bit")

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Bitstream-Datei nicht gefunden: {src_path}")

    os.makedirs(DIRECTORIES.copy_target, exist_ok=True)

    shutil.copyfile(src_path, dst_path)
    print(f"[hdlbuild] Bitstream-Datei kopiert nach {dst_path}")
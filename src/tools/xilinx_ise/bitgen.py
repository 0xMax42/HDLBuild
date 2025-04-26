import subprocess
import os
import shutil
from typing import Optional
from models.project import ProjectConfig
from models.config import DIRECTORIES
from tools.xilinx_ise.common import copy_file, run_tool

def run_bitgen(project: ProjectConfig):
    run_tool(
        project=project,
        tool_executable_name="bitgen",
        tool_option_attr="bitgen",
        mandatory_arguments=[
            "-w",
            f"{project.name}.ncd",
            f"{project.name}.bit"
        ], step_number=9, total_steps=12
    )


def copy_bitstream_file(project: ProjectConfig):
    copy_file(
        project=project,
        source_filename=f"{project.name}.bit",
        destination_filename=f"{project.name}.Bitstream",
        description="Bitstream File",
        step_number=10, total_steps=12
    )
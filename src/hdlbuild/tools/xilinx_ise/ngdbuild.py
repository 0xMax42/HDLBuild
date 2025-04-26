import subprocess
import os
from typing import Optional
from hdlbuild.models.project import ProjectConfig
from hdlbuild.models.config import DIRECTORIES
from hdlbuild.tools.xilinx_ise.common import run_tool

def run_ngdbuild(project: ProjectConfig):
    run_tool(
        project=project,
        tool_executable_name="ngdbuild",
        tool_option_attr="ngdbuild",
        mandatory_arguments=[
            "-p", project.target_device,
            "-uc", f"{DIRECTORIES.get_relative_prefix()}{project.constraints}",
            f"{project.name}.ngc",
            f"{project.name}.ngd"
        ], step_number=3, total_steps=12
    )

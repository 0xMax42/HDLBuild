import subprocess
import shutil
import os
from typing import Optional
from models.project import ProjectConfig
from models.config import DIRECTORIES
from tools.xilinx_ise.common import copy_file, run_tool

def run_par(project: ProjectConfig):
    run_tool(
        project=project,
        tool_executable_name="par",
        tool_option_attr="par",
        mandatory_arguments=[
            "-w",
            f"{project.name}.map.ncd",
            f"{project.name}.ncd",
            f"{project.name}.pcf"
        ], step_number=6, total_steps=12
    )

def copy_par_report(project: ProjectConfig):
    copy_file(
        project=project,
        source_filename=f"{project.name}.par",
        destination_filename=f"{project.name}.PlaceRouteReport",
        description="Place & Route Report",
        step_number=7, total_steps=12
    )

def copy_pinout_report(project: ProjectConfig):
    copy_file(
        project=project,
        source_filename=f"{project.name}_pad.txt",
        destination_filename=f"{project.name}.PinoutReport",
        description="Pinout Report",
        step_number=8, total_steps=12
    )
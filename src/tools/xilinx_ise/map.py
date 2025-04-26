import subprocess
import os
import shutil
from typing import Optional
from models.project import ProjectConfig
from models.config import DIRECTORIES
from tools.xilinx_ise.common import copy_file, run_tool

def run_map(project: ProjectConfig):
    run_tool(
        project=project,
        tool_executable_name="map",
        tool_option_attr="map",
        mandatory_arguments=[
            "-p", project.target_device,
            "-w",
            f"{project.name}.ngd",
            "-o", f"{project.name}.map.ncd",
            f"{project.name}.pcf"
        ], step_number=4, total_steps=12
    )

def copy_map_report(project: ProjectConfig):
    copy_file(
        project=project,
        source_filename=f"{project.name}.map.mrp",
        destination_filename=f"{project.name}.MapReport",
        description="Map Report",
        step_number=5, total_steps=12
    )

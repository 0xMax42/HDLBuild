import subprocess
import os
import shutil
from typing import Optional
from hdlbuild.models.project import ProjectConfig
from hdlbuild.models.config import DIRECTORIES
from hdlbuild.tools.xilinx_ise.common import copy_file, run_tool

def run_trace(project: ProjectConfig):
    run_tool(
        project=project,
        tool_executable_name="trce",
        tool_option_attr="trace",
        mandatory_arguments=[
            f"{project.name}.ncd",
            f"{project.name}.pcf",
        ], step_number=11, total_steps=12
    )

def copy_trace_report(project: ProjectConfig):
    copy_file(
        project=project,
        source_filename=f"{project.name}.twr",
        destination_filename=f"{project.name}.TimingReport",
        description="Timing Report", 
        step_number=12, total_steps=12
    )

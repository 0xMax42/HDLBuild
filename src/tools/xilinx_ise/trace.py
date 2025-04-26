import subprocess
import os
import shutil
from typing import Optional
from models.project import ProjectConfig
from models.config import DIRECTORIES
from tools.xilinx_ise.common import copy_report_file, run_tool

def run_trace(project: ProjectConfig):
    run_tool(
        project=project,
        tool_executable_name="trce",
        tool_option_attr="trace",
        mandatory_arguments=[
            f"{project.name}.ncd",
            f"{project.name}.pcf",
        ], step_number=6, total_steps=6
    )

def copy_trace_report(project: ProjectConfig):
    copy_report_file(
        project=project,
        source_filename=f"{project.name}.twr",
        destination_filename=f"{project.name}.TimingReport",
        description="Timing Report"
    )

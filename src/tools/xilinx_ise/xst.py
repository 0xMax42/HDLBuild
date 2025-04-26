from typing import Optional
from models.config import DIRECTORIES
from tools.xilinx_ise.common import copy_report_file, run_tool
from utils.source_resolver import expand_sources
from models.project import ProjectConfig
import subprocess
import os
import shutil

def generate_xst_project_file(project: ProjectConfig, output_path: str):
    """
    Generiert die XST .prj-Datei mit allen Quellcodes.
    """
    with open(output_path, "w") as f:
        # VHDL-Sources
        for lib, src in expand_sources(project.sources.vhdl):
            f.write(f"vhdl {lib} \"{DIRECTORIES.get_relative_prefix()}/{src}\"\n")
        # Verilog-Sources
        for lib, src in expand_sources(project.sources.verilog):
            f.write(f"verilog {lib} \"{DIRECTORIES.get_relative_prefix()}/{src}\"\n")
        
        # Optionale Dependencies
        if project.dependencies:
            for dep in project.dependencies:
                # Hier könnte man noch spezielle Sources aus dep.path expandieren
                pass

def generate_xst_script_file(project: ProjectConfig, output_path: str):
    """
    Generiert die XST .scr-Datei mit den Synthese-Optionen.
    """
    with open(output_path, "w") as f:
        f.write(f"run ")
        f.write(f"-ifn {project.name}.prj ")
        f.write(f"-ofn {project.name}.ngc ")
        f.write(f"-ifmt mixed ")

        if project.tool_options and project.tool_options.xst:
            for opt in project.tool_options.xst:
                f.write(f"{opt} ")

        f.write(f"-top {project.topmodule} ")
        f.write(f"-ofmt NGC ")
        f.write(f"-p {project.target_device} ")



def run_xst(project: ProjectConfig):
    run_tool(
        project=project,
        tool_executable_name="xst",
        mandatory_arguments=["-ifn", f"{project.name}.scr"]
    )

def copy_synthesis_report(project: ProjectConfig):
    copy_report_file(
        project=project,
        source_filename=f"{project.name}.srp",
        destination_filename=f"{project.name}.SynthesisReport",
        description="Synthesebericht"
    )
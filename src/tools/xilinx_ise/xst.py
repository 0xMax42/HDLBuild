from typing import Optional
from models.config import DIRECTORIES
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



def run_xst(project: ProjectConfig, working_dir: Optional[str] = None):
    """
    Führt Xilinx XST Synthese aus, basierend auf dem gegebenen Projekt.
    
    Args:
        project (ProjectConfig): Geladene Projektkonfiguration.
        working_dir (str, optional): Pfad, wo .prj/.scr liegen und gebaut werden soll.
                                     Wenn None, wird das aktuelle Arbeitsverzeichnis verwendet.
    """
    if working_dir is None:
        working_dir = DIRECTORIES.build

    xilinx_bin_dir = os.path.join(project.xilinx_path, "bin", "lin64")  # oder "nt64" für Windows
    xst_executable = os.path.join(xilinx_bin_dir, "xst")

    if not os.path.exists(xst_executable):
        raise FileNotFoundError(f"XST-Executable nicht gefunden unter: {xst_executable}")

    print(f"[hdlbuild] Starte XST Synthese über {xst_executable}")
    print(f"[hdlbuild] Arbeitsverzeichnis: {working_dir}")

    cmd = [xst_executable]

    # Füge die "common" Optionen ein, wenn sie existieren
    if project.tool_options and project.tool_options.common:
        cmd.extend(project.tool_options.common)

    # Jetzt die XST-spezifischen Aufrufe
    cmd.extend([
        "-ifn", f"{project.name}.scr"
    ])

    print(f"[hdlbuild] XST-Befehl: {' '.join(cmd)}")

    subprocess.run(cmd, cwd=working_dir, check=True)

def copy_synthesis_report(project: ProjectConfig):
    """
    Kopiert den Synthesebericht (.srp) vom Build-Verzeichnis ins Report-Verzeichnis
    und benennt ihn sinnvoll um.
    
    Args:
        project (ProjectConfig): Geladene Projektkonfiguration.
    """
    src_path = os.path.join(DIRECTORIES.build, f"{project.name}.srp")
    dst_path = os.path.join(DIRECTORIES.report, f"{project.name}.SynthesisReport")

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Synthesebericht nicht gefunden: {src_path}")

    # Stelle sicher, dass das Zielverzeichnis existiert
    os.makedirs(DIRECTORIES.report, exist_ok=True)

    shutil.copyfile(src_path, dst_path)
    print(f"[hdlbuild] Synthesebericht kopiert nach {dst_path}")
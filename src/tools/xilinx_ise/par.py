import subprocess
import shutil
import os
from typing import Optional
from models.project import ProjectConfig
from models.config import DIRECTORIES

def run_par(project: ProjectConfig, working_dir: Optional[str] = None):
    """
    Führt Xilinx PAR (Place & Route) aus, basierend auf dem gegebenen Projekt.
    
    Args:
        project (ProjectConfig): Geladene Projektkonfiguration.
        working_dir (str, optional): Arbeitsverzeichnis; Standard: build-Verzeichnis.
    """
    if working_dir is None:
        working_dir = DIRECTORIES.build

    xilinx_bin_dir = os.path.join(project.xilinx_path, "bin", "lin64")  # oder "nt64" für Windows
    par_executable = os.path.join(xilinx_bin_dir, "par")

    if not os.path.exists(par_executable):
        raise FileNotFoundError(f"PAR-Executable nicht gefunden unter: {par_executable}")

    print(f"[hdlbuild] Starte PAR über {par_executable}")
    print(f"[hdlbuild] Arbeitsverzeichnis: {working_dir}")

    cmd = [par_executable]

    # Füge zuerst die "common" Optionen ein (falls vorhanden)
    if project.tool_options and project.tool_options.common:
        cmd.extend(project.tool_options.common)

    # Dann die PAR-spezifischen Optionen
    if project.tool_options and project.tool_options.par:
        cmd.extend(project.tool_options.par)

    # Dann die Pflicht-Argumente
    cmd.extend([
        "-w",
        f"{project.name}.map.ncd",
        f"{project.name}.ncd",
        f"{project.name}.pcf"
    ])


    subprocess.run(cmd, cwd=working_dir, check=True)

def copy_par_report(project: ProjectConfig):
    """
    Kopiert den Place & Route Report (.par) vom Build-Verzeichnis ins Report-Verzeichnis
    und benennt ihn sinnvoll um.
    
    Args:
        project (ProjectConfig): Geladene Projektkonfiguration.
    """
    src_path = os.path.join(DIRECTORIES.build, f"{project.name}.par")
    dst_path = os.path.join(DIRECTORIES.report, f"{project.name}.PlaceRouteReport")

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"PAR-Report nicht gefunden: {src_path}")

    os.makedirs(DIRECTORIES.report, exist_ok=True)

    shutil.copyfile(src_path, dst_path)
    print(f"[hdlbuild] PAR-Report kopiert nach {dst_path}")

def copy_pinout_report(project: ProjectConfig):
    """
    Kopiert den Pinout Summary Report (_pad.txt) vom Build-Verzeichnis ins Report-Verzeichnis
    und benennt ihn sinnvoll um.
    
    Args:
        project (ProjectConfig): Geladene Projektkonfiguration.
    """
    src_path = os.path.join(DIRECTORIES.build, f"{project.name}_pad.txt")
    dst_path = os.path.join(DIRECTORIES.report, f"{project.name}.PinoutReport")

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Pinout-Report nicht gefunden: {src_path}")

    os.makedirs(DIRECTORIES.report, exist_ok=True)

    shutil.copyfile(src_path, dst_path)
    print(f"[hdlbuild] Pinout-Report kopiert nach {dst_path}")
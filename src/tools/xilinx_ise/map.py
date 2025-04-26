import subprocess
import os
import shutil
from typing import Optional
from models.project import ProjectConfig
from models.config import DIRECTORIES

def run_map(project: ProjectConfig, working_dir: Optional[str] = None):
    """
    Führt Xilinx MAP aus, basierend auf dem gegebenen Projekt.
    
    Args:
        project (ProjectConfig): Geladene Projektkonfiguration.
        working_dir (str, optional): Arbeitsverzeichnis; Standard: build-Verzeichnis.
    """
    if working_dir is None:
        working_dir = DIRECTORIES.build

    xilinx_bin_dir = os.path.join(project.xilinx_path, "bin", "lin64")  # oder "nt64" für Windows
    map_executable = os.path.join(xilinx_bin_dir, "map")

    if not os.path.exists(map_executable):
        raise FileNotFoundError(f"MAP-Executable nicht gefunden unter: {map_executable}")

    print(f"[hdlbuild] Starte MAP über {map_executable}")
    print(f"[hdlbuild] Arbeitsverzeichnis: {working_dir}")

    cmd = [map_executable]

    # Füge zuerst die "common" Optionen ein (falls vorhanden)
    if project.tool_options and project.tool_options.common:
        cmd.extend(project.tool_options.common)

    # Dann die MAP-spezifischen Optionen
    if project.tool_options and project.tool_options.map:
        cmd.extend(project.tool_options.map)

    # Dann die Pflicht-Argumente
    cmd.extend([
        "-p", project.target_device,
        "-w",
        f"{project.name}.ngd",
        "-o", f"{project.name}.map.ncd",
        f"{project.name}.pcf"
    ])


    subprocess.run(cmd, cwd=working_dir, check=True)

def copy_map_report(project: ProjectConfig):
    """
    Kopiert den Map-Report (.map.mrp) vom Build-Verzeichnis ins Report-Verzeichnis
    und benennt ihn sinnvoll um.
    
    Args:
        project (ProjectConfig): Geladene Projektkonfiguration.
    """
    src_path = os.path.join(DIRECTORIES.build, f"{project.name}.map.mrp")
    dst_path = os.path.join(DIRECTORIES.report, f"{project.name}.MapReport")

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Map-Report nicht gefunden: {src_path}")

    os.makedirs(DIRECTORIES.report, exist_ok=True)

    shutil.copyfile(src_path, dst_path)
    print(f"[hdlbuild] Map-Report kopiert nach {dst_path}")
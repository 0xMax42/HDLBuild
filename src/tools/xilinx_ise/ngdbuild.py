import subprocess
import os
from typing import Optional
from models.project import ProjectConfig
from models.config import DIRECTORIES

def run_ngdbuild(project: ProjectConfig, working_dir: Optional[str] = None):
    """
    Führt Xilinx NGDBuild aus, basierend auf dem gegebenen Projekt.
    
    Args:
        project (ProjectConfig): Geladene Projektkonfiguration.
        working_dir (str, optional): Arbeitsverzeichnis; Standard: build-Verzeichnis.
    """
    if working_dir is None:
        working_dir = DIRECTORIES.build

    xilinx_bin_dir = os.path.join(project.xilinx_path, "bin", "lin64")  # oder "nt64" für Windows
    ngdbuild_executable = os.path.join(xilinx_bin_dir, "ngdbuild")

    if not os.path.exists(ngdbuild_executable):
        raise FileNotFoundError(f"NGDBuild-Executable nicht gefunden unter: {ngdbuild_executable}")

    print(f"[hdlbuild] Starte NGDBuild über {ngdbuild_executable}")
    print(f"[hdlbuild] Arbeitsverzeichnis: {working_dir}")

    cmd = [ngdbuild_executable]

    # Füge zuerst die "common" Optionen ein (falls vorhanden)
    if project.tool_options and project.tool_options.common:
        cmd.extend(project.tool_options.common)

    # Dann die NGDBuild-spezifischen Optionen
    if project.tool_options and project.tool_options.ngdbuild:
        cmd.extend(project.tool_options.ngdbuild)

    # Dann die Pflicht-Argumente
    cmd.extend([
        "-p", project.target_device,
        "-uc", f"{DIRECTORIES.get_relative_prefix()}{project.constraints}",
        f"{project.name}.ngc",
        f"{project.name}.ngd"
    ])


    subprocess.run(cmd, cwd=working_dir, check=True)

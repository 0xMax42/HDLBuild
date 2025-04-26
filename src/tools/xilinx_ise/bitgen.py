import subprocess
import os
import shutil
from typing import Optional
from models.project import ProjectConfig
from models.config import DIRECTORIES

def run_bitgen(project: ProjectConfig, working_dir: Optional[str] = None):
    """
    Führt Xilinx BitGen aus, um den finalen Bitstream zu erzeugen.
    
    Args:
        project (ProjectConfig): Geladene Projektkonfiguration.
        working_dir (str, optional): Arbeitsverzeichnis; Standard: build-Verzeichnis.
    """
    if working_dir is None:
        working_dir = DIRECTORIES.build

    xilinx_bin_dir = os.path.join(project.xilinx_path, "bin", "lin64")  # oder "nt64" für Windows
    bitgen_executable = os.path.join(xilinx_bin_dir, "bitgen")

    if not os.path.exists(bitgen_executable):
        raise FileNotFoundError(f"BitGen-Executable nicht gefunden unter: {bitgen_executable}")

    print(f"[hdlbuild] Starte BitGen über {bitgen_executable}")
    print(f"[hdlbuild] Arbeitsverzeichnis: {working_dir}")

    cmd = [bitgen_executable]

    # Füge zuerst die "common" Optionen ein (falls vorhanden)
    if project.tool_options and project.tool_options.common:
        cmd.extend(project.tool_options.common)

    # Dann die BitGen-spezifischen Optionen
    if project.tool_options and project.tool_options.bitgen:
        cmd.extend(project.tool_options.bitgen)

    # Dann die Pflicht-Argumente
    cmd.extend([
        "-w",
        f"{project.name}.ncd",
        f"{project.name}.bit"
    ])

    subprocess.run(cmd, cwd=working_dir, check=True)

def copy_bitstream_file(project: ProjectConfig):
    """
    Kopiert die Bitstream-Datei (.bit) vom Build-Verzeichnis ins Output-Verzeichnis.
    
    Args:
        project (ProjectConfig): Geladene Projektkonfiguration.
    """
    src_path = os.path.join(DIRECTORIES.build, f"{project.name}.bit")
    dst_path = os.path.join(DIRECTORIES.copy_target, f"{project.name}.bit")

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Bitstream-Datei nicht gefunden: {src_path}")

    os.makedirs(DIRECTORIES.copy_target, exist_ok=True)

    shutil.copyfile(src_path, dst_path)
    print(f"[hdlbuild] Bitstream-Datei kopiert nach {dst_path}")
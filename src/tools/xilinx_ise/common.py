import shutil
import subprocess
import os
from typing import Optional, List
from models.project import ProjectConfig
from models.config import DIRECTORIES

def run_tool(
    project: ProjectConfig,
    tool_executable_name: str,
    mandatory_arguments: List[str],
    tool_option_attr: Optional[str] = None,
    working_dir: Optional[str] = None
):
    """
    Führt ein beliebiges Xilinx ISE Tool aus (XST, NGDBuild, MAP, PAR, BitGen),
    mit Common- und ggf. Toolspezifischen Optionen + festen Pflichtargumenten.

    Args:
        project (ProjectConfig): Das Projekt-Objekt
        tool_executable_name (str): z.B. "xst", "map", "par", "bitgen"
        mandatory_arguments (List[str]): Liste mit Pflicht-Argumenten
        tool_option_attr (Optional[str]): Attribut-Name in tool_options, z.B. "xst", "map"
        working_dir (Optional[str]): Arbeitsverzeichnis
    """
    if working_dir is None:
        working_dir = DIRECTORIES.build

    xilinx_bin_dir = os.path.join(project.xilinx_path, "bin", "lin64")  # oder "nt64"
    tool_executable = os.path.join(xilinx_bin_dir, tool_executable_name)

    if not os.path.exists(tool_executable):
        raise FileNotFoundError(f"Executable nicht gefunden: {tool_executable}")

    print(f"[hdlbuild] Starte {tool_executable_name.upper()} über {tool_executable}")
    print(f"[hdlbuild] Arbeitsverzeichnis: {working_dir}")

    cmd = [tool_executable]

    # Füge zuerst "common" Optionen ein
    if project.tool_options and project.tool_options.common:
        cmd.extend(project.tool_options.common)

    # Füge dann Toolspezifische Optionen ein (nur wenn angegeben)
    if tool_option_attr and project.tool_options:
        tool_opts = getattr(project.tool_options, tool_option_attr, [])
        if tool_opts:
            cmd.extend(tool_opts)

    # Füge die Pflicht-Argumente an
    cmd.extend(mandatory_arguments)

    print(f"[hdlbuild] Befehl: {' '.join(cmd)}")

    subprocess.run(cmd, cwd=working_dir, check=True)

def copy_report_file(
    project: ProjectConfig,
    source_filename: str,
    destination_filename: str,
    description: str = "Report"
):
    """
    Kopiert eine beliebige Report-Datei vom Build- in das Report-Verzeichnis.

    Args:
        project (ProjectConfig): Geladene Projektkonfiguration
        source_filename (str): Name der Quelldatei im Build-Ordner
        destination_filename (str): Neuer Name der Zieldatei im Report-Ordner
        description (str): Optionale Beschreibung für die Ausgabe (z.B. "Synthesis Report")
    """
    src_path = os.path.join(DIRECTORIES.build, source_filename)
    dst_path = os.path.join(DIRECTORIES.report, destination_filename)

    if not os.path.exists(src_path):
        raise FileNotFoundError(f"{description} nicht gefunden: {src_path}")

    os.makedirs(DIRECTORIES.report, exist_ok=True)

    shutil.copyfile(src_path, dst_path)
    print(f"[hdlbuild] {description} kopiert nach {dst_path}")
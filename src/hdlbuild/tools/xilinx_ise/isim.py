import os
from typing import List

from hdlbuild.models.project import ProjectConfig
from hdlbuild.models.config import DIRECTORIES
from hdlbuild.dependencies.resolver import DependencyResolver
from hdlbuild.utils.console_utils import ConsoleTask
from hdlbuild.utils.source_resolver import expand_all_sources, expand_testbenches

def generate_simulation_project_file(project: ProjectConfig, output_path: str, testbench_name: str):
    """
    Generiert die ISim Simulationsprojektdatei (.prj).

    Args:
        project (ProjectConfig): Das Hauptprojekt.
        output_path (str): Zielpfad für die .prj Datei.
        testbench_name (str): Name der Testbench-Datei (z.B. "VGATimingGenerator_test_tb").
    """
    resolver = DependencyResolver(project, offline_mode=True)
    resolver.resolve_all()

    vhdl_sources, verilog_sources = expand_all_sources(project, resolver.resolved)

    with open(output_path, "w") as f:
        # Normale VHDL-Sources
        for lib, file in vhdl_sources:
            f.write(f"vhdl {lib} \"{DIRECTORIES.get_relative_prefix()}{file}\"\n")

        # Normale Verilog-Sources
        for lib, file in verilog_sources:
            f.write(f"verilog {lib} \"{DIRECTORIES.get_relative_prefix()}{file}\"\n")

        # Testbench-Datei suchen und einfügen
        testbench_file = find_testbench_file(project, testbench_name)
        normalized_tb = os.path.normpath(testbench_file)
        f.write(f"vhdl work \"{DIRECTORIES.get_relative_prefix()}{normalized_tb}\"\n")

        # glbl.v immer zuletzt
        f.write(f"verilog work /opt/Xilinx/14.7/ISE_DS/ISE/verilog/src/glbl.v\n")


def find_testbench_file(project: ProjectConfig, testbench_name: str) -> str:
    """
    Findet eine Testbench-Datei im Projekt anhand ihres Namens (ohne Endung, Case-Insensitive).

    Args:
        project (ProjectConfig): Projektdefinition.
        testbench_name (str): Gesuchter Dateiname (z.B. "VGATimingGenerator_test_tb").

    Returns:
        str: Vollständiger Pfad zur Testbench-Datei.

    Raises:
        FileNotFoundError: Wenn die Datei nicht gefunden wurde.
    """
    candidates = expand_testbenches(project)

    # Vergleichswerte vorbereiten (Name ohne Endung, in Kleinbuchstaben)
    search_name = os.path.splitext(testbench_name)[0].lower()

    for _, filepath in candidates:
        filename = os.path.basename(filepath)
        filename_no_ext = os.path.splitext(filename)[0].lower()

        if filename_no_ext == search_name:
            return filepath

    raise FileNotFoundError(f"Testbench '{testbench_name}' wurde nicht gefunden.")

def build_testbench(project: ProjectConfig, testbench_name: str):
    """
    Baut eine einzelne Testbench mit FUSE.

    Args:
        project (ProjectConfig): Hauptprojekt-Konfiguration
        testbench_name (str): Name der Testbench-Datei, z.B. "VGATimingGenerator_test_tb.vhd"
    """
    # Pfade
    isim_exe_name = f"isim_{testbench_name.replace('.vhd', '').replace('.v', '')}"
    isim_exe_path = os.path.join(DIRECTORIES.build, isim_exe_name)

    # 1. Simulation-Projektdatei generieren
    generate_simulation_project_file(
        project=project,
        output_path=os.path.join(DIRECTORIES.build, f"{project.name}_sim.prj"),
        testbench_name=testbench_name
    )

    # 2. Befehl bauen
    xilinx_path = project.xilinx_path
    xilinx_bin_dir = os.path.join(xilinx_path, "bin", "lin64")  # oder nt64 bei Windows
    fuse_executable = os.path.join(xilinx_bin_dir, "fuse")

    cmd = [
        fuse_executable,
        "-intstyle", "xflow",
        "-prj", f"{project.name}_sim.prj",
        "-o", isim_exe_name,
        f"work.{testbench_name.replace('.vhd', '').replace('.v', '')}",
        "work.glbl"
    ]

    # 3. Ausführen mit Konsole
    task = ConsoleTask(prefix="hdlbuild", title=f"FUSE {testbench_name}")
    result = task.run_command(cmd, cwd=DIRECTORIES.build)

    if result != 0:
        raise RuntimeError(f"FUSE fehlgeschlagen für Testbench {testbench_name}")

def run_testbench(testbench_name: str):
    """
    Führt eine gebaute Testbench-Executable aus (ISim Simulation).

    Args:
        testbench_name (str): Name der Testbench-Datei (z.B. "VGATimingGenerator_test_tb.vhd")
    """
    # Pfade
    isim_exe_name = f"isim_{testbench_name.replace('.vhd', '').replace('.v', '')}"
    isim_exe_path = os.path.join(DIRECTORIES.build, isim_exe_name)

    isim_cmd_file = os.path.join(DIRECTORIES.build, f"{isim_exe_name}.cmd")

    # 1. TCL-Skript für ISim erzeugen (einfache Simulation)
    with open(isim_cmd_file, "w") as f:
        f.write("")

    # 2. Kommando bauen
    cmd = [
        f"./{isim_exe_name}", 
        "-gui",
        "-tclbatch", 
        f"{isim_exe_name}.cmd"
    ]

    # 3. Ausführen
    task = ConsoleTask(prefix="hdlbuild", title=f"RUN {testbench_name}")
    result = task.run_command(cmd, cwd=DIRECTORIES.build)

    if result != 0:
        raise RuntimeError(f"Testbench {testbench_name} ist während der Simulation fehlgeschlagen!")
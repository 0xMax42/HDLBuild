# src/hdlbuild/utils/source_resolver.py

import glob
import os
from typing import List, Tuple
from hdlbuild.models.project import SourceFile, ProjectConfig
from hdlbuild.models.dependency import ResolvedDependency

def _expand_project_sources(project: ProjectConfig, project_root: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    """
    Expandiert die Quellen eines einzelnen Projekts, getrennt nach VHDL und Verilog.

    Args:
        project (ProjectConfig): Das Projekt, dessen Quellen expandiert werden sollen.
        project_root (str): Basisverzeichnis, von dem aus die Pfade aufgelöst werden.

    Returns:
        Tuple: (List of (library, filepath) für VHDL, List of (library, filepath) für Verilog)
    """
    vhdl_expanded = []
    verilog_expanded = []

    # VHDL-Sources
    for source in project.sources.vhdl:
        full_pattern = os.path.join(project_root, source.path)
        matched_files = glob.glob(full_pattern, recursive=True)
        for file in matched_files:
            normalized_path = os.path.normpath(file)
            vhdl_expanded.append((source.library, normalized_path))

    # Verilog-Sources
    for source in project.sources.verilog:
        full_pattern = os.path.join(project_root, source.path)
        matched_files = glob.glob(full_pattern, recursive=True)
        for file in matched_files:
            normalized_path = os.path.normpath(file)
            verilog_expanded.append((source.library, normalized_path))

    return vhdl_expanded, verilog_expanded

def expand_all_sources(root_project: ProjectConfig, resolved_dependencies: List[ResolvedDependency]) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    """
    Expandiert alle Quellen aus dem Root-Projekt und allen Dependencies, getrennt nach VHDL und Verilog.

    Args:
        root_project (ProjectConfig): Das Hauptprojekt
        resolved_dependencies (List[ResolvedDependency]): Alle rekursiv aufgelösten Dependencies

    Returns:
        Tuple:
            - List of (library, filepath) für VHDL
            - List of (library, filepath) für Verilog
    """
    all_vhdl_sources = []
    all_verilog_sources = []

    # Root-Projekt expandieren
    vhdl_sources, verilog_sources = _expand_project_sources(root_project, ".")
    all_vhdl_sources.extend(vhdl_sources)
    all_verilog_sources.extend(verilog_sources)

    # Dependencies expandieren
    for dep in resolved_dependencies:
        vhdl_dep, verilog_dep = _expand_project_sources(dep.project, dep.local_path)
        all_vhdl_sources.extend(vhdl_dep)
        all_verilog_sources.extend(verilog_dep)

    return all_vhdl_sources, all_verilog_sources

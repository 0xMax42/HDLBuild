import glob
import os
from typing import List, Tuple
from models.project import SourceFile

def expand_sources(sources: List[SourceFile]) -> List[Tuple[str, str]]:
    """
    Expandiert eine Liste von SourceFile-Objekten mit Wildcards in echte Pfade.
    
    Returns:
        List of (library, filepath)
    """
    expanded = []
    for source in sources:
        matched_files = glob.glob(source.path, recursive=True)
        for file in matched_files:
            normalized_path = os.path.normpath(file)
            expanded.append((source.library, normalized_path))
    return expanded

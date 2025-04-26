import os
import shutil
from models.config import DIRECTORIES

def ensure_directories_exist(silent: bool = True):
    """
    Erstellt alle in der Konfiguration definierten Verzeichnisse, falls sie nicht existieren.
    """
    for name, path in DIRECTORIES.dict().items():
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            if not silent:
                print(f"[hdlbuild] Verzeichnis erstellt: {path}")
        else:
            if not silent:
                print(f"[hdlbuild] Verzeichnis vorhanden: {path}")

def clear_directories(silent: bool = True):
    """
    Löscht alle in der Konfiguration definierten Verzeichnisse, falls sie existieren.
    """
    for name, path in DIRECTORIES.dict().items():
        if os.path.exists(path):
            if not silent:
                print(f"[hdlbuild] Lösche Verzeichnis: {path}")
            shutil.rmtree(path)
        else:
            if not silent:
                print(f"[hdlbuild] Verzeichnis nicht vorhanden, übersprungen: {path}")

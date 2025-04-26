import os
import shutil
from models.config import DIRECTORIES

def ensure_directories_exist():
    """
    Erstellt alle in der Konfiguration definierten Verzeichnisse, falls sie nicht existieren.
    """
    for name, path in DIRECTORIES.dict().items():
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            print(f"[hdlbuild] Verzeichnis erstellt: {path}")
        else:
            print(f"[hdlbuild] Verzeichnis vorhanden: {path}")

def clear_directories():
    """
    Löscht alle in der Konfiguration definierten Verzeichnisse, falls sie existieren.
    """
    for name, path in DIRECTORIES.dict().items():
        if os.path.exists(path):
            print(f"[hdlbuild] Lösche Verzeichnis: {path}")
            shutil.rmtree(path)
        else:
            print(f"[hdlbuild] Verzeichnis nicht vorhanden, übersprungen: {path}")

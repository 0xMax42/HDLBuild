import os
import shutil
from hdlbuild.models.config import DIRECTORIES
from hdlbuild.utils.console_utils import ConsoleUtils

def ensure_directories_exist(silent: bool = False):
    """
    Erstellt alle in der Konfiguration definierten Verzeichnisse, falls sie nicht existieren.
    """
    console_utils = None
    if not silent:
        console_utils = ConsoleUtils("hdlbuild")

    for name, path in DIRECTORIES.dict().items():
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            if not silent and console_utils:
                console_utils.print(f"Verzeichnis erstellt: {path}")
        else:
            if not silent and console_utils:
                console_utils.print(f"[hdlbuild] Verzeichnis vorhanden: {path}")

def clear_directories(silent: bool = False):
    """
    Löscht alle in der Konfiguration definierten Verzeichnisse, falls sie existieren.
    """
    console_utils = None
    if not silent:
        console_utils = ConsoleUtils("hdlbuild")

    for name, path in DIRECTORIES.dict().items():
        if os.path.exists(path):
            if not silent and console_utils:
                console_utils.print(f"Lösche Verzeichnis: {path}")
            shutil.rmtree(path)
        else:
            if not silent and console_utils:
                console_utils.print(f"Verzeichnis nicht vorhanden, übersprungen: {path}")

def clear_build_directories(silent: bool = False):
    """
    Löscht alle in der Konfiguration definierten Verzeichnisse, falls sie existieren.
    """
    console_utils = None
    if not silent:
        console_utils = ConsoleUtils("hdlbuild")

    for name, path in DIRECTORIES.dict().items():
        if name == "dependency":
            continue
        if os.path.exists(path):
            if not silent and console_utils:
                console_utils.print(f"Lösche Verzeichnis: {path}")
            shutil.rmtree(path)
        else:
            if not silent and console_utils:
                console_utils.print(f"Verzeichnis nicht vorhanden, übersprungen: {path}")

import yaml
from models.project import ProjectConfig

def load_project_config(path: str = "project.yml") -> ProjectConfig:
    """
    Lädt die Projektkonfiguration aus einer YAML-Datei und gibt ein typisiertes ProjectConfig-Objekt zurück.
    
    Args:
        path (str): Pfad zur project.yml Datei (Default: "project.yml")
    
    Returns:
        ProjectConfig: Geparstes und typisiertes Projektkonfigurationsobjekt
    """
    with open(path, "r") as file:
        raw_data = yaml.safe_load(file)
    return ProjectConfig(**raw_data)

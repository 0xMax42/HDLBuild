from pydantic import BaseModel, Field, RootModel
from typing import Dict, Any

class TemplateInstance(BaseModel):
    template: str                       # Pfad zur Jinja2-Vorlage
    output: str                         # Zielpfad
    variables: Dict[str, Any] = Field(default_factory=dict)  # Variablen für Rendering

class ProjectTemplates(RootModel):
    """
    Pydantic-RootModel, das die Mapping-Struktur *name → TemplateInstance*
    kapselt.  In Pydantic v2 ersetzt `RootModel` die frühere `__root__`-Syntax.
    """
    root: Dict[str, TemplateInstance]  # key = Name wie „alu“, „control_unit“

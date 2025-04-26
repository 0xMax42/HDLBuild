# models/dependency.py

from pydantic import BaseModel
from hdlbuild.models.project import ProjectConfig

class ResolvedDependency(BaseModel):
    project: ProjectConfig
    local_path: str

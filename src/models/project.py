from pydantic import BaseModel, Field
from typing import List, Optional

class SourceFile(BaseModel):
    path: str
    library: str = "work"   # Default auf 'work'

class Dependency(BaseModel):
    name: str
    git: str
    rev: str
    library: str = "work"   # Default auf 'work'

class Sources(BaseModel):
    vhdl: List[SourceFile] = Field(default_factory=list)
    verilog: List[SourceFile] = Field(default_factory=list)

class Testbenches(BaseModel):
    vhdl: List[SourceFile] = Field(default_factory=list)
    verilog: List[SourceFile] = Field(default_factory=list)

class BuildOptions(BaseModel):
    build_dir: Optional[str] = "working"
    report_dir: Optional[str] = "reports"
    copy_target_dir: Optional[str] = "output"

class ProjectConfig(BaseModel):
    name: str
    topmodule: Optional[str]
    target_device: str
    xilinx_path: str
    sources: Sources
    testbenches: Optional[Testbenches] = None
    constraints: Optional[str] = None
    build: Optional[BuildOptions] = None
    dependencies: Optional[List[Dependency]] = Field(default_factory=list)

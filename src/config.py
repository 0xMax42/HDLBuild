from pydantic import BaseModel

class DirectoryConfig(BaseModel):
    dependency: str = ".hdlbuild_deps"
    build: str = ".working"
    report: str = "reports"
    copy_target: str = "output"

DIRECTORIES = DirectoryConfig()

class GitConfig(BaseModel):
    timeout: int = 10

GIT = GitConfig()
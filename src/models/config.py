import os
from pydantic import BaseModel

class DirectoryConfig(BaseModel):
    dependency: str = ".hdlbuild_deps"
    build: str = ".working"
    report: str = "reports"
    copy_target: str = "output"

    def get_relative_prefix(self) -> str:
        """
        Gibt den relativen Pfad von build-Verzeichnis zurück zum Hauptverzeichnis.

        Beispiel:
            ".working" -> "../"
            ".build/deep" -> "../../"
        """
        depth = len(os.path.normpath(self.build).split(os.sep))
        return "../" * depth

DIRECTORIES = DirectoryConfig()

class GitConfig(BaseModel):
    timeout: int = 10

GIT = GitConfig()
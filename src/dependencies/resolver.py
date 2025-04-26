# src/hdlbuild/dependency/resolver.py

from typing import List, Set

from git import Repo
from models.config import DIRECTORIES, GIT
from models.project import ProjectConfig
from models.dependency import ResolvedDependency
import os

from utils.console_utils import ConsoleUtils
from utils.project_loader import load_project_config

class DependencyResolver:
    def __init__(self, root_project: ProjectConfig, offline_mode: bool = False):
            self.root_project = root_project
            self.offline_mode = offline_mode
            self.resolved: List[ResolvedDependency] = [] 
            self.visited_urls: Set[str] = set()
            self.console = ConsoleUtils(live=True)
            self.console.start_live()

    def resolve_all(self):
        """Startet das Auflösen aller Abhängigkeiten (rekursiv)."""
        self._resolve_project(self.root_project)
        self.console.stop_live("[bold green]Alle Abhängigkeiten aufgelöst.[/bold green]")

    def _resolve_project(self, project: ProjectConfig):
        """Löst die Abhängigkeiten eines einzelnen Projekts auf."""
        for dep in project.dependencies or []:
            if dep.git in self.visited_urls:
                continue

            self.visited_urls.add(dep.git)

            local_path = self._clone_or_use_existing(dep.git, dep.rev)
            dep_project = self._load_project_config(os.path.join(local_path, "project.yml"))

            # Speichern als ResolvedDependency
            self.resolved.append(ResolvedDependency(project=dep_project, local_path=local_path))

            self._resolve_project(dep_project)

    def _clone_or_use_existing(self, git_url: str, rev: str) -> str:
        folder_name = os.path.basename(git_url.rstrip("/")).replace(".git", "")
        local_path = os.path.join(DIRECTORIES.dependency, folder_name)

        if os.path.exists(local_path):
            # Lokales Repo vorhanden
            self.console.print(f"[bold green]Benutze vorhandenes Repository: {folder_name}[/bold green]")
            repo = Repo(local_path)

            if not self.offline_mode:
                try:
                    self.console.print(f"[bold green]Aktualisiere {folder_name}...[/bold green]")

                    # Fetch Remote Updates
                    repo.remotes.origin.fetch()

                    # Prüfen, ob HEAD und origin/branch unterschiedlich sind
                    local_commit = repo.head.commit
                    remote_ref = repo.remotes.origin.refs[repo.active_branch.name]
                    remote_commit = remote_ref.commit

                    if local_commit.hexsha != remote_commit.hexsha:
                        self.console.print(f"[bold yellow]Änderungen erkannt! Force-Pull wird durchgeführt...[/bold yellow]")
                        repo.git.reset('--hard', remote_commit.hexsha)
                    else:
                        self.console.print(f"[bold green]Repository {folder_name} ist aktuell.[/bold green]")

                except Exception as e:
                    self.console.print(f"[bold red]Warnung beim Aktualisieren: {e}[/bold red]")

        else:
            # Lokales Repo fehlt → nur dann klonen
            if self.offline_mode:
                raise FileNotFoundError(f"Repository {folder_name} existiert lokal nicht und offline_mode ist aktiv.")
            else:
                self.console.print(f"[bold green]Klone {git_url}...[/bold green]")
                repo = Repo.clone_from(git_url, local_path)

        # Immer: Auf den richtigen Commit/Branch wechseln
        self.console.print(f"[bold green]Checkout auf[/bold green] [yellow]{rev}[/yellow] in {folder_name}")
        repo.git.checkout(rev)

        return local_path

    def _load_project_config(self, path: str) -> ProjectConfig:
        """
        Lädt eine project.yml aus einem lokalen Ordner.
        
        Args:
            path (str): Basisverzeichnis des geklonten Projekts.
        
        Returns:
            ProjectConfig: Das geladene Projekt.
        """
        self.console.print(f"Lade project.yml aus {path}...")
        return load_project_config(path)

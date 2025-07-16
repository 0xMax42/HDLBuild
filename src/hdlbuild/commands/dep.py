import typer

from hdlbuild.dependencies.resolver  import DependencyResolver
from hdlbuild.utils.console_utils    import ConsoleUtils
from hdlbuild.utils.project_loader   import load_project_config

cli = typer.Typer(rich_help_panel="🔗 Dependency Commands")

@cli.callback(invoke_without_command=True)
def dep() -> None:
    """
    Resolve all project dependencies.

    ```bash
    hdlbuild dep
    ```
    """
    console  = ConsoleUtils("hdlbuild")
    project  = load_project_config()

    console.print("Resolving dependencies …")
    DependencyResolver(project).resolve_all()
    console.print("Dependencies resolved.")

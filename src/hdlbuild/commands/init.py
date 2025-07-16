import shutil
from pathlib import Path
import typer

from hdlbuild.utils.console_utils import ConsoleUtils

cli = typer.Typer(rich_help_panel="🆕 Init Commands")

@cli.callback(invoke_without_command=True)
def init() -> None:
    """
    Initialise a new HDLBuild project in the current directory.

    Copies `.gitignore` and `project.yml` from the template folder.
    """
    console      = ConsoleUtils("hdlbuild")
    project_dir  = Path.cwd()

    script_dir   = Path(__file__).parent.resolve()
    template_dir = (script_dir / ".." / "templates").resolve()

    files = [
        ("gitignore.template", ".gitignore"),
        ("project.yml.template", "project.yml"),
    ]

    for template_name, target_name in files:
        template_path = template_dir / template_name
        target_path   = project_dir / target_name

        if not target_path.exists():
            shutil.copy(template_path, target_path)
            console.print(f"Created {target_name}")
        else:
            console.print(f"{target_name} already exists – skipping.")

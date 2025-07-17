from __future__ import annotations

import typer

from hdlbuild.generate.template_generator import TemplateGenerator
from hdlbuild.utils.console_utils import ConsoleUtils
from hdlbuild.utils.project_loader import load_project_config

cli = typer.Typer(rich_help_panel="🧬 Template Commands")

@cli.command("list")
def list_templates() -> None:
    """
    List all available template names from *project.yml*.

    ```bash
    hdlbuild gen list
    ```
    """
    console = ConsoleUtils("hdlbuild")
    project = load_project_config()
    TemplateGenerator.list_templates(project, console)


@cli.callback(invoke_without_command=True)
def gen( 
    ctx: typer.Context,
    name: str = typer.Option(
        None,
        "--name",
        "-n",
        help="Name of the template to generate (from project.yml)",
        show_default=False,
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Only show the output without writing file",
    ),
) -> None:
    """
    Render HDL files from Jinja2 templates.

    * `hdlbuild gen` → render all templates  
    * `hdlbuild gen <name>` → render a specific template  
    * `hdlbuild gen <name> --dry-run` → only show output without saving
    """
    console = ConsoleUtils("hdlbuild")
    project = load_project_config()

    # Only executed when no subcommand (e.g., "list") is active.
    if ctx.invoked_subcommand is None:
        TemplateGenerator.generate(project, name, dry_run, console)

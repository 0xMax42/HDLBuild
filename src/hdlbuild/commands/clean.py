import typer

from hdlbuild.utils.console_utils      import ConsoleUtils
from hdlbuild.utils.directory_manager  import clear_build_directories, clear_directories

cli = typer.Typer(rich_help_panel="🧹 Clean Commands")

@cli.callback(invoke_without_command=True)
def clean(
    target: str = typer.Argument(
        None,
        help="Optional: 'all' → wipe *all* artefacts, otherwise only the build directory",
        show_default=False,
    )
) -> None:
    """
    Remove build artefacts (`build/*`) or *everything* (`all`).

    Examples
    --------
    ```bash
    hdlbuild clean          # build/* and temporary files only
    hdlbuild clean all      # also caches, logs, etc.
    ```
    """
    console = ConsoleUtils("hdlbuild")

    if target == "all":
        console.print("Starting clean‑all …")
        clear_directories()
        console.print("All artefacts removed.")
    else:
        console.print("Removing build artefacts …")
        clear_build_directories()
        console.print("Build artefacts removed.")

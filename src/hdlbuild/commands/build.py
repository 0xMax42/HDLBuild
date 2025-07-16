import typer

from hdlbuild.tools.xilinx_ise.main    import xilinx_ise_all, xilinx_ise_synth
from hdlbuild.utils.console_utils      import ConsoleUtils
from hdlbuild.utils.directory_manager  import ensure_directories_exist
from hdlbuild.utils.project_loader     import load_project_config

cli = typer.Typer(rich_help_panel="🔨 Build Commands")

@cli.callback(invoke_without_command=True)
def build(
    target: str = typer.Argument(
        None,
        help="Optional: 'synth' to run synthesis only",
        show_default=False,
        rich_help_panel="🔨 Build Commands",
    )
) -> None:
    """
    Run the full build flow or synthesis only.

    * `hdlbuild build` → full flow  
    * `hdlbuild build synth` → synthesis only
    """
    console  = ConsoleUtils("hdlbuild")
    project  = load_project_config()

    ensure_directories_exist(True)
    if target == "synth":
        console.print("Starting synthesis …")
        xilinx_ise_synth(project)
    else:
        console.print("Starting full build …")
        xilinx_ise_all(project)

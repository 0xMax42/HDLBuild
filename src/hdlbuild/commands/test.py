import typer

from hdlbuild.tools.xilinx_ise.isim  import build_testbench, run_testbench
from hdlbuild.utils.console_utils    import ConsoleUtils
from hdlbuild.utils.project_loader   import load_project_config

cli = typer.Typer(rich_help_panel="🧪 Test Commands")

@cli.callback(invoke_without_command=True)
def test(
    target: str = typer.Argument(
        None,
        help="Name of the test target (leave empty to run all)",
        show_default=False,
    )
) -> None:
    """
    Build and run testbenches.

    ```bash
    hdlbuild test            # run all TBs
    hdlbuild test alu        # run TB 'alu' only
    ```
    """
    console  = ConsoleUtils("hdlbuild")
    project  = load_project_config()

    console.print("Starting test flow …")
    build_testbench(project, target)
    run_testbench(project,  target)
    console.print("Tests finished.")

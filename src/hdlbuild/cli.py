import typer
from importlib.metadata import version, PackageNotFoundError

from hdlbuild.commands.build import cli as build_cli
from hdlbuild.commands.clean import cli as clean_cli
from hdlbuild.commands.dep   import cli as dep_cli
from hdlbuild.commands.test  import cli as test_cli
from hdlbuild.commands.init  import cli as init_cli

def get_version() -> str:
    try:
        return version("hdlbuild")
    except PackageNotFoundError:
        return "unknown"

app = typer.Typer(
    rich_help_panel="ℹ️  HDLBuild – FPGA‑Build‑Tool",
    help=f"hdlbuild v{get_version()} – Build‑Management for FPGA projects"
)

# Unter‑Kommandos registrieren (entspricht add_subparsers)
app.add_typer(build_cli, name="build", help="Build the project")
app.add_typer(clean_cli, name="clean", help="Clean build artifacts")
app.add_typer(dep_cli,   name="dep",   help="Resolve dependencies")
app.add_typer(test_cli,  name="test",  help="Run simulations/testbenches")
app.add_typer(init_cli,  name="init",  help="Initialize project")

def main():
    app()

if __name__ == "__main__":
    main()
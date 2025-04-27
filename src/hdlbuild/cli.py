import argparse
import sys

from hdlbuild.dependencies.resolver import DependencyResolver
from hdlbuild.models.config import DIRECTORIES
from hdlbuild.tools.xilinx_ise.isim import build_testbench, generate_simulation_project_file, run_testbench
from hdlbuild.tools.xilinx_ise.main import xilinx_ise_all, xilinx_ise_synth
from hdlbuild.utils.console_utils import ConsoleUtils
from hdlbuild.utils.directory_manager import clear_build_directories, clear_directories, ensure_directories_exist
from hdlbuild.utils.project_loader import load_project_config

project = load_project_config()
console_utils = ConsoleUtils("hdlbuild")

def clear(args):
    """Clears the build artifacts."""
    if args.target == "all":
        console_utils.print("Starting clear all process...")
        clear_directories()
        console_utils.print("All cleared.")
    else:
        console_utils.print("Clearing build artifacts...")
        clear_build_directories()
        console_utils.print("Build artifacts cleared.")

def build(args):
    """Starts the build process."""
    console_utils.print("Starting build process...")
    ensure_directories_exist(True)
    xilinx_ise_all(project)

def synth(args):
    """Starts the build process."""
    console_utils.print("Starting build process...")
    ensure_directories_exist()
    xilinx_ise_synth(project)

def dep(args):
    """Starts the dependencies process."""
    console_utils.print("Starting dependencies process...")
    DependencyResolver(project).resolve_all()

def test(args):
    """Starts the test process."""
    console_utils.print("Starting test process...")
    build_testbench(project, args.target)
    run_testbench(args.target)


def main():
    parser = argparse.ArgumentParser(
        description="hdlbuild - Build management tool for FPGA projects",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        description="Available commands",
        dest="command",
        required=True
    )

    # Clear command
    parser_clear = subparsers.add_parser("clear", help="Clear build artifacts")
    parser_clear.add_argument(
        "target",
        nargs="?",
        choices=["all"],
        help="Specify 'all' to clear everything (optional)"
    )
    parser_clear.set_defaults(func=clear)

    # Build command
    parser_build = subparsers.add_parser("build", help="Start the build process")
    parser_build.set_defaults(func=build)

    # Synth command
    parser_synth = subparsers.add_parser("synth", help="Start the synth process")
    parser_synth.set_defaults(func=synth)

    # Dependencies command
    parser_dep = subparsers.add_parser("dep", help="Start the dependencies process")
    parser_dep.set_defaults(func=dep)

    # Tests command
    parser_test = subparsers.add_parser("test", help="Start the Tests process")
    parser_test.set_defaults(func=test)
    parser_test.add_argument(
        "target",
        nargs="?",
        help="Select the target to test"
    )

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
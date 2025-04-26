import argparse
import sys

from tools.xilinx_ise.main import xilinx_ise_all, xilinx_ise_synth
from utils.console_utils import ConsoleUtils
from utils.directory_manager import clear_build_directories, clear_directories, ensure_directories_exist
from utils.project_loader import load_project_config

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
    parser_build = subparsers.add_parser("synth", help="Start the synth process")
    parser_build.set_defaults(func=synth)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
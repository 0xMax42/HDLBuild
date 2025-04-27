import argparse
from importlib.metadata import version, PackageNotFoundError
from hdlbuild.commands import register_commands

def get_version():
    try:
        return version("hdlbuild")  # Paketname aus pyproject.toml
    except PackageNotFoundError:
        return "unknown"

def main():
    version_str = get_version()
    parser = argparse.ArgumentParser(
        description=f"hdlbuild v{version_str} - Build management tool for FPGA projects",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        description="Available commands",
        dest="command",
        required=True
    )

    # Register all commands
    register_commands(subparsers)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
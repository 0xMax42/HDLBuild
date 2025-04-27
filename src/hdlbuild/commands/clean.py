from hdlbuild.utils.console_utils import ConsoleUtils
from hdlbuild.utils.directory_manager import clear_build_directories, clear_directories

class CleanCommand:
    def __init__(self):
        self.console_utils = ConsoleUtils("hdlbuild")

    def register(self, subparsers):
        parser = subparsers.add_parser("clean", help="Clean build artifacts")
        parser.add_argument(
            "target",
            nargs="?",
            choices=["all"],
            help="Specify 'all' to clean everything (optional)"
        )
        parser.set_defaults(func=self.execute)

    def execute(self, args):
        """Cleans the build artifacts."""
        if args.target == "all":
            self.console_utils.print("Starting clean all process...")
            clear_directories()
            self.console_utils.print("All cleaned.")
        else:
            self.console_utils.print("Clearing build artifacts...")
            clear_build_directories()
            self.console_utils.print("Build artifacts cleaned.")
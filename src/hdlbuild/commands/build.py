from hdlbuild.tools.xilinx_ise.main import xilinx_ise_all, xilinx_ise_synth
from hdlbuild.utils.console_utils import ConsoleUtils
from hdlbuild.utils.directory_manager import ensure_directories_exist
from hdlbuild.utils.project_loader import load_project_config

class BuildCommand:
    def __init__(self):
        self.console_utils = ConsoleUtils("hdlbuild")

    def register(self, subparsers):
        parser = subparsers.add_parser("build", help="Start the build process")
        parser.add_argument(
            "target",
            nargs="?",
            choices=["synth"],
            help="Specify 'synth' to only synthesize the design (optional)"
        )
        parser.set_defaults(func=self.execute)

    def execute(self, args):
        """Starts the build process."""
        self.project = load_project_config()
        if args.target == "synth":
            self.console_utils.print("Starting synth process...")
            ensure_directories_exist(True)
            xilinx_ise_synth(self.project)
        else:
            self.console_utils.print("Starting build process...")
            ensure_directories_exist(True)
            xilinx_ise_all(self.project)
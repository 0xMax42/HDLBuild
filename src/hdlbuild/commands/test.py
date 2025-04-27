from hdlbuild.tools.xilinx_ise.isim import build_testbench, run_testbench
from hdlbuild.utils.console_utils import ConsoleUtils
from hdlbuild.utils.project_loader import load_project_config

class TestCommand:
    def __init__(self):
        self.console_utils = ConsoleUtils("hdlbuild")

    def register(self, subparsers):
        parser = subparsers.add_parser("test", help="Start the Tests process")
        parser.add_argument(
            "target",
            nargs="?",
            help="Select the target to test"
        )
        parser.set_defaults(func=self.execute)

    def execute(self, args):
        """Starts the test process."""
        self.project = load_project_config()
        self.console_utils.print("Starting test process...")
        build_testbench(self.project, args.target)
        run_testbench(self.project, args.target)
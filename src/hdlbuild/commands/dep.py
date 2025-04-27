from hdlbuild.dependencies.resolver import DependencyResolver
from hdlbuild.utils.console_utils import ConsoleUtils
from hdlbuild.utils.project_loader import load_project_config

class DepCommand:
    def __init__(self):
        self.console_utils = ConsoleUtils("hdlbuild")
        self.project = load_project_config()

    def register(self, subparsers):
        parser = subparsers.add_parser("dep", help="Start the dependencies process")
        parser.set_defaults(func=self.execute)

    def execute(self, args):
        """Starts the dependencies process."""
        self.console_utils.print("Starting dependencies process...")
        DependencyResolver(self.project).resolve_all()
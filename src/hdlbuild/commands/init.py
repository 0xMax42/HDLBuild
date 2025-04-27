from pathlib import Path
import shutil
from hdlbuild.dependencies.resolver import DependencyResolver
from hdlbuild.utils.console_utils import ConsoleUtils

class InitCommand:
    def __init__(self):
        self.console_utils = ConsoleUtils("hdlbuild")

    def register(self, subparsers):
        parser = subparsers.add_parser("init", help="Initialize a new HDLBuild project")
        parser.set_defaults(func=self.execute)

    def execute(self, args):
        """Initialize a new HDLBuild project."""
        project_dir = Path.cwd()

        # Correctly resolve path to templates directory
        script_dir = Path(__file__).parent.resolve()
        template_dir = (script_dir / ".." / "templates").resolve()

        # Files to copy
        files = [
            ("gitignore.template", ".gitignore"),
            ("project.yml.template", "project.yml"),
        ]

        for template_name, target_name in files:
            template_path = template_dir / template_name
            target_path = project_dir / target_name

            if not target_path.exists():
                shutil.copy(template_path, target_path)
                self.console_utils.print(f"Created {target_name}")
            else:
                self.console_utils.print(f"{target_name} already exists, skipping.")

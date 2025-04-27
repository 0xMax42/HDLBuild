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

        # Paths to templates
        template_dir = Path(__file__).parent / "templates"

        # .gitignore
        gitignore_template = template_dir / "gitignore.template"
        gitignore_target = project_dir / ".gitignore"

        if not gitignore_target.exists():
            shutil.copy(gitignore_template, gitignore_target)
            self.console_utils.print("Created .gitignore")
        else:
            self.console_utils.print(".gitignore already exists, skipping.")

        # project.yml
        project_yml_template = template_dir / "project.yml.template"
        project_yml_target = project_dir / "project.yml"

        if not project_yml_target.exists():
            shutil.copy(project_yml_template, project_yml_target)
            self.console_utils.print("Created project.yml")
        else:
            self.console_utils.print("project.yml already exists, skipping.")
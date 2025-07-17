"""
hdlbuild.generate.template_generator
====================================

Enthält die Klasse :class:`TemplateGenerator`, die das Auflisten und Rendern
von in *project.yml* definierten Jinja2-Templates kapselt.
"""

from __future__ import annotations

import os
from typing import Optional

from jinja2 import Environment, FileSystemLoader

from hdlbuild.models.templates import TemplateInstance
from hdlbuild.utils.console_utils import ConsoleUtils


class TemplateGenerator:
    """
    Hilfsklasse zum Auflisten und Rendern der im Projekt konfigurierten
    Jinja2-Templates.
    """

    # --------------------------------------------------------------------- #
    # Öffentliche API
    # --------------------------------------------------------------------- #

    @staticmethod
    def list_templates(project, console: ConsoleUtils) -> None:
        """
        Alle in *project.yml* definierten Templates auflisten.
        """
        if not project.templates:
            console.print("[yellow]No templates defined in project.yml")
            return

        console.print("[bold underline]Available Templates:")
        for name in project.templates.root.keys():
            console.print(f"• {name}")

    @classmethod
    def generate(
        cls,
        project,
        name: Optional[str],
        dry_run: bool,
        console: ConsoleUtils,
    ) -> None:
        """
        Templates erzeugen.

        Parameters
        ----------
        project
            Geladenes Projekt-Model.
        name
            Name eines einzelnen Templates oder *None*, um alle Templates
            zu erzeugen.
        dry_run
            Wenn *True*, wird das gerenderte Ergebnis nur ausgegeben,
            jedoch nicht auf die Festplatte geschrieben.
        console
            Farbige Konsolen-Ausgaben.
        """
        if not project.templates:
            console.print("[red]No templates defined in project.yml")
            return

        templates = project.templates.root

        if name:
            # Ein bestimmtes Template
            if name not in templates:
                console.print(f"[red]Template '{name}' not found.")
                return
            cls._render_template(name, templates[name], dry_run, console)
        else:
            # Alle Templates durchlaufen
            for tname, template in templates.items():
                cls._render_template(tname, template, dry_run, console)

    # --------------------------------------------------------------------- #
    # Interne Helfer
    # --------------------------------------------------------------------- #

    @staticmethod
    def _render_template(
        name: str,
        template: TemplateInstance,
        dry_run: bool,
        console: ConsoleUtils,
    ) -> None:
        """
        Einzelnes Template rendern und wahlweise speichern.
        """
        template_path = template.template
        output_path = template.output
        variables = template.variables

        env = Environment(
            loader=FileSystemLoader(os.path.dirname(template_path)),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        j2 = env.get_template(os.path.basename(template_path))
        result = j2.render(**variables)

        if dry_run:
            console.print(f"[green]--- Template: {name} (dry-run) ---")
            console.print(result)
            console.print(f"[green]--- End of {name} ---")
            return

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(result)

        console.print(f"[cyan]✔ Rendered template '{name}' → {output_path}")

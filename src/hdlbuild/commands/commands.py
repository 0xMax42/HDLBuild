from hdlbuild.commands.build import BuildCommand
from hdlbuild.commands.clean import CleanCommand
from hdlbuild.commands.dep import DepCommand
from hdlbuild.commands.init import InitCommand
from hdlbuild.commands.test import TestCommand


def register_commands(subparsers):
    """Registers all available commands."""
    commands = [
        CleanCommand(),
        BuildCommand(),
        DepCommand(),
        TestCommand(),
        InitCommand(),
    ]

    for command in commands:
        command.register(subparsers)
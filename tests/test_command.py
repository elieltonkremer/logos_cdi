import pytest
from logos_cdi.application import Application
from logos_cdi.command import Commands, AbstractCommand, CommandModule
from unittest.mock import MagicMock
from logos_cdi.resource import Service
from logos_cdi.application import BaseModule

class HelloCommand(AbstractCommand):
    def define_arguments(self, argument_parser):
        argument_parser.add_argument('--name', default='World')
        return super().define_arguments(argument_parser)

    def execute(self):
        return f"Hello, {self.arguments.name}!"

class TestCommandModule(CommandModule, BaseModule):
    def define_commands(self):
        return {
            'hello': Service(
                class_path=f'{__name__}.HelloCommand',
                parameters={}
            )
        }

def test_command_execution():
    app = Application(modules=[Commands(), TestCommandModule()])
    command = app.get('commands.hello')

    mock_args = type('args', (), {'name': 'Jules'})()
    mock_parser = MagicMock()
    mock_parser.parse_known_args.return_value = (mock_args, [])
    command.argument_parser = mock_parser

    assert command.execute() == "Hello, Jules!"

def test_command_argument_definition():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    command = HelloCommand()
    command.define_arguments(parser)
    args = parser.parse_args(['--name', 'Test'])
    assert args.name == 'Test'

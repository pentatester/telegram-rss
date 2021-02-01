from telegram.ext import CommandHandler
from telegram.ext import Dispatcher

from .start import command as start_command
from .update import command as update_command


COMMANDS = [
    start_command,
    update_command,
]


def register_commands(dispatcher: Dispatcher):
    for command in COMMANDS:
        if isinstance(command, CommandHandler):
            dispatcher.add_handler(command)
        else:
            ValueError(f"{type(command)} is not CommandHandler instance")

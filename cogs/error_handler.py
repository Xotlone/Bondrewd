import logging

import disnake
from disnake.ext import commands as dis_commands
from disnake.ext.commands import errors

from constants import commands
import exceptions

log = logging.getLogger('logs')


class ErrorHandler(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot

    @dis_commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.CommandInteraction, error: dis_commands.CommandError):
        def er(e): isinstance(error, e)

        if er(errors.CheckFailure):
            try:
                command_access = commands.Command.search(inter.application_command.name).access
            except AttributeError:
                command_access = commands.SubCommand.search(inter.application_command.name).access

            await exceptions.Access.call(inter, error, command_access)

        else:
            log.error(error, exc_info=True)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))

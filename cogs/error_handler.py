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
        log.error(repr(error), exc_info=True)
        log.info(error.args)

        if type(error) == errors.CheckFailure:
            try:
                command_access = commands.Command.search(inter.application_command.name).access
            except AttributeError:
                command_access = commands.SubCommand.search(inter.application_command.name).access

            await exceptions.Access(inter, command_access)

        elif type(error) == errors.NSFWChannelRequired:
            await exceptions.NSFW(inter)

        elif type(error) == errors.CommandInvokeError and error.args[0] == 'Command raised an exception: ' \
                                                                           'InteractionNotResponded: This interaction ' \
                                                                           'hasn\'t been responded to yet':
            await exceptions.UndefinedError(inter)



def setup(bot):
    bot.add_cog(ErrorHandler(bot))

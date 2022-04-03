import logging

import disnake
from disnake.ext import commands as dis_commands

from database import database


class Administration(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Administration(bot))

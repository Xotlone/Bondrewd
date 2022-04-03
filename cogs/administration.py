import disnake
from disnake.ext import commands as dis_commands

from constants import commands
import controller
from database import database


class Administration(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot

    @dis_commands.slash_command(**commands.administration())
    @dis_commands.check(commands.administration.acs)
    @dis_commands.has_permissions(administrator=True)
    async def command_administration(self, inter: disnake.CommandInteraction):
        pass

    @command_administration.sub_command(**commands.administration.sub['logging']())
    @dis_commands.check(commands.administration.sub['logging'].acs)
    async def sub_logging(self, inter: disnake.CommandInteraction, condition: str):
        if int(condition):
            database(f'UPDATE servers_settings SET logging = {inter.channel_id} WHERE id = {inter.guild_id}')
            embed = disnake.Embed(
                title='Логирование включено',
                description='В этот канал теперь будут присылаться логи',
                colour=controller.RANKS_DICT['Колокольчик'].colour
            )

        else:
            database(f'UPDATE servers_settings SET logging = 0 WHERE id = {inter.guild_id}')
            embed = disnake.Embed(
                title='Логирование выключено',
                description='В этом канале больше не будет логов',
                colour=controller.RANKS_DICT['Колокольчик'].colour
            )

        await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(Administration(bot))

import disnake
from disnake.ext import commands as dis_commands

from constants import commands
import controller

class Munera(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot
   
    @dis_commands.slash_command(**commands.munera())
    @dis_commands.check(commands.munera.acs)
    async def command_munera(self, inter: disnake.CommandInteraction):
        pass
    
    @command_munera.sub_command(**commands.munera.sub['calc']())
    @dis_commands.check(commands.munera.sub['calc'].acs)
    async def sub_calc(self, inter: disnake.CommandInteraction, primer: str):
        embed = disnake.Embed(
            title='Математический пример',
            description=f"{primer} = {eval(primer)}",
            colour=controller.RANKS_DICT['Колокольчик'].colour
        )
        await inter.edit_original_message(embed=embed)

def setup(bot):
   bot.add_cog(Munera(bot))
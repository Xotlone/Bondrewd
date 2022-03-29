import disnake
from disnake.ext import commands as dis_commands

from constants import commands
import controller

class Munera(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot
   
    @dis_commands.slash_command(**commands.funcs())
    @dis_commands.check(commands.funcs.acs)
    async def command_funcs(self, inter: disnake.CommandInteraction):
        pass
    
    @command_funcs.sub_command(**commands.funcs.sub['calc']())
    @dis_commands.check(commands.funcs.sub['calc'].acs)
    async def sub_calc(self, inter: disnake.CommandInteraction, primer: str):
        embed = disnake.Embed(
            title='Математический пример',
            description=f"{primer} = {eval(primer)}",
            colour=controller.RANKS_DICT['Колокольчик'].colour
        )
        await inter.edit_original_message(embed=embed)
    
    @command_funcs(**commands.funcs.sub['learn-japanese']())
    @dis_commands.check(commands.funcs.sub['learn-japanese'].acs)
    async def learn_japanese(self, inter: disnake.CommandInteraction, alphabet: str, only_complex: bool=False):
        modal = disnake.ui.Modal(
            title='Test',
            components=[
                disnake.ui.TextInput(
                    label="Test text input",
                    placeholder="The name of the tag",
                    custom_id="custom id",
                    style=disnake.TextInputStyle.short,
                    max_length=50,
                ),
            ]
        )

        await inter.response.send_modal(modal=modal())

def setup(bot):
   bot.add_cog(Munera(bot))
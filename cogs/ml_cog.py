import disnake
from disnake.ext import commands as dis_commands

from constants import commands
from ml import word_processing
import controller


class ML(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot

    @dis_commands.slash_command(**commands.ml())
    @dis_commands.check(commands.ml.acs)
    async def command_ml(self, inter: disnake.CommandInteraction):
        pass

    @command_ml.sub_command(**commands.ml.sub['skip-gramm']())
    @dis_commands.check(commands.ml.sub['skip-gramm'].acs)
    async def skip_gramm(self, inter: disnake.CommandInteraction, text: str, n_gramm: int = 3,
                         padding: str = 'correspond'):
        s_gramm = word_processing.skip_gramm(text, n_gramm, padding)
        s_gramm_txt = '[\n'
        for i in s_gramm:
            s_gramm_txt += f'    {str(i)},\n'
        s_gramm_txt += ']'

        with open('temp/_df.txt', 'w', encoding='utf-8') as f:
            f.write(str(s_gramm_txt))
        file = disnake.File('temp/_df.txt', 'skip-gramm.txt')
        await inter.edit_original_message(file=file)


def setup(bot):
    bot.add_cog(ML(bot))

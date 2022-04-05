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

    #@command_ml.sub_command_group(**commands.ml.sub['tokenizer']())
    #@dis_commands.check(commands.ml.sub['tokenizer'].acs)
    #async def group_tokenizer(self, inter: disnake.CommandInteraction):
    #    pass
    #
    #@group_tokenizer.sub_command(**commands.ml.sub['tokenizer'].sub['tokenize']())
    #@dis_commands.check(commands.ml.sub['tokenizer'].sub['tokenize'].acs)
    #async def sub_tokenize(self, inter: disnake.CommandInteraction, text: str):
    #    tokens = word_processing.Tokenizator.tokenize(inter.author.id, text)
    #    with open('temp/_df.txt', 'w', encoding='utf-8') as f:
    #        f.write(str(tokens))
    #
    #    tokenized_text = disnake.File('temp/_df.txt', 'tokenized_text.txt')
    #    embed = disnake.Embed(
    #        title='Токенизированный текст',
    #        colour=controller.RANKS_DICT['Чёрный свисток'].colour
    #    )
    #    await inter.edit_original_message(embed=embed, file=tokenized_text)
    #
    #@group_tokenizer.sub_command(**commands.ml.sub['tokenizer'].sub['pre']())
    #@dis_commands.check(commands.ml.sub['tokenizer'].sub['pre'].acs)
    #async def sub_pre(self, inter: disnake.CommandInteraction, text: str):
    #    tokens = word_processing.Tokenizator.pre(text)
    #
    #    with open('temp/_df.txt', 'w', encoding='utf-8') as f:
    #        f.write(str(tokens))
    #    file = disnake.File('temp/_df.txt', 'filtered_text.txt')
    #    embed = disnake.Embed(
    #        title='Подготовленный текст',
    #        colour=controller.RANKS_DICT['Чёрный свисток'].colour
    #    )
    #    await inter.edit_original_message(embed=embed, file=file)

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

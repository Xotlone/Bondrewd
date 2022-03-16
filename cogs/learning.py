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

    @command_ml.sub_command_group(**commands.ml.sub['tokenizator']())
    @dis_commands.check(commands.ml.sub['tokenizator'].acs)
    async def group_tokenizator(self, inter: disnake.CommandInteraction):
        pass
    
    @group_tokenizator.sub_command(**commands.ml.sub['tokenizator'].sub['tokenize']())
    @dis_commands.check(commands.ml.sub['tokenizator'].sub['tokenize'].acs)
    async def sub_tokenize(self, inter: disnake.CommandInteraction, text: str):
        tokens = word_processing.Tokenizator.tokenize(inter.author.id, text)
        with open('_df.txt', 'w', encoding='utf-8') as f:
            f.write(str(tokens))
        
        tokenized_text = disnake.File('_df.txt', 'tokenized_text.txt')
        embed = disnake.Embed(
            title='Токенизированный текст',
            colour=controller.RANKS_DICT['Чёрный свисток'].colour
        )
        await inter.edit_original_message(embed=embed, file=tokenized_text)
    
    @group_tokenizator.sub_command(**commands.ml.sub['tokenizator'].sub['pre']())
    @dis_commands.check(commands.ml.sub['tokenizator'].sub['pre'].acs)
    async def sub_pre(self, inter: disnake.CommandInteraction, text: str):
        tokens = word_processing.Tokenizator.pre(text)
        with open('_df.txt', 'w', encoding='utf-8') as f:
            f.write(str(tokens))
        
        tokenized_text = disnake.File('_df.txt', 'filtered_text.txt')
        embed = disnake.Embed(
            title='Подготовленный текст',
            colour=controller.RANKS_DICT['Чёрный свисток'].colour
        )
        await inter.edit_original_message(embed=embed, file=tokenized_text)

def setup(bot):
   bot.add_cog(ML(bot))
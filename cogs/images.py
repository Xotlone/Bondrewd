import disnake
from disnake.ext import commands as dis_commands

from anekos import NekosLifeClient

from constants import commands
import controller


class Images(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot
        self.neko = NekosLifeClient()

    @dis_commands.slash_command(**commands.images())
    @dis_commands.check(commands.images.acs)
    async def command_images(self, inter: disnake.CommandInteraction):
        pass

    @command_images.sub_command(**commands.images.sub['action']())
    @dis_commands.check(commands.images.sub['action'].acs)
    async def sub_action(self, inter: disnake.CommandInteraction, action_type: str, user: disnake.Member = None):
        tag = eval(f'SFWImageTags.{action_type.upper()}')
        action_type = commands.ACTION_WORDS[action_type]
        img = await self.neko.image(tag)
        title = f'{inter.author.name} {action_type}'
        if user is not None and user != inter.author:
            title += f' {user.name}'
        else:
            title += '...'
        embed = disnake.Embed(
            title=title,
            colour=controller.RANKS_DICT['Колокольчик'].colour
        )
        embed.set_image(img.url)
        await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(Images(bot))

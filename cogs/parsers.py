import disnake
from disnake.ext import commands as dis_commands

from constants import commands
from constants import config

import utilities
import views


async def highlevel_parser(inter: disnake.CommandInteraction, title: str, count: int, parser: utilities.Parser):
    await inter.response.defer()
    content = parser.try_parse(count)

    if count == 1:
        embed = disnake.Embed(
            title=title,
            color=config.EMBED_COLOR
        )
        embed.set_author(name=inter.author.name, icon_url=inter.author.avatar.url)
        embed.set_image(url=content[0]['image'])
        await inter.send(embed=embed)

    else:
        embeds = []
        for i in range(count):
            embed = disnake.Embed(
                title=f'{title} [{count}]',
                color=config.EMBED_COLOR
            )
            embed.set_author(name=inter.author.name, icon_url=inter.author.avatar.url)
            embed.set_image(url=content[i]['image'])
            embed.set_footer(text=f'Страница {i + 1}/{count}')
            embeds.append(embed)

        await inter.send(embed=embeds[0], view=views.Paginator(embeds))


class Parsers(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot

    @dis_commands.slash_command(**commands.parsers.to_dict())
    async def parsers(self, inter: disnake.CommandInteraction):
        pass

    @parsers.sub_command_group(**commands.parsers.sub['anime'].to_dict())
    @dis_commands.is_nsfw()
    async def parsers_anime(self, inter: disnake.CommandInteraction):
        pass

    @parsers_anime.sub_command(**commands.parsers.sub['anime'].sub['ero'].to_dict())
    async def parsers_anime_ero(self, inter: disnake.CommandInteraction, count: int = 1):
        await highlevel_parser(inter, 'Anime ero', count, utilities.AnimeEroParser())

    @parsers_anime.sub_command(**commands.parsers.sub['anime'].sub['ero-gif'].to_dict())
    async def parsers_anime_ero_gif(self, inter: disnake.CommandInteraction, count: int = 1):
        await highlevel_parser(inter, 'Anime ero gif', count, utilities.AnimeEroGifsParser())

    @parsers_anime.sub_command(**commands.parsers.sub['anime'].sub['monster-girl'].to_dict())
    async def parsers_anime_monster_girl(self, inter: disnake.CommandInteraction, count: int = 1):
        await highlevel_parser(inter, 'Anime ero monster-girl', count, utilities.AnimeMonsterGirlParser())


def setup(bot: dis_commands.Bot):
    bot.add_cog(Parsers(bot))

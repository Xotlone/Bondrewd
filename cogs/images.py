import disnake
from disnake.ext import commands as dis_commands
from disnake import errors

from anekos import NekosLifeClient, SFWImageTags

import utilities
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

    @command_images.sub_command(**commands.images.sub['parse']())
    @dis_commands.check(commands.images.sub['parse'].acs)
    @dis_commands.is_nsfw()
    async def sub_parse(self, inter: disnake.CommandInteraction, parse_type: str = 'Anime'):
        try:
            if parse_type == 'Anime':
                parser = utilities.AnimeParser()
                parsed = parser.try_parse()
                embed = disnake.Embed(
                    title='Аниме',
                    colour=controller.RANKS_DICT['Колокольчик'].colour
                )

            elif parse_type == 'Anime Ero':
                parser = utilities.AnimeEroParser()
                parsed = parser.try_parse()
                embed = disnake.Embed(
                    title='Аниме Эротика',
                    colour=controller.RANKS_DICT['Колокольчик'].colour
                )

            elif parse_type == 'Anime Ero Gifs':
                parser = utilities.AnimeEroGifsParser()
                parsed = parser.try_parse()
                embed = disnake.Embed(
                    title='Аниме Эротика (гифки)',
                    colour=controller.RANKS_DICT['Колокольчик'].colour
                )

            elif parse_type == 'Anime Ears':
                parser = utilities.AnimeEarsParser()
                parsed = parser.try_parse()
                embed = disnake.Embed(
                    title='Аниме Неко (и не только)',
                    colour=controller.RANKS_DICT['Колокольчик'].colour
                )

            elif parse_type == 'Anime Cute':
                parser = utilities.AnimeCuteParser()
                parsed = parser.try_parse()
                embed = disnake.Embed(
                    title='Аниме Няши',
                    colour=controller.RANKS_DICT['Колокольчик'].colour
                )

            elif parse_type == 'Monster Girl':
                parser = utilities.AnimeMonsterGirlParser()
                parsed = parser.try_parse()
                embed = disnake.Embed(
                    title='Monster Girl',
                    colour=controller.RANKS_DICT['Колокольчик'].colour
                )

            elif parse_type == 'Hentai':
                parser = utilities.HentaiParser()
                parsed = parser.try_parse()
                embed = disnake.Embed(
                    title='Хентай',
                    colour=controller.RANKS_DICT['Колокольчик'].colour
                )
                embed.add_field('Название', parsed['title'], inline=False)
                embed.add_field('Описание', parsed['desc'], inline=False)
                embed.add_field('Ссылка', parsed['link'], inline=False)

            else:
                raise Exception(f'Unknown picture_type "{parse_type}"')

            embed.set_image(parsed['image'])
            embed.set_footer(text=parser.link)
            await inter.edit_original_message(embed=embed)

        except errors.InteractionNotResponded:
            await self.sub_parse(inter, parse_type)


def setup(bot):
    bot.add_cog(Images(bot))

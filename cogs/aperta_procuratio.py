import time
from datetime import datetime

import disnake
from disnake.ext import commands
from anekos import SFWImageTags, NSFWImageTags, NekosLifeClient

from configuratione import mandatumes, config
from utilitates import log

class ApertaProcuratio(commands.Cog):
    def __init__(self, machina: commands.Bot):
        self.machina = machina
        self.neko = NekosLifeClient()
    
    @commands.slash_command(**mandatumes.informationes())
    async def informationes(self, inter: disnake.CommandInteraction):
        pass

    @informationes.sub_command(**mandatumes.informationes.sub['mandatumes']())
    async def _mandatumes(self, inter: disnake.CommandInteraction):
        omnia = mandatumes.Mandatum.sort('nomen')
        omnia = ', '.join(map(lambda x: f'`{x.nomen}`', omnia))
        embed = disnake.Embed(
            title='Все мандаты',
            description=omnia,
            colour=config.COLOR
        )
        await inter.send(embed=embed)
    
    @informationes.sub_command(**mandatumes.informationes.sub['mandatum']())
    async def _mandatum(self, inter: disnake.CommandInteraction, nomen: str):
        omnia_nomen = map(lambda m: m.nomen, mandatumes.Mandatum.omnia)
        if nomen.lower() in omnia_nomen:
            mandatum = mandatumes.Mandatum.invenire(nomen.lower())
            embed = disnake.Embed(
                title=f'Мандат "{mandatum.nomen}"',
                description=f'Описание: {mandatum.descriptio}',
                colour=config.COLOR
            )
            await inter.send(embed=embed)

        else:
            embed = disnake.Embed(
                title='Error',
                description=f'Мандат "{nomen}" не найден',
                colour=config.COLOR
            )
            await inter.send(embed=embed)
    
    @commands.slash_command(**mandatumes.ping())
    async def ping(self, inter: disnake.CommandInteraction):
        embed = disnake.Embed(
            title='Задержка отклика',
            description='Вычисление...',
            colour=config.COLOR
        )
        t = time.monotonic()
        await inter.send(embed=embed)
        _ping = round((time.monotonic() - t) * 1000, 2)
        msg = await inter.original_message()
        embed.description = f'{_ping} мс.'
        await msg.edit(embed=embed)
        log(f'\t{_ping} ms.', 'M')
    
    @commands.slash_command(**mandatumes.actio())
    async def actio(self, inter: disnake.CommandInteraction, genus: str, subjecto: disnake.Member=None):
        genus = eval(f'SFWImageTags.{genus.upper()}')
        img = self.neko.image(genus).url
        title = f'{inter.author.name} {genus}'
        if subjecto != None:
            title += f' -> {subjecto.name}'
        embed = disnake.Embed(
            title=title,
            colour=config.COLOR
        )
        embed.set_image(img)
        await inter.send(embed=embed)

def setup(machina):
    machina.add_cog(ApertaProcuratio(machina))
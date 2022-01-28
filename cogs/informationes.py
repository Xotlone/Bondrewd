import time

import disnake
from disnake.ext import commands

from configuratione import mandatumes, config
from utilitates import log
import con_ter

class Informationes(commands.Cog):
    def __init__(self, machina: commands.Bot):
        self.machina = machina

    @commands.slash_command(**mandatumes.informationes())
    @commands.check(mandatumes.informationes.acs)
    async def informationes(self, inter: disnake.CommandInteraction):
        pass

    @informationes.sub_command(**mandatumes.informationes.sub['mandatumes']())
    @commands.check(mandatumes.informationes.sub['mandatumes'].acs)
    async def _mandatumes(self, inter: disnake.CommandInteraction):
        mandatum_omnia = mandatumes.Mandatum.sub_sort('nomen')
        omnia = {k.nomen: [] for k in con_ter.INDEX_OCCASIONES[:-1]}
        for mandatum in mandatum_omnia:
            if mandatum != {}:
                for sub in mandatum.sub.values():
                    omnia[sub.occasiones].append(f'`{mandatum.nomen} {sub.nomen}`')
            else:
                omnia[mandatum.occasiones].append(mandatum.name)

        embed = disnake.Embed(
            title='Все мандаты',
            description='Мандаты разделены на группы. Название каждой группы говорит о требуемом свистке для использования. Бежевая линия слева так-же говорит о требуемом свистке.',
            colour=config.WISTLES['Колокольчик']
        )
        for i, (occasiones, sub) in enumerate(omnia.items()):
            embed.add_field(occasiones, ', '.join(sub), inline=False)
        await inter.send(embed=embed)
    
    @informationes.sub_command(**mandatumes.informationes.sub['mandatum']())
    @commands.check(mandatumes.informationes.sub['mandatum'].acs)
    async def mandatum(self, inter: disnake.CommandInteraction, nomen: str):
        omnia_nomen = map(lambda m: m.nomen, mandatumes.Mandatum.omnia)
        if nomen.lower() in omnia_nomen:
            mandatum = mandatumes.Mandatum.invenire(nomen.lower())
            embed = disnake.Embed(
                title=f'Мандат "{mandatum.nomen}"',
                description=f'Описание: {mandatum.descriptio}',
                colour=config.WISTLES['Колокольчик']
            )
            await inter.send(embed=embed)

        else:
            embed = disnake.Embed(
                title='Error',
                description=f'Мандат "{nomen}" не найден',
                colour=config.ERROR_COLOR
            )
            await inter.send(embed=embed)
    
    @informationes.sub_command(**mandatumes.informationes.sub['avatar']())
    @commands.check(mandatumes.informationes.sub['avatar'].acs)
    async def avatar(self, inter: disnake.CommandInteraction, subjecto: disnake.Member=None):
        if subjecto == None:
            subjecto = inter.author
        embed = disnake.Embed(
            title=f'Аватар {subjecto.name}',
            colour=config.WISTLES['Колокольчик']
        )
        embed.set_image(subjecto.avatar)
        await inter.send(embed=embed)

    @informationes.sub_command(**mandatumes.informationes.sub['ping']())
    @commands.check(mandatumes.informationes.sub['ping'].acs)
    async def ping(self, inter: disnake.CommandInteraction):
        embed = disnake.Embed(
            title='Задержка отклика',
            description='Вычисление...',
            colour=config.WISTLES['Колокольчик']
        )
        t = time.monotonic()
        await inter.send(embed=embed)
        _ping = round((time.monotonic() - t) * 1000, 2)
        msg = await inter.original_message()
        embed.description = f'{_ping} мс.'
        await msg.edit(embed=embed)
        log(f'  {_ping} ms.', 'Mandatum')
   
def setup(machina):
    machina.add_cog(Informationes(machina))
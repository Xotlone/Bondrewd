import time

import disnake
from disnake.ext import commands

from configuratione import mandatumes, config
from utilitates import log, ProgressBar
import con_ter
from apparatus_doctrina import verbum_processing
import errata_fieri
from database import database

class Informationes(commands.Cog):
    def __init__(self, machina: commands.Bot):
        self.machina = machina

    @commands.slash_command(**mandatumes.informationes())
    @commands.check(mandatumes.informationes.acs)
    async def mandatum_informationes(self, inter: disnake.CommandInteraction):
        pass

    @mandatum_informationes.sub_command(**mandatumes.informationes.sub['mandatumes']())
    @commands.check(mandatumes.informationes.sub['mandatumes'].acs)
    async def sub_mandatumes(self, inter: disnake.CommandInteraction):
        mandatum_omnia = mandatumes.Mandatum.sub_sort('nomen')
        omnia = {k: [] for k in con_ter.OCCASIONES_DICT.keys()}
        for mandatum in mandatum_omnia:
            if mandatum.sub != {}:
                for sub1 in mandatum.sub.values():
                    if isinstance(sub1, mandatumes.SubMandatumGroup):
                        for sub2 in sub1.sub.values():
                            omnia[sub2.occasiones].append(f'`{mandatum.nomen} {sub1.nomen} {sub2.nomen}`')
                    
                    else:
                        omnia[sub1.occasiones].append(f'`{mandatum.nomen} {sub1.nomen}`')
            else:
                omnia[mandatum.occasiones].append(f'`{mandatum.nomen}`')
        
        for el in omnia.items():
            if el[1] == []:
                omnia[el[0]] = ['Мандаты отсутствуют']

        embed = disnake.Embed(
            title='Все мандаты',
            description='Мандаты разделены на группы. Название каждой группы говорит о требуемом *свистке* для использования. Линия слева так-же говорит о *свистке*.',
            colour=con_ter.OCCASIONES_DICT['Колокольчик'].colour
        )
        for occasiones, sub in omnia.items():
            embed.add_field(occasiones, ', '.join(sub), inline=False)
        await inter.send(embed=embed)
    
    @mandatum_informationes.sub_command(**mandatumes.informationes.sub['mandatum']())
    @commands.check(mandatumes.informationes.sub['mandatum'].acs)
    async def sub_mandatum(self, inter: disnake.CommandInteraction, nomen: str):
        mandatum_omnia = mandatumes.Mandatum.sub_sort('nomen')
        omnia = {}
        for mandatum in mandatum_omnia:
            if mandatum.sub != {}:
                for sub in mandatum.sub.values():
                    omnia[f'{mandatum.nomen} {sub.nomen}'] = sub
            
            else:
                omnia[mandatum.nomen] = mandatum

        if nomen.lower() in omnia.keys():
            mandatum = omnia[nomen]
            embed = disnake.Embed(
                title=f'Мандат `{nomen}`',
                description=mandatum.descriptio,
                colour=con_ter.OCCASIONES_DICT['Колокольчик'].colour
            )
            await inter.send(embed=embed)

        else:
            embed = disnake.Embed(
                title='Ошибка',
                description=f'Мандат `{nomen}` не найден',
                colour=config.DEFAULT_COLOR
            )
            await inter.send(embed=embed)
    
    @mandatum_informationes.sub_command(**mandatumes.informationes.sub['avatar']())
    @commands.check(mandatumes.informationes.sub['avatar'].acs)
    async def sub_avatar(self, inter: disnake.CommandInteraction, subjecto: disnake.Member=None):
        if subjecto == None:
            subjecto = inter.author

        embed = disnake.Embed(
            title=f'Аватар {subjecto.name}',
            colour=con_ter.OCCASIONES_DICT['Колокольчик'].colour
        )
        embed.set_image(subjecto.avatar)
        await inter.send(embed=embed)

    @mandatum_informationes.sub_command(**mandatumes.informationes.sub['ping']())
    @commands.check(mandatumes.informationes.sub['ping'].acs)
    async def sub_ping(self, inter: disnake.CommandInteraction):
        embed = disnake.Embed(
            title='Задержка отклика',
            description='Вычисление...',
            colour=con_ter.OCCASIONES_DICT['Колокольчик'].colour
        )
        t = time.monotonic()
        await inter.send(embed=embed)
        _ping = round((time.monotonic() - t) * 1000, 2)
        msg = await inter.original_message()
        embed.description = f'{_ping} мс.'
        await msg.edit(embed=embed)
        log(f'  {_ping} мс.', 'Mandatum')
    
    @mandatum_informationes.sub_command(**mandatumes.informationes.sub['sticker']())
    @commands.check(mandatumes.informationes.sub['sticker'].acs)
    async def sub_sticker(self, inter: disnake.CommandInteraction, _id: int):
        sticker = self.machina.get_sticker(_id)
        if sticker == None:
            embed = disnake.Embed(
                title='Стикер не найден',
                colour=config.DEFAULT_COLOR
            )
        
        else:
            descriptio = f'''Название: **{sticker.name}**;
            Описание: {sticker.description if sticker.description != '' else 'Отсутствует'};
            Эмодзи: {sticker.emoji};
            Доступность: `{"Доступен" if sticker.available else "Недоступен"}`;
            Идентификатор: `{sticker.id}`;
            Добавивший: **{sticker.user.name}**;
            Гильдия: **{sticker.guild.name}** (`{sticker.guild_id}`).'''

            embed = disnake.Embed(
                title=f'Стикер "{sticker.name}"',
                description=descriptio,
                colour=con_ter.OCCASIONES_DICT['Колокольчик'].colour
            )
        
        await inter.send(embed=embed)
    
    @mandatum_informationes.sub_command(**mandatumes.informationes.sub['doctrina']())
    @commands.check(mandatumes.informationes.sub['doctrina'].acs)
    async def sub_doctrina_praecepta(self, inter: disnake.CommandInteraction):
        corpus_conditio = int(con_ter.Doctrina.extractio('corpus_conditio'))
        corpus_limit = int(con_ter.Doctrina.extractio('corpus_limit'))
        corpus_longum = verbum_processing.corpus_len()
        corpus_negotium = str(ProgressBar(corpus_limit, corpus_longum, progress=True))
        corpus_descriptio = f'''```py
conditio={corpus_conditio}
limit={corpus_limit}
longum={corpus_longum}
negotium="{corpus_negotium}"```'''

        embed = disnake.Embed(
            title='Doctrina praecepta',
            description=mandatumes.informationes.sub['doctrina'].descriptio,
            colour=con_ter.OCCASIONES_DICT['Колокольчик'].colour
        )
        embed.add_field('Corpus', corpus_descriptio, inline=False)

        await inter.send(embed=embed)
    
    @mandatum_informationes.sub_command(**mandatumes.informationes.sub['member']())
    @commands.check(mandatumes.informationes.sub['member'].acs)
    async def sub_member(self, inter: disnake.CommandInteraction, subjecto: disnake.Member=None):
        if subjecto == None:
            subjecto = inter.author
        
        if subjecto.bot:
            error = ValueError('Subject is bot')
            await errata_fieri.Bot(inter, error)
        
        wistle = con_ter.Wistle.get(int(database(f'SELECT occasione_id FROM users WHERE id = {subjecto.id}', 'one')[0]))
        descriptio = f'''Имя: **{subjecto.name}**;
        Доступ: **{wistle.nomen}**;
        Создан: {disnake.utils.format_dt(subjecto.created_at, style='R')};
        Вступил на сервер: {disnake.utils.format_dt(subjecto.joined_at, style='R')};
        Роли: {", ".join(list(map(lambda role: f'**{role.name}**', subjecto.roles))[1:])};
        Идентификатор: `{subjecto.id}`.'''

        embed = disnake.Embed(
            title=f'О {subjecto.name}',
            description=descriptio,
            colour=subjecto.colour
        )
        embed.set_thumbnail(subjecto.avatar)
        await inter.send(embed=embed)
   
def setup(machina):
    machina.add_cog(Informationes(machina))
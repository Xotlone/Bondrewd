import time

import disnake
from disnake.ext import commands as dis_commands

from constants import commands, config
from utilities import log, ProgressBar
import controller
from ml import word_processing
import exceptions
from database import database


class Information(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot

    @dis_commands.slash_command(**commands.info())
    @dis_commands.check(commands.info.acs)
    async def command_info(self, inter: disnake.CommandInteraction):
        pass

    @command_info.sub_command(**commands.info.sub['commands']())
    @dis_commands.check(commands.info.sub['commands'].acs)
    async def sub_commands(self, inter: disnake.CommandInteraction):
        command_instances = commands.Command.sub_sort('name')
        _instances = {k: [] for k in controller.RANKS_DICT.keys()}
        for command in command_instances:
            if command.sub != {}:
                for sub1 in command.sub.values():
                    if isinstance(sub1, commands.SubCommandGroup):
                        for sub2 in sub1.sub.values():
                            _instances[sub2.access].append(f'`{command.name} {sub1.name} {sub2.name}`')

                    else:
                        _instances[sub1.access].append(f'`{command.name} {sub1.name}`')
            else:
                _instances[command.access].append(f'`{command.name}`')

        for el in _instances.items():
            if not el[1]:
                _instances[el[0]] = ['Команды отсутствуют']

        embed = disnake.Embed(
            title='Все команды',
            description='Команды разделены на группы. Название каждой группы говорит о требуемом *свистке* для '
                        'использования. Линия слева так-же говорит о цвете *свистка*.',
            colour=controller.RANKS_DICT['Колокольчик'].colour
        )
        for access, sub in _instances.items():
            embed.add_field(access, ', '.join(sub), inline=False)
        await inter.edit_original_message(embed=embed)

    @command_info.sub_command(**commands.info.sub['command']())
    @dis_commands.check(commands.info.sub['command'].acs)
    async def sub_command(self, inter: disnake.CommandInteraction, name: str):
        command_instances = commands.Command.sub_sort('name')
        _instances = {}
        for command in command_instances:
            if command.sub != {}:
                for sub in command.sub.values():
                    _instances[f'{command.name} {sub.name}'] = sub

            else:
                _instances[command.name] = command

        if name.lower() in _instances.keys():
            command = _instances[name]
            embed = disnake.Embed(
                title=f'Команда `{name}`',
                description=command.description,
                colour=controller.RANKS_DICT['Колокольчик'].colour
            )
            await inter.edit_original_message(embed=embed)

        else:
            embed = disnake.Embed(
                title='Ошибка',
                description=f'Команда `{name}` не найдена',
                colour=config.DEFAULT_COLOR
            )
            await inter.edit_original_message(embed=embed)

    @command_info.sub_command(**commands.info.sub['avatar']())
    @dis_commands.check(commands.info.sub['avatar'].acs)
    async def sub_avatar(self, inter: disnake.CommandInteraction, user: disnake.Member = None):
        if user is None:
            user = inter.author

        embed = disnake.Embed(
            title=f'Аватар {user.name}',
            colour=controller.RANKS_DICT['Колокольчик'].colour
        )
        embed.set_image(user.avatar)
        await inter.edit_original_message(embed=embed)

    @command_info.sub_command(**commands.info.sub['ping']())
    @dis_commands.check(commands.info.sub['ping'].acs)
    async def sub_ping(self, inter: disnake.CommandInteraction):
        embed = disnake.Embed(
            title='Задержка отклика',
            description='Вычисление...',
            colour=controller.RANKS_DICT['Колокольчик'].colour
        )
        t = time.monotonic()
        await inter.edit_original_message(embed=embed)
        _ping = round((time.monotonic() - t) * 1000, 2)
        msg = await inter.original_message()
        embed.description = f'{_ping} мс.'
        await msg.edit(embed=embed)
        log(f'  {_ping} мс.', 'Command')

    @command_info.sub_command(**commands.info.sub['sticker']())
    @dis_commands.check(commands.info.sub['sticker'].acs)
    async def sub_sticker(self, inter: disnake.CommandInteraction, _id: int):
        sticker = self.bot.get_sticker(_id)
        if sticker is None:
            embed = disnake.Embed(
                title='Стикер не найден',
                colour=config.DEFAULT_COLOR
            )

        else:
            description = f'''Название: **{sticker.name}**;
            Описание: {sticker.description if sticker.description != '' else 'Отсутствует'};
            Эмодзи: {sticker.emoji};
            Доступность: `{"Доступен" if sticker.available else "Недоступен"}`;
            Идентификатор: `{sticker.id}`;
            Добавивший: **{sticker.user.name}**;
            Гильдия: **{sticker.guild.name}** (`{sticker.guild_id}`).'''

            embed = disnake.Embed(
                title=f'Стикер "{sticker.name}"',
                description=description,
                colour=controller.RANKS_DICT['Колокольчик'].colour
            )

        await inter.edit_original_message(embed=embed)

    @command_info.sub_command(**commands.info.sub['ml']())
    @dis_commands.check(commands.info.sub['ml'].acs)
    async def sub_ml_rules(self, inter: disnake.CommandInteraction):
        corpus_condition = int(controller.ML.extract('corpus_condition'))
        corpus_limit = int(controller.ML.extract('corpus_limit'))
        corpus_length = len(word_processing.Tokenizator.corpus_get())
        corpus_fill = str(ProgressBar(corpus_limit, corpus_length, progress=True))
        corpus_description = f'''```py
condition={corpus_condition}
limit={corpus_limit}
length={corpus_length}
fill="{corpus_fill}"```'''

        embed = disnake.Embed(
            title='Информация о ML',
            description=commands.info.sub['ml'].description,
            colour=controller.RANKS_DICT['Колокольчик'].colour
        )
        embed.add_field('Corpus', corpus_description, inline=False)

        await inter.edit_original_message(embed=embed)

    @command_info.sub_command(**commands.info.sub['member']())
    @dis_commands.check(commands.info.sub['member'].acs)
    async def sub_member(self, inter: disnake.CommandInteraction, user: disnake.Member = None):
        if user is None:
            user = inter.author

        if user.bot:
            error = ValueError('User is bot')
            await exceptions.Bot(inter, error)

        wistle = controller.Wistle.get(int(database(f'SELECT rank_id FROM users WHERE id = {user.id}', 'one')[0]))
        description = f'''Имя: **{user.name}**
        Доступ: **{wistle.name}**
        Создан: {disnake.utils.format_dt(user.created_at, style='R')}
        Вступил на сервер: {disnake.utils.format_dt(user.joined_at, style='R')}
        Роли: {", ".join(list(map(lambda role: f'**{role.name}**', user.roles))[1:])}
        Идентификатор: `{user.id}`'''

        embed = disnake.Embed(
            title=f'О {user.name}',
            description=description,
            colour=controller.RANKS_DICT['Колокольчик'].colour
        )
        embed.set_thumbnail(user.avatar)
        await inter.edit_original_message(embed=embed)

    @command_info.sub_command(**commands.info.sub['rating']())
    @dis_commands.check(commands.info.sub['rating'].acs)
    async def sub_rating(self, inter: disnake.CommandInteraction, ml: str):
        if ml == 'corpus':
            corpus_rating = word_processing.Tokenizator.update_rating()
            corpus_len = len(word_processing.Tokenizator.corpus_get())
            proc = word_processing.normed_exponential_func([int(x[1]) / corpus_len for x in corpus_rating])
            users_list = '\n'.join([f'{i + 1}. **{self.bot.get_user(int(a)).name}**: `{c}` '
                                    f'{round(proc[i] * 100, 2)}%' for i, (a, c) in enumerate(corpus_rating.items())][
                                   :10])

            embed = disnake.Embed(
                title='Рейтинг вклада в корпус',
                description=users_list,
                colour=controller.RANKS_DICT['Колокольчик'].colour
            )
            await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))

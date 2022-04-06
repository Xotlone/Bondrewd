import time
import csv

import disnake
from disnake.ext import commands as dis_commands
from matplotlib import pyplot as plt

from constants import commands, config
from utilities import log
import controller
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
            _instances[command.access].append(f'\n{command.name}')
            if command.sub != {}:
                prev_access = None
                for sub1 in command.sub.values():
                    if command.access != sub1.access and (prev_access is None or prev_access != sub1.access):
                        _instances[sub1.access].append(f'\n{command.name}')
                        prev_access = sub1.access
                    _instances[sub1.access].append(f'|  {sub1.name}')
                    if isinstance(sub1, commands.SubCommandGroup):
                        for sub2 in sub1.sub.values():
                            if sub1.access != sub2.access and prev_access != sub2.access:
                                _instances[sub2.access].append(f'\n{command.name}')
                                _instances[sub2.access].append(f'|  {sub1.name}')
                                prev_access = sub2.access
                            _instances[sub2.access].append(f'|  |  {sub2.name}')

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
            backslashed_sub = '\n'.join(sub)
            embed.add_field(access, f'```{backslashed_sub}```', inline=False)
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

    @command_info.sub_command(**commands.info.sub['ram']())
    @dis_commands.check(commands.info.sub['ram'].acs)
    async def sub_ram(self, inter: disnake.CommandInteraction):
        x, y = [], []
        with open('temp/ram.csv') as csv_file:
            data = csv.reader(csv_file)
            for row in data:
                x.append(int(row[0]))
                y.append(int(row[1]))

        local_max = [0, 0]
        for i, j in zip(x, y):
            if local_max[1] < j:
                local_max = [i, j]

        plt.plot(x, y, 'c-')
        plt.xlabel('Время (секунды)')
        plt.ylabel('Потребление (МБ)')
        plt.title('Потребление ОЗУ')
        plt.ylim(0, 500)
        plt.annotate(local_max[1], local_max)
        plt.savefig(fname='temp/ram_plot.png', format='png')
        plt.close()

        embed = disnake.Embed(
            title='Потребление ОЗУ',
            colour=controller.RANKS_DICT['Колокольчик'].colour
        )
        embed.set_image(file=disnake.File('temp/ram_plot.png'))
        await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))

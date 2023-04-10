from math import exp

import disnake
from disnake.ext import commands as dis_commands
from disnake.utils import format_dt

from constants import commands
from constants import config
from database import cursor
from utilities import ProgressBar, log, normed_exponential
import economy
import views


class Info(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot

    @dis_commands.slash_command(**commands.info.to_dict())
    async def info(self, inter: disnake.CommandInteraction):
        pass

    @info.sub_command(**commands.info.sub['commands'].to_dict())
    async def info_commands(self, inter: disnake.CommandInteraction):
        all_commands = commands.Command.sort()

        def recursive_sort(cmds: list, _depth: int = 0):
            out_text = []
            for cmd in cmds:
                out_text.append(f'{"--" * _depth}{cmd.name}')
                if cmd.sub is not None:
                    out_text.append(recursive_sort(cmd.sub_sort(), _depth + 1))
            return '\n'.join(out_text)

        sorted_commands = recursive_sort(all_commands)
        embed = disnake.Embed(
            title='Команды',
            description=f'```yaml\n{sorted_commands}```',
            color=config.EMBED_COLOR
        )

        async def select_callback(select: disnake.ui.Select, select_inter: disnake.MessageInteraction):
            selected_command = commands.get_command(select.values[0])
            sorted_subcommands = recursive_sort([selected_command])
            command_embed = disnake.Embed(
                title=f'Команда {selected_command.name}',
                description=f'```yaml\n{sorted_subcommands}```',
                color=config.EMBED_COLOR
            )
            await select_inter.response.edit_message(embed=command_embed)

        await inter.send(embed=embed, view=views.DropdownView(
            'Конкретная команда',
            [disnake.SelectOption(label=command.name) for command in all_commands],
            select_callback
        ))

    @info.sub_command(**commands.info.sub['member'].to_dict())
    async def info_member(self, inter: disnake.CommandInteraction, member: disnake.Member = None):
        if member is None:
            member = inter.author

        if not member.bot:
            # db data
            _, activity_scores = cursor(f'SELECT * FROM users WHERE id = {member.id}')

            level, scores = economy.scores_to_levels(activity_scores).values()
            scores_progress = ProgressBar(economy.levels_cost[level - 1], scores, advanced=True)

            embed = disnake.Embed(
                title='Про участника',
                description=f'''Участник: **{member}** (`{member.id}`)
    Уровень: {level}
    Очки [{activity_scores}]: {str(scores_progress)}
    Создан: {format_dt(member.created_at)} ({format_dt(member.created_at, style='R')})
    Присоединился: {format_dt(member.joined_at)} ({format_dt(member.joined_at, style='R')})
    Роли [{len(member.roles) - 1}]: {", ".join(map(lambda role: role.name, member.roles[1:]))}''',
                color=member.top_role.color
            )
        else:
            embed = disnake.Embed(
                title='Про участника',
                description=f'''Участник: **{member}** (`{member.id}`)
                Создан: {format_dt(member.created_at)} ({format_dt(member.created_at, style='R')})
                Присоединился: {format_dt(member.joined_at)} ({format_dt(member.joined_at, style='R')})
                Роли [{len(member.roles) - 1}]: {", ".join(map(lambda role: role.name, member.roles[1:]))}''',
                color=member.top_role.color
            )
        embed.set_thumbnail(member.avatar.url)
        await inter.send(embed=embed)

    @info.sub_command(**commands.info.sub['server'].to_dict())
    async def info_server(self, inter: disnake.CommandInteraction):
        guild = inter.guild
        embed = disnake.Embed(
            title='Про сервер',
            description=f'''Название: **{guild.name}** (`{guild.id}`)
Владелец: **{guild.owner.name}** (`{guild.owner.id}`)
Создан: {format_dt(guild.created_at)} ({format_dt(guild.created_at, style='R')})
Вы вступили: {format_dt(guild.me.joined_at)} ({format_dt(guild.me.joined_at, style='R')})''',
            color=config.EMBED_COLOR
        )
        embed.add_field(
            f'Участники [{guild.member_count}]',
            f'''Пользователей: **{len(list(filter(lambda member: not member.bot, guild.members)))}**
Онлайн: **{len(list(filter(lambda member: member.status == disnake.Status.online, guild.members)))}**
Оффлайн: **{len(list(filter(lambda member: member.status == disnake.Status.offline, guild.members)))}**
Боты: **{len(list(filter(lambda member: member.bot, guild.members)))}**'''
        )
        embed.add_field(
            'Другое',
            f'''Количество ролей: **{len(guild.roles) - 1}**
Количество эмодзи: **{len(guild.emojis)}**'''
        )
        embed.add_field(
            'Статистика',
            '`Пусто`'
        )
        await inter.send(embed=embed)

    @info.sub_command(**commands.info.sub['rating'].to_dict())
    async def info_rating(self, inter: disnake.CommandInteraction):
        users_db = cursor('SELECT * FROM users')
        named_db = []
        for user in users_db:
            user_id, user_scores = user
            disnake_user = self.bot.get_user(user_id)
            if disnake_user is not None:
                named_db.append([disnake_user.name, user_scores])
            else:
                cursor(f'DELETE FROM users WHERE id = {user_id}')
                log(f'Пользователь с id {user_id} удалён из таблицы', 'DELETE')
        sorted_db = sorted(named_db, key=lambda user: user[1], reverse=True)

        nef_scores = normed_exponential(list(map(lambda x: x[1], sorted_db)))
        nef_scores = list(map(lambda x: round(x * 100, 2), nef_scores))
        for idx, user in enumerate(sorted_db):
            user.append(nef_scores[idx])

        def slice_list(list, size):
            return [list[i:i + size] for i in range(0, len(list), size)]

        sliced_db = slice_list(sorted_db, 10)
        embeds = [disnake.Embed(
            title=f'Рейтинг ({idx + 1}/{len(sliced_db)})',
            description='\n'.join([f'{id_user + 1 + (idx * 10)}.**{user[0]}** [{user[1]}] '
                                   f'{str(ProgressBar(100, user[2]))} {user[2]}%' for id_user,
                                                                           user in enumerate(
                users)]),
            color=config.EMBED_COLOR
        ) for idx, users in enumerate(sliced_db)]
        await inter.send(embed=embeds[0], view=views.Paginator(embeds))


def setup(bot: dis_commands.Bot):
    bot.add_cog(Info(bot))

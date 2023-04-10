import time
import re

import disnake
from disnake.ext import commands as dis_commands

import database
from database import cursor
from utilities import log
from constants import config
import economy


async def log_chnl(guild: disnake.Guild, text: str):
    logging_chnl = cursor(f'SELECT logging_chnl FROM guilds WHERE id = {guild.id}')[0]
    if logging_chnl != 0:
        await guild.get_channel(logging_chnl).send(embed=disnake.Embed(
            color=config.EMBED_COLOR,
            title='Лог',
            description=text
        ))


class Events(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot

    @dis_commands.Cog.listener()
    async def on_connect(self):
        log('Инициализация базы данных...', 'INIT')
        database.init()
        database.insert(users=self.bot.users, guilds=await self.bot.fetch_guilds().flatten())
        log('Соединение установлено', 'INIT')

    @dis_commands.Cog.listener()
    async def on_disconnect(self):
        log('Соединение разорвано', 'EVENT')

    @dis_commands.Cog.listener()
    async def on_resumed(self):
        log('Соединение восстановлено', 'EVENT')

    @dis_commands.Cog.listener()
    async def on_message(self, msg: disnake.Message):
        if not msg.author.bot:
            log(f'#{msg.channel.name} -> @{msg.author} отправил сообщение: {msg.content}', 'MESSAGE')

            await economy.message_check(msg)

    @dis_commands.Cog.listener()
    async def on_message_delete(self, msg: disnake.Message):
        if not msg.author.bot:
            await log_chnl(msg.guild, f'{msg.channel.mention} -> {msg.author} удалено сообщение: {msg.content}')
            log(f'#{msg.channel.name} -> @{msg.author} удалено сообщение: {msg.content}', 'LOGGING')

    @dis_commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        if not before.author.bot:
            await log_chnl(before.guild,
                           f'{before.channel.mention} -> {before.author} изменено сообщение: {before.content} -> '
                           f'{after.content}')
            log(f'#{before.channel.name} -> @{before.author} изменено сообщение: {before.content} -> {after.content}',
                'LOGGING')

    @dis_commands.Cog.listener()
    async def on_slash_command(self, inter: disnake.ApplicationCommandInteraction):
        log(f'#{inter.channel.name} -> @{inter.author} вызвал команду {inter.application_command.name}', 'COMMAND')
        config.command_time = time.time()

    @dis_commands.Cog.listener()
    async def on_slash_command_completion(self, inter: disnake.ApplicationCommandInteraction):
        log(f'Команда {inter.application_command.name} завершена за {round(time.time() - config.command_time, 2)}с.',
            'COMMAND')

    @dis_commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        log(f'Наначи добавлена на сервер {guild.name}', 'EVENT')
        database.insert(guilds=[guild])

    @dis_commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        log(f'#{member.name} присоединился к серверу {member.guild.name}', 'EVENT')
        database.insert(users=[member])

    @dis_commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        await log_chnl(member.guild, f'{member.mention} покинул сервер {member.guild.name}')
        log(f'@{member} покинул сервер {member.guild.name}', 'EVENT')


def setup(bot: dis_commands.Bot):
    bot.add_cog(Events(bot))

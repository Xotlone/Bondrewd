import time

import disnake
from disnake.ext import commands as dis_commands

from database import database
from constants import config
from utilities import log
import controller
from ml import word_processing


class Events(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot

    async def send_logging(self, guild_id: int, text: str):
        channel_id = database(f'SELECT logging FROM servers_settings WHERE id = {guild_id}', 'one')[0]
        if channel_id != 0:
            channel = self.bot.get_channel(channel_id)
            embed = disnake.Embed(
                title='Лог',
                description=text,
                colour=disnake.Colour.yellow()
            )
            await channel.send(embed=embed)

    @dis_commands.Cog.listener()
    async def on_connect(self):
        await controller.initialization(self.bot)
        config.owner_id = self.bot.owner_id
        log('Инициализация ML', 'ML')

        log_msg = f'Подключение за {round(time.time() - config.connect_time, 2)} с.'
        log(log_msg, 'Event')
        async for guild in self.bot.fetch_guilds(limit=None):
            await self.send_logging(guild.id, log_msg)

    @dis_commands.Cog.listener()
    async def on_disconnect(self):
        config.shutdown_time = time.time()
        log('Отключение', 'Event')
    
    @dis_commands.Cog.listener()
    async def on_resumed(self):
        log_msg = f'Соединение восстановлено за {round(time.time() - config.shutdown_time, 2)} с.'
        log(log_msg, 'Event')
        async for guild in self.bot.fetch_guilds(limit=None):
            await self.send_logging(guild.id, log_msg)
    
    @dis_commands.Cog.listener()
    async def on_message(self, msg: disnake.Message):
        if msg.author.bot:
            return
    
    @dis_commands.Cog.listener()
    async def on_slash_command(self, inter: disnake.ApplicationCommandInteraction):
        log(f'Выполнение "{inter.application_command.name}"', 'Command')
        config.command_time = time.time()
    
    @dis_commands.Cog.listener()
    async def on_slash_command_completion(self, inter: disnake.CommandInteraction):
        t = round(time.time() - config.command_time, 2)
        log(f'  Команда выполнена за {t} с.', 'Command')
    
    @dis_commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        log(f'Присоединение к гильдии "{guild.name}"', 'E')

        if guild.id not in map(lambda a: a[0], database('SELECT id FROM servers_settings', 'all')):
            database(f'INSERT INTO servers_settings VALUES ({guild.id})')
            log(f'   Сервер "{guild.name}" добавлен в таблицу')

        for member in guild.members:
            if member.id not in map(lambda a: a[0], database('SELECT id FROM users', 'all')) and not member.bot:
                if await self.bot.is_owner(member):
                    new_member = controller.User(member.id, 5)
                
                else:
                    new_member = controller.User(member.id, 0)

                new_member.insert()
                log(f'Записан новый участник {member.name}', 'Event')
    
    @dis_commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot or message.content == '':
            return
        
        log(f'{message.author.name}: "{message.content}"', 'Message')
        
        corpus_condition = int(database('SELECT condition FROM ml WHERE name = \'corpus_condition\'', 'one')[0])
        corpus_limit = int(database('SELECT condition FROM ml WHERE name = \'corpus_limit\'', 'one')[0])
        if corpus_condition and corpus_limit < 100000:
            word_processing.Tokenizator.corpus_update(message.author.id, message.content)

    @dis_commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        if message.author.bot:
            return

        log_msg = f'Сообщение автора {message.author.name} удалено "{message.content}"'
        log(log_msg, 'Message')
        await self.send_logging(message.guild.id, log_msg)

    @dis_commands.Cog.listener()
    async def on_message_edit(self, before: disnake.Message, after: disnake.Message):
        if before.author.bot:
            return

        log_msg = f'Сообщение автора {before.author.name} изменено "{before.content}" -> "{after.content}"'
        log(log_msg, 'Message')
        await self.send_logging(before.guild.id, log_msg)


def setup(bot):
    bot.add_cog(Events(bot))

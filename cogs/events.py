import time

import disnake
from disnake.ext import commands as dis_commands

from database import database
from constants import config
from utilities import log
import controller
from ml import word_processing

class Events(dis_commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @dis_commands.Cog.listener()
    async def on_connect(self):
        await controller.initialization(self.bot)
        config.owner_id = self.bot.owner_id
        log('Инициализация ML', 'ML')
        word_processing.Tokenizator.corpus_init()
        log(f'Подключён за {round(time.time() - config.connect_time, 2)} с.', 'Event')

    @dis_commands.Cog.listener()
    async def on_disconnect(self):
        config.shutdown_time = time.time()
        log('Отключение', 'Event')
    
    @dis_commands.Cog.listener()
    async def on_resumed(self):
        log(f'Соединение восстановлено за {round(time.time() - config.shutdown_time, 2)} с.', 'Event')
    
    @dis_commands.Cog.listener()
    async def on_message(self, msg: disnake.Message):
        if msg.author.bot:
            return
    
    @dis_commands.Cog.listener()
    async def on_slash_command(self, inter: disnake.ApplicationCommandInteraction):
        log(f'Выполнение "{inter.application_command.name}"', 'Command')
        config.command_time = time.time()
        
        await inter.response.defer()
    
    @dis_commands.Cog.listener()
    async def on_slash_command_completion(self, inter: disnake.CommandInteraction):
        t = round(time.time() - config.command_time, 2)
        log(f'  Команда выполнена за {t} с.', 'Command')
    
    @dis_commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        log(f'Присоединён к гильдии "{guild.name}"', 'E')

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
            print(word_processing.Tokenizator.update_rating())
    
def setup(bot):
    bot.add_cog(Events(bot))

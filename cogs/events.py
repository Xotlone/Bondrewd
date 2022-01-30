import time

import disnake
from disnake.ext import commands

from database import database
from configuratione import config
from utilitates import log
import con_ter
from apparatus_doctrina import verbum_processing

class Events(commands.Cog):
    def __init__(self, machina):
        self.machina = machina

    @commands.Cog.listener()
    async def on_connect(self):
        await con_ter.initialization(self.machina)
        config.owner_id = self.machina.owner_id
        log(f'Подключён за {round(time.time() - config.satus_tempus, 2)} с.', 'Event')

    @commands.Cog.listener()
    async def on_disconnect(self):
        config.shutdown_tempore = time.time()
        log('Отключение', 'Event')
    
    @commands.Cog.listener()
    async def on_resumed(self):
        log(f'Соеденение восстановлено за {round(time.time() - config.shutdown_tempore, 2)} с.', 'Event')
    
    @commands.Cog.listener()
    async def on_message(self, msg: disnake.Message):
        if msg.author.bot:
            return
    
    @commands.Cog.listener()
    async def on_slash_command(self, inter: disnake.ApplicationCommandInteraction):
        log(f'Выполнение "{inter.application_command.name}"', 'Mandatum')
        config.mandatum_tempus = time.time()
    
    @commands.Cog.listener()
    async def on_slash_command_completion(self, inter: disnake.CommandInteraction):
        tempus = round(time.time() - config.mandatum_tempus, 2)
        log(f'  Мандат выполнен за {tempus} с.', 'Mandatum')
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        log(f'Присоединён к гильдии "{guild.name}"', 'E')

        for member in guild.members:
            if member.id not in map(lambda a: a[0], database('SELECT id FROM users', 'all')) and not member.bot:
                if await self.machina.is_owner(member):
                    novum_membrum = con_ter.User(member.id, 5)
                
                else:
                    novum_membrum = con_ter.User(member.id, 0)

                novum_membrum.ingressum()
                log(f'Записан новый участник {member.name}', 'Event')
    
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot or message.content == '':
            return
        
        log(f'{message.author.name}: "{message.content}"', 'Message')
        
        corpus_conditio = int(database('SELECT conditio FROM doctrina WHERE nomen = \'corpus_conditio\'', 'one')[0])
        corpus_limit = int(database('SELECT conditio FROM doctrina WHERE nomen = \'corpus_limit\'', 'one')[0])
        if corpus_conditio and corpus_limit < 100000:
            verbum_processing.corpus_addition(message.author.id, message.content)
    
def setup(machina):
    machina.add_cog(Events(machina))

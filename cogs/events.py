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
        database.executio('tabulas_creando')
        con_ter.initialization()
        log(f'Подключён за {round(time.time() - config.satus_tempus, 2)} с.', 'Event')

    @commands.Cog.listener()
    async def on_disconnect(self):
        config.shutdown_tempore = time.time()
        log('Отключение', 'Event')
    
    @commands.Cog.listener()
    async def on_resumed(self):
        log(f'Соеденение восстановлено за {time.time() - config.shutdown_tempore} с.', 'Event')
    
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

        for particeps in guild.members:
            if particeps.id not in database('SELECT id FROM users', 'all'):
                if particeps == guild.owner:
                    alpha_id = con_ter.INDEX_ACCESSUM_CAMPESTER[-1].id
                    novum_membrum = con_ter.User(particeps.id, alpha_id)
                
                else:
                    omega_id = con_ter.INDEX_ACCESSUM_CAMPESTER[0].id
                    novum_membrum = con_ter.User(particeps.id, omega_id)

                novum_membrum.ingressum()
                log(f'Записан новый участник {particeps.name}', 'Event')
    
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot or message.content == '':
            return
        
        log(f'{message.author.name}: "{message.content}"', 'Message')
        
        corpus_conditio = bool(database('SELECT conditio FROM doctrina WHERE nomen = \'corpus_conditio\'', 'one')[0])
        corpus_limit = int(database('SELECT conditio FROM doctrina WHERE nomen = \'corpus_limit\'', 'one')[0])
        if corpus_conditio and corpus_limit < 100000:
            verbum_processing.corpus_addition(message.author.id, message.content)
        
        elif corpus_limit >= 100000:
            log('КОРПУС ЗАПОЛНЕН', 'DOCTRINA')
    
def setup(machina):
    machina.add_cog(Events(machina))

import datetime
import time

import disnake
from disnake.ext import commands

from database import database
from configuratione import config
from utilitates import monospace, log
import controlatoris_terminus

class Events(commands.Cog):
    def __init__(self, machina):
        self.machina = machina

    @commands.Cog.listener()
    async def on_connect(self):
        database.executio('tabulas_creando')
        controlatoris_terminus.initialization()
        log(f'Coniuncta in {round(time.time() - config.satus_tempus, 2)} s.', 'E')

    @commands.Cog.listener()
    async def on_disconnect(self):
        config.shutdown_tempore = time.time()
        log('Shutdown', 'E')
    
    @commands.Cog.listener()
    async def on_resumed(self):
        log(f'Connexionem resumitur post {time.time() - config.shutdown_tempore} seconds', 'e')
    
    @commands.Cog.listener()
    async def on_message(self, msg: disnake.Message):
        if msg.author.bot:
            return

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.CommandInteraction, error: commands.CommandError):
        #log(error, 'E', 'error')
        embed = disnake.Embed(
            title=monospace('Error'),
            description=f'`{error}`',
            colour=disnake.Color.red()
        )
        await inter.send(embed=embed, file=disnake.File('logs.log'))
    
    @commands.Cog.listener()
    async def on_slash_command(self, inter: disnake.CommandInteraction):
        log(f'"{inter.application_command.name}"', 'M')
        config.mandatum_tempus = time.time()
    
    @commands.Cog.listener()
    async def on_slash_command_completion(self, inter: disnake.CommandInteraction):
        tempus = round(time.time() - config.mandatum_tempus, 2)
        log(f'\t"{inter.application_command.name}" mandatum completur in {tempus} s.', 'M')
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        log(f'Joenium collegium {guild.name}', 'E')

        for particeps in guild.members:
            if particeps.id not in database('SELECT id FROM users', 'all'):
                omega_id = controlatoris_terminus.INDEX_ACCESSUM_CAMPESTER[0].id
                novum_membrum = controlatoris_terminus.Users(particeps.id, omega_id)
                novum_membrum.ingressum()
                log(f'Novum particeps {particeps.name}', 'E')
    
def setup(machina):
    machina.add_cog(Events(machina))

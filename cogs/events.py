import datetime
import logging
import time

import discord
from configuratione import config
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.model import SlashMessage

import database
from configuratione import config

log = logging.getLogger('logs')

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    def log_ev(self, text: str):
        log.info(f'E> {text}')

    @commands.Cog.listener()
    async def on_connect(self):
        database.database.executio('tabulas_creando')
        self.log_ev(f'Coniuncta in {round(time.time() - config.SATUS_TEMPUS, 1)} secundis')

    @commands.Cog.listener()
    async def on_disconnect(self):
        config.SHUTDOWN_TEMPORE = time.time()
        self.log_ev('Shutdown')
    
    @commands.Cog.listener()
    async def on_resumed(self):
        self.log_ev(f'Connexionem resumitur post {time.time() - config.SHUTDOWN_TEMPORE} seconds')
    
    @commands.Cog.listener()
    async def on_message(self, msg: SlashMessage):
        if msg.author.bot:
            return

    @commands.Cog.listener()
    async def on_command_error(self, ctx: SlashContext):
        pass
    
    @commands.Cog.listener()
    async def on_commands(self, ctx: SlashContext):
        log.info(f'M> {ctx.command.name}')
    
    @commands.Cog.listener()
    async def on_command_completion(self, ctx: SlashContext):
        log.info(f'\t{ctx.command.name} mandatum completur')
    
def setup(client):
    client.add_cog(Events(client))

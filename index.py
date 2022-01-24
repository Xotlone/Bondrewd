import time

from configuratione import config

config.SATUS_TEMPUS = time.time()

import logging
import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

file_log = logging.FileHandler('logs.log', encoding='utf-8')
console_out = logging.StreamHandler()
logging_level = logging.INFO
logging.basicConfig(
    handlers=(file_log, console_out),
    format='[%(asctime)s] %(message)s',
    level=logging_level
)
log = logging.getLogger('logs')

load_dotenv('.env')

intents = discord.Intents.all()
machina = commands.Bot(command_prefix='/', intents=intents)
machina.remove_command('help')
slash = SlashCommand(machina, sync_commands=True, sync_on_cog_reload=True)

for cog_name in os.listdir('./cogs'):
    if cog_name.endswith('.py'):
        machina.load_extension(f'cogs.{cog_name[:-3]}')

machina.run(os.getenv('TOKEN'))

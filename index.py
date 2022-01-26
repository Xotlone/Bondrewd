import time

from configuratione import config
config.satus_tempus = time.time()

import logging
import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

from utilitates import log

file_log = logging.FileHandler('logs.log', 'w', 'utf-8')
console_out = logging.StreamHandler()
logging_level = logging.INFO
logging.basicConfig(
    handlers=(file_log, console_out),
    format='[%(asctime)s] %(message)s',
    level=logging_level
)

load_dotenv('.env')

intents = disnake.Intents.all()
machina = commands.Bot(command_prefix='/', intents=intents)
machina.remove_command('help')

log('Cogs loading', 'L')
for cog_name in os.listdir('./cogs'):
    if cog_name.endswith('.py'):
        machina.load_extension(f'cogs.{cog_name[:-3]}')
        log(f'\t{cog_name[:-3]} loaded', 'L')

machina.run(os.getenv('TOKEN'))

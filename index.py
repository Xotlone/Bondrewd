import time

from constants import config
config.connect_time = time.time()

import logging
import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

from utilities import log

file_log = logging.FileHandler('logs.log', 'w', 'utf-8')
console_out = logging.StreamHandler()
logging_level = logging.INFO
logging.basicConfig(
    handlers=(file_log, console_out),
    format='[%(asctime)s] - %(message)s',
    level=logging_level
)

load_dotenv('.env')

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)
bot.remove_command('help')

log('Загрузка модулей', 'Loading')
for cog_name in os.listdir('./cogs'):
    if cog_name.endswith('.py'):
        bot.load_extension(f'cogs.{cog_name[:-3]}')
        log(f'  {cog_name[:-3]} загружен', 'Loading')

bot.run(os.getenv('TOKEN'))

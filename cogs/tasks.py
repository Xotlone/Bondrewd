import csv
import time

import disnake
from disnake.ext import commands as dis_commands, tasks
from memory_profiler import memory_usage

from constants import config


class Tasks(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot
        self.ram_read.start()

    def cog_unload(self):
        self.ram_read.cancel()

    @tasks.loop(seconds=config.RAM_READ_DELAY)
    async def ram_read(self):
        with open('temp/ram.csv', 'a', newline='') as csv_file:
            ram_writer = csv.writer(csv_file)
            ram_writer.writerow([int(time.time() - config.connect_time), int(memory_usage()[0])])


def setup(bot):
    bot.add_cog(Tasks(bot))

from math import *
import time
import asyncio

import disnake
from disnake.ext import commands as dis_commands
import numpy as np
import serial

from constants import commands
from constants import config


class Useful(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.arduino = serial.Serial(port='COM7', baudrate=115200, timeout=.1)
        self.bot = bot

    @dis_commands.slash_command(**commands.useful.to_dict())
    async def useful(self, inter: disnake.CommandInteraction):
        pass

    @useful.sub_command(**commands.useful.sub['calculator'].to_dict())
    async def useful_calculator(self, inter: disnake.CommandInteraction, condition: str):
        try:
            cond = f'{condition} = {eval(condition)}'
            embed = disnake.Embed(
                title='Калькулятор',
                description=cond,
                color=config.EMBED_COLOR
            )
        except NameError:
            embed = disnake.Embed(
                title='Калькулятор',
                description=f'Выражение `{condition}` не верно',
                color=disnake.Color.red()
            )

        await inter.send(embed=embed)

    @useful.sub_command(**commands.useful.sub['microcontroller_test'].to_dict())
    async def useful_microcontroller_test(self, inter: disnake.CommandInteraction, angle: int):
        await inter.response.defer()

        async def servo(angle: int):
            self.arduino.write(bytes(str(angle), 'utf-8'))
            await asyncio.sleep(0.05)
            return self.arduino.readline().decode('utf-8')

        answer = await servo(angle)

        embed = disnake.Embed(
            title='Ответ микроконтроллера',
            description=answer,
            color=config.EMBED_COLOR
        )

        await inter.send(embed=embed)


def setup(bot: dis_commands.Bot):
    bot.add_cog(Useful(bot))

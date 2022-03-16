import os

import pandas as pd
from psycopg2 import errors
import disnake
from disnake.ext import commands as dis_commands

from constants import commands
import controller
from database import database
import exceptions
from ml import word_processing
from utilities import ProgressBar

class Spotter(dis_commands.Cog):
    def __init__(self, bot: dis_commands.Bot):
        self.bot = bot
    
    @dis_commands.slash_command(**commands.manual_viscus())
    @dis_commands.check(commands.manual_viscus.acs)
    async def command_manual_execute(self, inter: disnake.CommandInteraction, request: str):
        try:
            request = database(request, 'all')
            embed = disnake.Embed(
                title='Прямой запрос',
                description=f'```{request}```',
                colour=controller.RANKS_DICT['Белый свисток'].colour
            )
            await inter.edit_original_message(embed=embed)

        except errors.SyntaxError as error:
            await exceptions.DBSyntax.call(inter, error, request)
        
        except errors.UndefinedColumn as error:
            await exceptions.DBUndefinedColumn.call(inter, error)

        except errors.ProgrammingError:
            embed = disnake.Embed(
                title='Прямой запрос',
                description=f'`True`',
                colour=controller.RANKS_DICT['Белый свисток'].colour
            )
            await inter.edit_original_message(embed=embed)

    @dis_commands.slash_command(**commands.extract())
    @dis_commands.check(commands.extract.acs)
    async def command_extract(self, inter: disnake.CommandInteraction):
        pass

    @command_extract.sub_command(**commands.extract.sub['param']())
    @dis_commands.check(commands.extract.sub['param'].acs)
    async def sub_param(self, inter: disnake.CommandInteraction, type: str, key: str=''):
        try:
            if key != '':
                key = f'WHERE {key}'
            
            param = database(f'SELECT * FROM {type} {key}', 'all')

            column = database(f'SELECT column_name FROM information_schema.columns WHERE table_schema = \'public\' AND table_name=\'{type}\'', 'all')
            column = list(map(lambda c: c[0], column))
            table = pd.DataFrame(param, columns=column)

            embed = disnake.Embed(
                title='Ответ',
                description=f'```{table}```',
                colour=controller.RANKS_DICT['Красный свисток'].colour
            )
            await inter.edit_original_message(embed=embed)

        except errors.SyntaxError as error:
            await exceptions.DBSyntax.call(inter, error)
        
        except errors.UndefinedColumn as error:
            await exceptions.DBUndefinedColumn.call(inter, error, key)

    @command_extract.sub_command(**commands.extract.sub['ml']())
    @dis_commands.check(commands.extract.sub['ml'].acs)
    async def sub_ml_data(self, inter: disnake.CommandInteraction, key: str):
        if key == 'corpus':
            limit = int(controller.ML.extract('corpus_limit'))
            if os.path.exists('ml/corpus.csv'):
                corpus = disnake.File('ml/corpus.csv')
                pb = str(ProgressBar(limit, len(word_processing.Tokenizator.corpus_get()), progress=True))
                embed = disnake.Embed(
                    title='Словарный корпус',
                    description=f'Заполненность {pb}',
                    colour=controller.RANKS_DICT['Чёрный свисток'].colour
                )
                await inter.edit_original_message(embed=embed, file=corpus)
            
            else:
                embed = disnake.Embed(
                    title='Корпус не обнаружен',
                    colour=controller.RANKS_DICT['Чёрный свисток'].colour
                )
                await inter.edit_original_message(embed=embed)
    
    @dis_commands.slash_command(**commands.inserta())
    @dis_commands.check(commands.inserta.acs)
    async def command_insert(self, inter: disnake.CommandInteraction):
        pass
    
    @command_insert.sub_command(**commands.inserta.sub['param']())
    @dis_commands.check(commands.inserta.sub['param'].acs)
    async def sub_param(self, inter: disnake.CommandInteraction, type: str, value: str):
        try:
            database(f'INSERT INTO {type} VALUES ({value})')
            request = database(f'SELECT * FROM {type}', 'all')[-10:]

            column = database(f'SELECT column_name FROM information_schema.columns WHERE table_schema = \'public\' AND table_name=\'{type}\'', 'all')
            column = list(map(lambda c: c[0], column))
            table = pd.DataFrame(request, columns=column)

            embed = disnake.Embed(
                title='Параметры успешно добавлены',
                description=f'```{table}```',
                colour=controller.RANKS_DICT['Синий свисток'].colour
            )
            await inter.edit_original_message(embed=embed)
        
        except errors.SyntaxError as error:
            await exceptions.DBSyntax.call(inter, error)
        
        except errors.UndefinedColumn as error:
            await exceptions.DBUndefinedColumn.call(inter, error, value)
    
    @command_insert.sub_command(**commands.inserta.sub['ml']())
    @dis_commands.check(commands.inserta.sub['ml'].acs)
    async def sub_ml_data(self, inter: disnake.CommandInteraction, type: str, file: disnake.Attachment):
        raise Exception('IN DEVELOPING')
    
    @dis_commands.slash_command(**commands.update())
    @dis_commands.check(commands.update.acs)
    async def command_data_update(self, inter: disnake.CommandInteraction):
        pass
    
    @command_data_update.sub_command(**commands.update.sub['param']())
    @dis_commands.check(commands.update.sub['param'].acs)
    async def sub_param(self, inter: disnake.CommandInteraction, type: str, value: str, key: str=''):
        try:
            if key != '':
                key = f'WHERE {key}'
            request = f'UPDATE {type} SET {value} {key}'
            database(request)
            request = database(f'SELECT * FROM {type}')[:10]

            column = database(f'SELECT column_name FROM information_schema.columns WHERE table_schema = \'public\' AND table_name=\'{type}\'', 'all')
            column = list(map(lambda c: c[0], column))
            table = pd.DataFrame(request, columns=column)

            embed = disnake.Embed(
                title='Параметры обновлены',
                description=f'```{table}```',
                colour=controller.RANKS_DICT['Синий свисток'].colour
            )
            await inter.edit_original_message(embed=embed)
        
        except errors.SyntaxError as error:
            await exceptions.DBSyntax.call(inter, error)

    @command_data_update.sub_command_group(**commands.update.sub['ml']())
    @dis_commands.check(commands.update.sub['ml'].acs)
    async def group_ml(self, inter: disnake.CommandInteraction):
        pass

    @group_ml.sub_command(**commands.update.sub['ml'].sub['corpus']())
    @dis_commands.check(commands.update.sub['ml'].sub['corpus'].acs)
    async def re_mutabilis(self, inter: disnake.CommandInteraction, condition: str, limit: int=0):
        if limit == 0:
            limit = int(controller.ML.extract('corpus_limit'))

        if limit <= 100000 and limit >= 1000:
            controller.ML.update('corpus_condition', condition)
            controller.ML.update('corpus_limit', limit)

            embed = disnake.Embed(
                title='Изменения записаны',
                description=f'`corpus_condition={condition}`\n`corpus_limit={limit}`',
                colour=controller.RANKS_DICT['Лунный свисток'].colour
            )
            await inter.edit_original_message(embed=embed)
        
        else:
            error = Exception('Corpus limit')
            await exceptions.MLCorpusLimit.call(inter, error)
   
def setup(bot):
    bot.add_cog(Spotter(bot))
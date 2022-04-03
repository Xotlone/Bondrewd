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

    @dis_commands.slash_command(**commands.manual_request())
    @dis_commands.check(commands.manual_request.acs)
    async def command_manual_execute(self, inter: disnake.CommandInteraction, request: str):
        try:
            request = database(request, 'all')
            embed = disnake.Embed(
                title='Прямой SQL запрос',
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

    @dis_commands.slash_command(**commands.data())
    @dis_commands.check(commands.data.acs)
    async def command_data(self, inter: disnake.CommandInteraction):
        pass

    @command_data.sub_command_group(**commands.data.sub['extract']())
    @dis_commands.check(commands.data.sub['extract'].acs)
    async def group_extract(self, inter: disnake.CommandInteraction):
        pass

    @group_extract.sub_command(**commands.data.sub['extract'].sub['param']())
    @dis_commands.check(commands.data.sub['extract'].sub['param'].acs)
    async def sub_param(self, inter: disnake.CommandInteraction, table_name: str, key: str = ''):
        try:
            if key != '':
                key = f'WHERE {key}'

            param = database(f'SELECT * FROM {table_name} {key}', 'all')

            column = database(f'SELECT column_name FROM information_schema.columns WHERE table_schema = \'public\' '
                              f'AND table_name=\'{table_name}\'', 'all')
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

    @group_extract.sub_command(**commands.data.sub['extract'].sub['ml']())
    @dis_commands.check(commands.data.sub['extract'].sub['ml'].acs)
    async def sub_ml(self, inter: disnake.CommandInteraction, key: str):
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

    @command_data.sub_command_group(**commands.data.sub['insert']())
    @dis_commands.check(commands.data.sub['insert'].acs)
    async def group_insert(self, inter: disnake.CommandInteraction):
        pass

    @group_insert.sub_command(**commands.data.sub['insert'].sub['param']())
    @dis_commands.check(commands.data.sub['insert'].sub['param'].acs)
    async def sub_param(self, inter: disnake.CommandInteraction, table_name: str, value: str):
        try:
            database(f'INSERT INTO {table_name} VALUES ({value})')
            request = database(f'SELECT * FROM {table_name}', 'all')[-10:]

            column = database(
                f'SELECT column_name FROM information_schema.columns WHERE table_schema = \'public\' AND '
                f'table_name=\'{table_name}\'',
                'all')
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

    # TODO: Создание команды "data insert ml <type: str> <file: disnake.Attachment>"
    '''@group_insert.sub_command(**commands.data.sub['insert'].sub['ml']())
    @dis_commands.check(commands.data.sub['insert'].sub['ml'].acs)
    async def sub_ml_data(self, inter: disnake.CommandInteraction, type: str, file: disnake.Attachment):
        raise Exception('IN DEVELOPING')'''

    @command_data.sub_command_group(**commands.data.sub['update']())
    @dis_commands.check(commands.data.sub['update'].acs)
    async def group_update(self, inter: disnake.CommandInteraction):
        pass

    @group_update.sub_command(**commands.data.sub['update'].sub['param']())
    @dis_commands.check(commands.data.sub['update'].sub['param'].acs)
    async def sub_param(self, inter: disnake.CommandInteraction, table_name: str, value: str, key: str = ''):
        try:
            if key != '':
                key = f'WHERE {key}'
            request = f'UPDATE {table_name} SET {value} {key}'
            database(request)
            request = database(f'SELECT * FROM {table_name}')[:10]

            column = database(
                f'SELECT column_name FROM information_schema.columns WHERE table_schema = \'public\' AND '
                f'table_name=\'{table_name}\'',
                'all')
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

    @group_update.sub_command(**commands.data.sub['update'].sub['ml-corpus']())
    @dis_commands.check(commands.data.sub['update'].sub['ml-corpus'].acs)
    async def sub_ml_corpus(self, inter: disnake.CommandInteraction, condition: str, limit: int = 0):
        if limit == 0:
            limit = int(controller.ML.extract('corpus_limit'))

        if 100000 >= limit >= 1000:
            controller.ML.update('corpus_condition', condition)
            controller.ML.update('corpus_limit', str(limit))

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

import os

import pandas as pd
from psycopg2 import errors
import disnake
from disnake.ext import commands

from configuratione import mandatumes
import con_ter
from database import database
import errata_fieri
from apparatus_doctrina import verbum_processing
from utilitates import ProgressBar

class Mutatio(commands.Cog):
    def __init__(self, machina: commands.Bot):
        self.machina = machina
    
    @commands.slash_command(**mandatumes.manual_viscus())
    @commands.check(mandatumes.manual_viscus.acs)
    async def mandatum_manual_inquisitionis(self, inter: disnake.CommandInteraction, inquisitionis: str):
        try:
            respondere = database(inquisitionis, 'all')
            embed = disnake.Embed(
                title='Прямой запрос',
                description=f'```{respondere}```',
                colour=con_ter.OCCASIONES_DICT['Белый свисток'].colour
            )
            await inter.send(embed=embed)

        except errors.SyntaxError as error:
            await errata_fieri.DBSyntax.call(inter, error, inquisitionis)
        
        except errors.UndefinedColumn as error:
            await errata_fieri.DBUndefinedColumn.call(inter, error)

        except errors.ProgrammingError:
            embed = disnake.Embed(
                title='Прямой запрос',
                description=f'`True`',
                colour=con_ter.OCCASIONES_DICT['Белый свисток'].colour
            )
            await inter.send(embed=embed)

    @commands.slash_command(**mandatumes.extractionem())
    @commands.check(mandatumes.extractionem.acs)
    async def mandatum_extractionem(self, inter: disnake.CommandInteraction):
        pass

    @mandatum_extractionem.sub_command(**mandatumes.extractionem.sub['param']())
    @commands.check(mandatumes.extractionem.sub['param'].acs)
    async def sub_param(self, inter: disnake.CommandInteraction, genus: str, key: str=''):
        try:
            if key != '':
                key = f'WHERE {key}'
            
            param = database(f'SELECT * FROM {genus} {key}', 'all')

            columnae = database(f'SELECT column_name FROM information_schema.columns WHERE table_schema = \'public\' AND table_name=\'{genus}\'', 'all')
            columnae = list(map(lambda c: c[0], columnae))
            tabulas = pd.DataFrame(param, columns=columnae)

            embed = disnake.Embed(
                title='Ответ',
                description=f'```{tabulas}```',
                colour=con_ter.OCCASIONES_DICT['Красный свисток'].colour
            )
            await inter.send(embed=embed)

        except errors.SyntaxError as error:
            await errata_fieri.DBSyntax.call(inter, error)
        
        except errors.UndefinedColumn as error:
            await errata_fieri.DBUndefinedColumn.call(inter, error, key)

    @mandatum_extractionem.sub_command(**mandatumes.extractionem.sub['mutabilis']())
    @commands.check(mandatumes.extractionem.sub['mutabilis'].acs)
    async def sub_mutabilis(self, inter: disnake.CommandInteraction, key: str):
        if key == 'corpus':
            limit = int(con_ter.Doctrina.extractio('corpus_limit'))
            if os.path.exists('apparatus_doctrina/corpus.csv'):
                corpus = disnake.File('apparatus_doctrina/corpus.csv')
                pb = str(ProgressBar(limit, verbum_processing.corpus_len(), progress=True))
                embed = disnake.Embed(
                    title='Словарный корпус',
                    description=f'Заполненность {pb}',
                    colour=con_ter.OCCASIONES_DICT['Чёрный свисток'].colour
                )
                await inter.send(embed=embed, file=corpus)
            
            else:
                embed = disnake.Embed(
                    title='Корпус не обнаружен',
                    colour=con_ter.OCCASIONES_DICT['Чёрный свисток'].colour
                )
                await inter.send(embed=embed)
    
    @commands.slash_command(**mandatumes.inserta())
    @commands.check(mandatumes.inserta.acs)
    async def mandatum_inserta(self, inter: disnake.CommandInteraction):
        pass
    
    @mandatum_inserta.sub_command(**mandatumes.inserta.sub['param']())
    @commands.check(mandatumes.inserta.sub['param'].acs)
    async def sub_param(self, inter: disnake.CommandInteraction, genus: str, valorem: str):
        try:
            database(f'INSERT INTO {genus} VALUES ({valorem})')
            recens = database(f'SELECT * FROM {genus}', 'all')[-10:]

            columnae = database(f'SELECT column_name FROM information_schema.columns WHERE table_schema = \'public\' AND table_name=\'{genus}\'', 'all')
            columnae = list(map(lambda c: c[0], columnae))
            tabulas = pd.DataFrame(recens, columns=columnae)

            embed = disnake.Embed(
                title='Параметры успешно добавлены',
                description=f'```{tabulas}```',
                colour=con_ter.OCCASIONES_DICT['Синий свисток'].colour
            )
            await inter.send(embed=embed)
        
        except errors.SyntaxError as error:
            await errata_fieri.DBSyntax.call(inter, error)
        
        except errors.UndefinedColumn as error:
            await errata_fieri.DBUndefinedColumn.call(inter, error, valorem)
    
    @mandatum_inserta.sub_command(**mandatumes.inserta.sub['mutabilis']())
    @commands.check(mandatumes.inserta.sub['mutabilis'].acs)
    async def sub_mutabilis(self, inter: disnake.CommandInteraction, genus: str, file: disnake.Attachment):
        raise Exception('IN DEVELOPING')
    
    @commands.slash_command(**mandatumes.renovatio())
    @commands.check(mandatumes.renovatio.acs)
    async def mandatum_renovatio(self, inter: disnake.CommandInteraction):
        pass
    
    @mandatum_renovatio.sub_command(**mandatumes.renovatio.sub['param']())
    @commands.check(mandatumes.renovatio.sub['param'].acs)
    async def sub_param(self, inter: disnake.CommandInteraction, genus: str, valorem: str, key: str=''):
        try:
            if key != '':
                key = f'WHERE {key}'
            inquisitionis = f'UPDATE {genus} SET {valorem} {key}'
            database(inquisitionis)
            recens = database(f'SELECT * FROM {genus}')[:10]

            columnae = database(f'SELECT column_name FROM information_schema.columns WHERE table_schema = \'public\' AND table_name=\'{genus}\'', 'all')
            columnae = list(map(lambda c: c[0], columnae))
            tabulas = pd.DataFrame(recens, columns=columnae)

            embed = disnake.Embed(
                title='Параметры обновлены',
                description=f'```{tabulas}```',
                colour=con_ter.OCCASIONES_DICT['Синий свисток'].colour
            )
            await inter.send(embed=embed)
        
        except errors.SyntaxError as error:
            await errata_fieri.DBSyntax.call(inter, error)

    @mandatum_renovatio.sub_command_group(**mandatumes.renovatio.sub['doctrina']())
    @commands.check(mandatumes.renovatio.sub['doctrina'].acs)
    async def group_doctrina(self, inter: disnake.CommandInteraction):
        pass

    @group_doctrina.sub_command(**mandatumes.renovatio.sub['doctrina'].sub['corpus']())
    @commands.check(mandatumes.renovatio.sub['doctrina'].sub['corpus'].acs)
    async def re_mutabilis(self, inter: disnake.CommandInteraction, conditio: str, limit: int=0):
        if limit == 0:
            limit = int(con_ter.Doctrina.extractio('corpus_limit'))

        if limit <= 100000 and limit >= 1000:
            con_ter.Doctrina.renovatio('corpus_conditio', conditio)
            con_ter.Doctrina.renovatio('corpus_limit', limit)

            embed = disnake.Embed(
                title='Изменения записаны',
                description=f'`corpus_conditio={conditio}`\n`corpus_limit={limit}`',
                colour=con_ter.OCCASIONES_DICT['Лунный свисток'].colour
            )
            await inter.send(embed=embed)
        
        else:
            error = Exception('Corpus limit')
            await errata_fieri.DoctrinaCorpusLimit.call(inter, error)
   
def setup(machina):
    machina.add_cog(Mutatio(machina))
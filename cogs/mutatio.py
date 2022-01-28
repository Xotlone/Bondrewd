import pandas as pd
from psycopg2 import errors
import disnake
from disnake.ext import commands

from configuratione import config, mandatumes
import con_ter
from utilitates import log
from database import database
import errata_fieri

class Mutatio(commands.Cog):
    def __init__(self, machina: commands.Bot):
        self.machina = machina
    
    @commands.slash_command(**mandatumes.manual_viscus())
    @commands.check(mandatumes.manual_viscus.acs)
    async def manual_viscus(self, inter: disnake.CommandInteraction, inquisitionis: str):
        try:
            respondere = database(inquisitionis, 'all')
            embed = disnake.Embed(
                title='Прямой запрос',
                description=f'Ответ\n```{respondere}```',
                colour=config.WISTLES['Белый свисток']
            )
            await inter.send(embed=embed)

        except errors.SyntaxError as error:
            await errata_fieri.DBSyntax.call(inter, error, inquisitionis)
        
        except errors.ProgrammingError:
            embed = disnake.Embed(
                title='Прямой запрос',
                description=f'Ответ\n`True`',
                colour=config.WISTLES['Белый свисток']
            )
            await inter.send(embed=embed)

    @commands.slash_command(**mandatumes.extractionem())
    @commands.check(mandatumes.extractionem.acs)
    async def extractionem(self, inter: disnake.CommandInteraction):
        pass
    
    @extractionem.sub_command(**mandatumes.extractionem.sub['param']())
    @commands.check(mandatumes.extractionem.sub['param'].acs)
    async def ex_param(self, inter: disnake.CommandInteraction, genus: str, key: str=''):
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
                colour=config.WISTLES['Красный свисток']
            )
            await inter.send(embed=embed)

        except errors.SyntaxError as error:
            await errata_fieri.DBSyntax.call(inter, error)
    
    @extractionem.sub_command(**mandatumes.extractionem.sub['mutabilis']())
    @commands.check(mandatumes.extractionem.sub['mutabilis'].acs)
    async def ex_mutabilis(self, inter: disnake.CommandInteraction, genus: str, key: str=''):
        raise Exception('IN DEVELOPING')
    
    @commands.slash_command(**mandatumes.inserta())
    @commands.check(mandatumes.inserta.acs)
    async def inserta(self, inter: disnake.CommandInteraction):
        pass
    
    @inserta.sub_command(**mandatumes.inserta.sub['param']())
    @commands.check(mandatumes.inserta.sub['param'].acs)
    async def in_param(self, inter: disnake.CommandInteraction, genus: str, valorem: str):
        try:
            database(f'INSERT INTO {genus} VALUES ({valorem})')
            recens = database(f'SELECT * FROM {genus}', 'all')[-10:]

            columnae = database(f'SELECT column_name FROM information_schema.columns WHERE table_schema = \'public\' AND table_name=\'{genus}\'', 'all')
            columnae = list(map(lambda c: c[0], columnae))
            tabulas = pd.DataFrame(recens, columns=columnae)

            embed = disnake.Embed(
                title='Параметры успешно добавлены',
                description=f'```{tabulas}```',
                colour=config.WISTLES['Синий свисток']
            )
            await inter.send(embed=embed)
        
        except errors.SyntaxError as error:
            await errata_fieri.DBSyntax.call(inter, error)
        
        except errors.UndefinedColumn as error:
            await errata_fieri.DBUndefinedColumn.call(inter, error, valorem)
    
    @inserta.sub_command(**mandatumes.inserta.sub['mutabilis']())
    @commands.check(mandatumes.inserta.sub['mutabilis'].acs)
    async def in_mutabilis(self, inter: disnake.CommandInteraction, genus: str, file: disnake.Attachment):
        raise Exception('IN DEVELOPING')
    
    @commands.slash_command(**mandatumes.renovatio())
    @commands.check(mandatumes.renovatio.acs)
    async def renovatio(self, inter: disnake.CommandInteraction):
        pass
    
    @renovatio.sub_command(**mandatumes.renovatio.sub['param']())
    @commands.check(mandatumes.renovatio.sub['param'].acs)
    async def re_param(self, inter: disnake.CommandInteraction, genus: str, valorem: str, key: str=''):
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
                colour=config.WISTLES['Синий свисток']
            )
            await inter.send(embed=embed)
        
        except errors.SyntaxError as error:
            await errata_fieri.DBSyntax.call(inter, error)
    
    @renovatio.sub_command(**mandatumes.renovatio.sub['mutabilis']())
    @commands.check(mandatumes.renovatio.sub['mutabilis'].acs)
    async def re_mutabilis(self, inter: disnake.CommandInteraction, genus: str, key: str, file: disnake.Attachment):
        pass
   
def setup(machina):
    machina.add_cog(Mutatio(machina))
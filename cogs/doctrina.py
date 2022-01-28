import os

import disnake
from disnake.ext import commands

from configuratione import mandatumes, config
from database import database
import errata_fieri

class Doctrina(commands.Cog):
    def __init__(self, machina: commands.Bot):
        self.machina = machina
    
    @commands.slash_command(**mandatumes.doctrina_modos())
    @commands.check(mandatumes.doctrina_modos.acs)
    async def doctrina_modos(self, inter: disnake.CommandInteraction):
        pass
    
    @doctrina_modos.sub_command(**mandatumes.doctrina_modos.sub['corpus']())
    @commands.check(mandatumes.doctrina_modos.sub['corpus'].acs)
    async def corpus(self, inter: disnake.CommandInteraction, conditio: str, limit: str=10000):
        if limit < 100000:
            database(f'''
                UPDATE doctrina SET conditio = \'{conditio}\' WHERE nomen = \'coprus_conditio\';
                UPDATE doctrina SET conditio = \'{limit}\' WHERE nomen = \'corpus_limit\';
            ''')
            embed = disnake.Embed(
                title='Изменения записаны',
                description=f'`corpus_conditio={conditio}`\n`corpus_limit={limit}`',
                colour=config.WISTLES['Лунный свисток']
            )
            await inter.send(embed=embed)
        
        else:
            error = Exception('Corpus limit')
            await errata_fieri.DoctrinaCorpusLimit.call(inter, error)
   
    @commands.slash_command(**mandatumes.doctrina_praecepta())
    @commands.check(mandatumes.doctrina_praecepta.acs)
    async def doctrina_praecepta(self, inter: disnake.CommandInteraction):
        praecepta = {k: v for (k, v) in database('SELECT * FROM doctrina', 'all')}
        praecepta_list = '\n'.join([f'`{k}={v}`' for k, v in praecepta.items()])

        embed = disnake.Embed(
            title='Правила доктрины',
            description=praecepta_list,
            colour=config.WISTLES['Колокольчик']
        )
        await inter.send(embed=embed)
    
    @commands.slash_command(**mandatumes.doctrina_extractio())
    @commands.check(mandatumes.doctrina_extractio.acs)
    async def doctrina_extractio(self, inter: disnake.CommandInteraction):
        if os.path.exists('apparatus_doctrina/corpus.csv'):
            corpus = disnake.File('apparatus_doctrina/corpus.csv')
            embed = disnake.Embed(
                title='Выгруженный словарный корпус',
                colour=config.EXPLORATOR_COLOR
            )
            await inter.send(embed=embed, file=corpus)
        
        else:
            embed = disnake.Embed(
                title='Корпуса не обнаружено',
                colour=config.config.WISTLES['Чёрный свисток']
            )
            await inter.send(embed=embed)

def setup(machina):
   machina.add_cog(Doctrina(machina))
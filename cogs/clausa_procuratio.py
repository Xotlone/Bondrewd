import disnake
from disnake.ext import commands

from configuratione import mandatumes
import controlatoris_terminus
from utilitates import monospace, notitia_constructione
from configuratione import config
from database import database

class ClausaProcuratio(commands.Cog):
    def __init__(self, machina):
        self.machina = machina

    '''@commands.slash_command()
    async def extractum_aperta(self, ctx: commands.Context, **kwargs):
        mensa = kwargs['mensa']
        terminus = controlatoris_terminus.TERMINUS_COMITIA[mensa]

        try:
            parameter = kwargs['parametri']
            significatio = kwargs['significatio']
            data = database(f'SELECT * FROM {mensa} WHERE {parameter} = {significatio}', 'all')

        except KeyError:
            data = terminus.legere_all()
            
        embed = disnake.Embed(
            title=monospace(mensa),
            colour=config.COLOR
        )
        embed.set_author(name=monospace('Dominus Aurorae'), icon_url=self.machina.user.avatar_url)

        file = notitia_constructione(data, terminus)
        if file != False:
            embed.set_footer(text=monospace('Code: >PRESENT<'))
            await ctx.reply(embed=embed, file=notitia_constructione(data, terminus))

        else:
            embed.set_footer(text=monospace('Code: >INANIS<'))
            await ctx.reply(embed=embed)'''
    
def setup(machina):
    machina.add_cog(ClausaProcuratio(machina))
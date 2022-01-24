import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext

from configuratione import mandatumes
import controlatoris_terminus

class ClausaProcuratio(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_subcommand(**mandatumes.extractum_accessum())
    async def extractum_accessum(self, ctx: SlashContext, **kwargs):
        try:
            id = kwargs['id']
            accessum = controlatoris_terminus.AccessumCampester.lectio(id)
        except IndexError:
            accessum = controlatoris_terminus.AccessumCampester.legere_all()
        await ctx.send(f'```py\n{accessum}```')
    
def setup(client):
    client.add_cog(ClausaProcuratio(client))
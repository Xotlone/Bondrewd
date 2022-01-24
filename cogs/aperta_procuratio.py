import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext

from configuratione import mandatumes

class ApertaProcuratio(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @cog_ext.cog_slash(**mandatumes.help())
    async def help(self, ctx: SlashContext, **kwargs):
        await ctx.send('test')

def setup(client):
    client.add_cog(ApertaProcuratio(client))
import logging

import disnake
from disnake.ext import commands
from disnake.ext.commands import errors

from configuratione import mandatumes
import errata_fieri

class ErrorTracto(commands.Cog):
    def __init__(self, machina: commands.Bot):
        self.machina = machina

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.CommandInteraction, error: commands.CommandError):
        er = lambda e: isinstance(error, e)

        if er(errors.CheckFailure):
            try:
                mandatum_occasiones = mandatumes.Mandatum.invenire(inter.application_command.name).occasiones
            except AttributeError:
                mandatum_occasiones = mandatumes.SubMandatum.invenire(inter.application_command.name).occasiones

            await errata_fieri.Accessum.call(inter, error, mandatum_occasiones)
        
        else:
            logging.exception(error, exc_info=True)
   
def setup(machina):
    machina.add_cog(ErrorTracto(machina))
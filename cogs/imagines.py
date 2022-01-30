import disnake
from disnake.ext import commands

from anekos import SFWImageTags, NSFWImageTags, NekosLifeClient

from configuratione import mandatumes
import con_ter

class Imagines(commands.Cog):
    def __init__(self, machina: commands.Bot):
       self.machina = machina
       self.neko = NekosLifeClient()

    @commands.slash_command(**mandatumes.imagines())
    @commands.check(mandatumes.imagines.acs)
    async def mandatum_imagines(self, inter: disnake.CommandInteraction):
       pass
    
    @mandatum_imagines.sub_command(**mandatumes.imagines.sub['actio']())
    @commands.check(mandatumes.imagines.sub['actio'].acs)
    async def sub_actio(self, inter: disnake.CommandInteraction, genus: str, subjecto: disnake.Member=None):
        tag = eval(f'SFWImageTags.{genus.upper()}')
        genus = mandatumes.ACTIO_VERBS[genus]
        img = await self.neko.image(tag)
        title = f'{inter.author.name} {genus}'
        if subjecto != None and subjecto != inter.author:
            title += f' {subjecto.name}'
        else:
            title += '...'
        embed = disnake.Embed(
            title=title,
            colour=con_ter.OCCASIONES_DICT['Колокольчик'].colour
        )
        embed.set_image(img.url)
        await inter.send(embed=embed)
   
def setup(machina):
    machina.add_cog(Imagines(machina))
import typing

from discord import Permissions
from discord_slash import SlashCommandOptionType
from discord_slash.utils import manage_commands

import controlatoris_terminus

GENERALES_PERMISSIONES = Permissions.general()

class Mandatum:
    mandatum_album = []

    def __init__(self,
        nomen: str,
        descriptio: str,
        optiones: typing.List[typing.Dict]=None,
        permissiones: Permissions=GENERALES_PERMISSIONES,
        nsfw: bool=False
    ):
        self.nomen = nomen
        self.descriptio = descriptio
        self.optiones = optiones
        self.permissiones = permissiones
        self.nsfw = nsfw

        Mandatum.mandatum_album.append(self)
    
    def __call__(self):
        return {
            'name': self.nomen,
            'description': self.descriptio,
            'options': self.optiones
        }

    @staticmethod
    def numerus():
        return len(Mandatum.mandatum_dictionary)
    
    @staticmethod
    def quaerere(nomen: str):
        nomen = nomen.lower()
        for mandatum in Mandatum.mandatum_album:
            if nomen == mandatum.nomen:
                return mandatum
        
    @staticmethod
    def genus():
        Mandatum.mandatum_album = sorted(Mandatum.mandatum_album, key=lambda x: x.nomen)

class SubMandatum(Mandatum):
    def __init__(self,
        base: str,
        nomen: str,
        descriptio: str,
        optiones: typing.List[typing.Dict]=None,
        permissiones: Permissions=GENERALES_PERMISSIONES,
        nsfw: bool=False
    ):
        super().__init__(nomen, descriptio, optiones, permissiones, nsfw)
        self.base = base
        self.coetus = base + 'coetus'
    
    def __call__(self):
        return {
            'base': self.base,
            'subcommand_group': self.coetus,
            'name': self.nomen,
            'description': self.descriptio,
            'options': self.optiones
        }

help = Mandatum(
    'help',
    'Технические возможности',
    [
        manage_commands.create_option(
            'commmand',
            'Команда, подробности которой вам требуются',
            SlashCommandOptionType.STRING,
            False
        )
    ]
)

extractum_accessum = SubMandatum(
    'extractum',
    'accessum',
    'Extractum accessum campesters',
    [
        manage_commands.create_option(
            'id',
            'Identifier',
            SlashCommandOptionType.INTEGER,
            False
        )
    ]
)

extractum_variabilis = SubMandatum(
    'extractum',
    'variabilis',
    'Extractum variabilis',
    [
        manage_commands.create_option(
            'nomen',
            'Nomen',
            SlashCommandOptionType.STRING,
            False
        )
    ]
)

extractum_textuum = SubMandatum(
    'extractum',
    'textuum',
    'Extractum textuum',
    [
        manage_commands.create_option(
            'nomen',
            'Nomen',
            SlashCommandOptionType.STRING,
            False
        )
    ]
)
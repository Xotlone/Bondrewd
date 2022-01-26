import typing

from disnake import Option, OptionType, Permissions
from anekos import SFWImageTags, NSFWImageTags

import controlatoris_terminus

GENERALES_PERMISSIONES = Permissions.general()

class SubMandatum:
    numerus = 0

    def __init__(
        self,
        nomen: str,
        descriptio: str,
        optiones: typing.List[Option]=[]
    ):
        self.nomen = nomen
        self.descriptio = descriptio
        self.optiones = optiones
        self.id = SubMandatum.numerus
        
        SubMandatum.numerus += 1
    
    def __call__(self):
        return {
            'name': self.nomen,
            'description': self.descriptio,
            'options': self.optiones
        }

class Mandatum:
    numerus = 0
    omnia = []

    def __init__(
        self,
        nomen: str,
        descriptio: str,
        optiones: typing.List[Option]=[],
        sub: typing.Tuple[SubMandatum]=()
    ):
        self.nomen = nomen
        self.descriptio = descriptio
        self.optiones = optiones
        self.sub = {n.nomen: n for n in sub}
        self.id = Mandatum.numerus

        Mandatum.numerus += 1
        Mandatum.omnia.append(self)
    
    def __call__(self):
        return {
            'name': self.nomen,
            'description': self.descriptio,
            'options': self.optiones
        }
    
    @staticmethod
    def sort(key: str):
        if key == 'nomen':
            return sorted(Mandatum.omnia, key=lambda m: m.nomen)
        elif key == 'id':
            return sorted(Mandatum.omnia, key=lambda m: m.id)
        else:
            raise KeyError(f'Key "{key}" does not exist')
    
    @staticmethod
    def invenire(nomen: str):
        for mandatum in Mandatum.omnia:
            if nomen.lower() == mandatum.nomen:
                return mandatum

informationes = Mandatum(
    'informationes',
    'Информация',
    sub=(
        SubMandatum('mandatumes', 'Список мандатов'),
        SubMandatum('mandatum', 'Описание определённого мандата', [
            Option(
                'nomen',
                'Название мандата, конкретное описание которого запрашивается',
                OptionType.string,
                True
            )
        ])
    )
)

ping = Mandatum(
    'ping',
    'Задержка отклика'
)

actio = Mandatum(
    'actio',
    'Действие',
    [
        Option(
            'genus',
            'Выберите действие',
            OptionType.string,
            True,
            SFWImageTags.to_list()
        ),
        Option(
            'subjecto',
            'Субъект, которому направлено действие',
            OptionType.user,
        )
    ]
)
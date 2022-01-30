import typing

from disnake.ext import commands
from disnake import Option, OptionType, Permissions
from anekos import SFWImageTags, NSFWImageTags

from configuratione import config
import con_ter
from database import database

GENERALES_PERMISSIONES = Permissions.general()

class OccasionesCheck:
    def acs(self, ctx: commands.Context):
        subjecto_occasione_id = database(f'SELECT occasione_id FROM users WHERE id = {ctx.author.id}', 'one')[0]

        if subjecto_occasione_id == None:
            if ctx.author.id == config.owner_id:
                subjecto = con_ter.User(ctx.author.id, 5)
            
            else:
                subjecto = con_ter.User(ctx.author.id, 0)
                
            subjecto.ingressum()
        
        return con_ter.OCCASIONES_DICT[self.occasiones].prioritas <= subjecto_occasione_id

class SubMandatum(OccasionesCheck):
    numerus = 0
    omnia = []

    def __init__(
        self,
        nomen: str,
        descriptio: str,
        optiones: typing.List[Option]=[],
        occasiones: str='hereditas'
    ):
        self.nomen = nomen
        self.descriptio = descriptio
        self.optiones = optiones
        self.occasiones = occasiones
        self.id = SubMandatum.numerus
        
        SubMandatum.numerus += 1
        SubMandatum.omnia.append(self)
    
    def __call__(self):
        return {
            'name': self.nomen,
            'description': self.descriptio,
            'options': self.optiones
        }

    @staticmethod
    def invenire(nomen: str):
        for sub_mandatum in SubMandatum.omnia:
            if nomen.lower() == sub_mandatum.nomen:
                return sub_mandatum

class SubMandatumGroup(OccasionesCheck):
    numerus = 0
    omnia = []

    def __init__(
        self,
        nomen,
        sub: typing.Tuple[SubMandatum],
        occasiones: str='hereditas'
    ):
        self.nomen = nomen
        self.sub = {n.nomen: n for n in sub}
        self.occasiones = occasiones
        self.id = SubMandatumGroup.numerus

        for _sub in sub:
            if _sub.occasiones == 'hereditas':
                _sub.occasiones = occasiones
        
        SubMandatumGroup.numerus += 1
        SubMandatumGroup.omnia.append(self)
    
    def __call__(self):
        return {'name': self.nomen}
    
    @staticmethod
    def sort(key: str):
        if key == 'nomen':
            return sorted(SubMandatumGroup.omnia, key=lambda m: m.nomen)

        elif key == 'id':
            return sorted(SubMandatumGroup.omnia, key=lambda m: m.id)

        else:
            raise KeyError(f'Key "{key}" does not exist')

    @staticmethod
    def sub_sort(key: str):
        if key == 'nomen':
            omnia = SubMandatumGroup.sort(key)
            out = []
            for group in omnia:
                subs = sorted(group.sub.items(), key=lambda s: s[1].nomen)
                group.sub = {k: v for k, v in subs}
                out.append(group)
            return out
        
        elif key == 'id':
            omnia = SubMandatumGroup.sort(key)
            out = []
            for group in omnia:
                subs = sorted(group.sub.items(), key=lambda s: s[1].id)
                group.sub = {k: v for k, v in subs}
                out.append(group)
            return out
        
        else:
            raise KeyError(f'Key "{key}" does not exist')

class Mandatum(OccasionesCheck):
    numerus = 0
    omnia = []

    def __init__(
        self,
        nomen: str,
        descriptio: str,
        optiones: typing.List[Option]=[],
        sub: typing.Tuple[typing.Union[SubMandatum, SubMandatumGroup]]=(),
        occasiones: str='Колокольчик'
    ):
        self.nomen = nomen
        self.descriptio = descriptio
        self.optiones = optiones
        self.sub = {n.nomen: n for n in sub}
        self.occasiones = occasiones
        self.id = Mandatum.numerus

        if sub != ():
            for _sub in sub:
                if _sub.occasiones == 'hereditas':
                    _sub.occasiones = occasiones

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
    def sub_sort(key: str):
        if key == 'nomen':
            omnia = Mandatum.sort(key)
            out = []
            for mandatum in omnia:
                subs = sorted(mandatum.sub.items(), key=lambda s: s[1].nomen)
                mandatum.sub = {k: v for k, v in subs}
                out.append(mandatum)
            return out
        
        elif key == 'id':
            omnia = Mandatum.sort(key)
            out = []
            for mandatum in omnia:
                subs = sorted(mandatum.sub.items(), key=lambda s: s[1].id)
                mandatum.sub = {k: v for k, v in subs}
                out.append(mandatum)
            return out
        
        else:
            raise KeyError(f'Key "{key}" does not exist')
    
    @staticmethod
    def invenire(nomen: str):
        for mandatum in Mandatum.omnia:
            if nomen.lower() == mandatum.nomen:
                return mandatum

doctrina_praecepta = Mandatum(
    'doctrina_praecepta',
    'Все правила доктрины'
)

manual_viscus = Mandatum(
    'manual',
    'Прямой запрос',
    [
        Option(
            'inquisitionis',
            'Запрос',
            OptionType.string,
            True
        )
    ],
    occasiones='Белый свисток'
)

extractionem = Mandatum(
    'extractionem',
    'Извлечение параметров/обучаемых параметров',
    sub=(
        SubMandatum('param', 'Извлечение параметров',
            [
                Option(
                    'genus',
                    'Тип',
                    OptionType.string,
                    True,
                    {
                        'Пользовательские': 'users',
                        'Переменные': 'variabilium'
                    }
                ),
                Option(
                    'key',
                    'Ключ',
                    OptionType.string,
                    False
                )
            ]
        ),
        SubMandatum('mutabilis', 'Извлечение обучаемых параметров',
            [
                Option(
                    'key',
                    'Ключ',
                    OptionType.string,
                    True,
                    {
                        'Словарный корпус': 'corpus'
                    }
                )
            ],
            'Чёрный свисток'
        )
    ),
    occasiones='Красный свисток'
)

inserta = Mandatum(
    'inserta',
    'Запись новых параметров/обучаемых параметров',
    sub=(
        SubMandatum('param', 'Запись параметра',
            [
                Option(
                    'genus',
                    'Тип',
                    OptionType.string,
                    True,
                    {
                        'Переменные': 'variabilium'
                    }
                ),
                Option(
                    'valorem',
                    'Значение (<val>)',
                    OptionType.string,
                    True
                )
            ]
        ),
        SubMandatum('mutabilis', 'Запись обучаемых параметров',
            [
                Option(
                    'genus',
                    'Тип',
                    OptionType.string,
                    True
                ),
                Option(
                    'file',
                    'Файл с параметрами',
                    OptionType.attachment,
                    True
                )
            ],
            'Лунный свисток'
        )
    ),
    occasiones='Синий свисток'
)

renovatio = Mandatum(
    'renovatio',
    'Обновление существующих параметров/обучаемых параметров',
    sub=(
        SubMandatum('param', 'Обновление параметра',
            [
                Option(
                    'genus',
                    'Тип',
                    OptionType.string,
                    True,
                    {
                        'Переменные': 'variabilium'
                    }
                ),
                Option(
                    'valorem',
                    'Значение (<name>=<val>)',
                    OptionType.string,
                    True
                ),
                Option(
                    'key',
                    'Ключ',
                    OptionType.string,
                    False
                )
            ]
        ),
        SubMandatumGroup('doctrina', 
            [
                SubMandatum('corpus', 'Параметры заполнения корпуса',
                    [
                        Option(
                            'conditio',
                            'Включение заполнения корпуса',
                            OptionType.string,
                            True,
                            {
                                'Y': '1',
                                'N': '0'
                            }
                        ),
                        Option(
                            'limit',
                            'Лимит корпуса',
                            OptionType.integer,
                            False
                        )
                    ]
                ),
            ],
            'Лунный свисток'
        )
    ),
    occasiones='Синий свисток'
)

informationes = Mandatum(
    'informationes',
    'Разного рода информация',
    sub=(
        SubMandatum('mandatumes', 'Список мандатов'),
        SubMandatum('mandatum', 'Описание определённого мандата',
            [
                Option(
                    'nomen',
                    'Название мандата, конкретное описание которого запрашивается',
                    OptionType.string,
                    True
                )
            ]
        ),
        SubMandatum('avatar', 'Аватар субъекта',
            [
                Option(
                    'subjecto',
                    'Субъект, аватар которого требуется',
                    OptionType.user,
                    False
                )
            ]
        ),
        SubMandatum('ping', 'Задержка отклика'),
        SubMandatum('sticker', 'Информация о стикере',
            [
                Option(
                    'id',
                    'id стикера',
                    OptionType.integer,
                    True
                )
            ]
        ),
        SubMandatum('doctrina', 'Информация о состоянии обучения'),
        SubMandatum('member', 'Информация о пользователе',
            [
                Option(
                    'subjecto',
                    'Субъект',
                    OptionType.user,
                    False
                )
            ]
        ),
    )
)

ACTIO_DISCTIONARY = {
    'Щекотать': 'tickle',
    'Тыкать': 'poke',
    'Целовать': 'kiss',
    'Пощёчина': 'slap',
    'Обнимать': 'cuddle',
    'Погладить': 'pat',
    'Выглядеть самодовольно': 'smug',
    'Кормить': 'feed'
}
ACTIO_VERBS = {
    'tickle': 'щекочет',
    'poke': 'тыкает',
    'kiss': 'целует',
    'slap': 'даёт пощёчину',
    'cuddle': 'обнимает',
    'pat': 'гладит',
    'smug': 'выглядит самодовольно перед',
    'feed': 'кормит'
}
ACTIO_DISCTIONARY = {k: v for k, v in sorted(ACTIO_DISCTIONARY.items(), key=lambda a: a[1])}
imagines = Mandatum(
    'imagines',
    'Изображения',
    sub=(
        SubMandatum(
            'actio',
            'Действие',
            [
                Option(
                    'genus',
                    'Выберите действие',
                    OptionType.string,
                    True,
                    ACTIO_DISCTIONARY
                ),
                Option(
                    'subjecto',
                    'Субъект, которому направлено действие',
                    OptionType.user,
                )
            ]
        ),
    )
)
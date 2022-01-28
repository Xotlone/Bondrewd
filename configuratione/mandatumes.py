import typing

import disnake
from disnake.ext import commands
from disnake import Option, OptionType, Permissions
from anekos import SFWImageTags, NSFWImageTags

import con_ter
from database import database

GENERALES_PERMISSIONES = Permissions.general()

class SubMandatum:
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
    
    def acs(self, ctx: commands.Context):
        subjecto_accessum_id = database(f'SELECT accessum_id FROM users WHERE id = {ctx.author.id}', 'one')[0]

        if subjecto_accessum_id == None:
            subjecto = con_ter.User(ctx.author.id, 0)
            subjecto.ingressum()

        subjecto_accessum = con_ter.AccessumCampester.get(f'id = {subjecto_accessum_id}')
        
        return self.occasiones in subjecto_accessum.occasiones or 'Белый свисток' in subjecto_accessum.occasiones.split(';')

    @staticmethod
    def invenire(nomen: str):
        for sub_mandatum in SubMandatum.omnia:
            if nomen.lower() == sub_mandatum.nomen:
                return sub_mandatum

class Mandatum:
    numerus = 0
    omnia = []

    def __init__(
        self,
        nomen: str,
        descriptio: str,
        optiones: typing.List[Option]=[],
        sub: typing.Tuple[SubMandatum]=(),
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
                    _sub.occasiones = self.occasiones

        Mandatum.numerus += 1
        Mandatum.omnia.append(self)
    
    def __call__(self):
        return {
            'name': self.nomen,
            'description': self.descriptio,
            'options': self.optiones
        }
    
    def acs(self, ctx: commands.Context):
        subjecto_accessum_id = database(f'SELECT accessum_id FROM users WHERE id = {ctx.author.id}', 'one')[0]

        if subjecto_accessum_id == None:
            subjecto = con_ter.User(ctx.author.id, 0)
            subjecto.ingressum()

        subjecto_accessum = con_ter.AccessumCampester.get(f'id = {subjecto_accessum_id}')

        return self.occasiones in subjecto_accessum.occasiones or 'Белый свисток' in subjecto_accessum.occasiones.split(';')
    
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

# Лунный свисток access

doctrina_modos = Mandatum(
    'doctrina_modos',
    'Обновление правил обучающей доктрины',
    sub=(
        SubMandatum('corpus', 'Заполненние корпуса',
        [
            Option(
                'conditio',
                'Включение заполнения корпуса',
                OptionType.string,
                True,
                {
                    'Y': 'True',
                    'N': 'False'
                }
            ),
            Option(
                'limit',
                'Лимит корпуса',
                OptionType.integer,
                False
            )
        ]),
    ),
    occasiones='Лунный свисток'
)

doctrina_praecepta = Mandatum(
    'doctrina_praecepta',
    'Все правила доктрины'
)

doctrina_extractio = Mandatum(
    'doctrina_extractio',
    'Извлечение различных обучаемых параметров',
    sub=(
        SubMandatum('corpus', 'Извлечение корпуса'),
    ),
    occasiones='Чёрный свисток'
)

# Summa access

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
                    'Уровни доступа': 'accessum_campesters',
                    'Переменные': 'variabilium',
                    'Текстовые': 'textuum'
                }
            ),
            Option(
                'key',
                'Ключ',
                OptionType.string,
                False
            )
        ]),
        SubMandatum('mutabilis', 'Извлечение обучаемых параметров',
        [
            Option(
                'genus',
                'Тип',
                OptionType.string,
                True
            ),
            Option(
                'key',
                'Ключ (не пользовательский тип)',
                OptionType.string,
                False
            )
        ], 'Лунный свисток')
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
                    'Уровни доступа': 'accessum_campesters',
                    'Переменные': 'variabilium',
                    'Текстовые': 'textuum'
                }
            ),
            Option(
                'valorem',
                'Значение (<val>)',
                OptionType.string,
                True
            )
        ]),
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
        ], 'Лунный свисток')
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
                    'Уровни доступа': 'accessum_campesters',
                    'Переменные': 'variabilium',
                    'Текстовые': 'textuum'
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
        ]),
        SubMandatum('mutabilis', 'Обновление обучаемых параметров',
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
            ),
            Option(
                'key',
                'Ключ',
                OptionType.string,
                False
            )
        ], 'Лунный свисток')
    ),
    occasiones='Синий свисток'
)

# Inferior Access

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
        ]),
        SubMandatum('avatar', 'Аватар субъекта',
        [
            Option(
                'subjecto',
                'Субъект, аватар которого требуется',
                OptionType.user,
                False
            )
        ]),
        SubMandatum('ping', 'Задержка отклика'),
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
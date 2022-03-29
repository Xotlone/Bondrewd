import typing

from disnake.ext import commands
from disnake import Option, OptionType, Permissions
from anekos import SFWImageTags, NSFWImageTags

from constants import config
import controller
from database import database

GENERALES_PERMISSIONES = Permissions.general()

class RanksCheck:
    def acs(self, ctx: commands.Context):
        user_rank_id = database(f'SELECT rank_id FROM users WHERE id = {ctx.author.id}', 'one')[0]

        if user_rank_id == None:
            if ctx.author.id == config.owner_id:
                user = controller.User(ctx.author.id, 5)
            
            else:
                user = controller.User(ctx.author.id, 0)
                
            user.insert()
        
        return controller.RANKS_DICT[self.access].priority <= user_rank_id

class SubCommand(RanksCheck):
    count = 0
    _instances = []

    def __init__(
        self,
        name: str,
        description: str,
        options: typing.List[Option]=[],
        access: str='hereditas'
    ):
        self.name = name
        self.description = description
        self.options = options
        self.access = access
        self.id = SubCommand.count
        
        SubCommand.count += 1
        SubCommand._instances.append(self)
    
    def __call__(self):
        return {
            'name': self.name,
            'description': self.description,
            'options': self.options
        }

    @staticmethod
    def search(name: str):
        for sub_command in SubCommand._instances:
            if name.lower() == sub_command.name:
                return sub_command

class SubCommandGroup(RanksCheck):
    count = 0
    _instances = []

    def __init__(
        self,
        name,
        sub: typing.Tuple[SubCommand],
        access: str='hereditas'
    ):
        self.name = name
        self.sub = {n.name: n for n in sub}
        self.access = access
        self.id = SubCommandGroup.count
        
        SubCommandGroup.count += 1
        SubCommandGroup._instances.append(self)
    
    def __call__(self):
        return {'name': self.name}
    
    @staticmethod
    def sort(key: str):
        if key == 'name':
            return sorted(SubCommandGroup._instances, key=lambda m: m.name)

        elif key == 'id':
            return sorted(SubCommandGroup._instances, key=lambda m: m.id)

        else:
            raise KeyError(f'Key "{key}" does not exist')

    @staticmethod
    def sub_sort(key: str):
        if key == 'name':
            _instances = SubCommandGroup.sort(key)
            out = []
            for group in _instances:
                subs = sorted(group.sub.items(), key=lambda s: s[1].name)
                group.sub = {k: v for k, v in subs}
                out.append(group)
            return out
        
        elif key == 'id':
            _instances = SubCommandGroup.sort(key)
            out = []
            for group in _instances:
                subs = sorted(group.sub.items(), key=lambda s: s[1].id)
                group.sub = {k: v for k, v in subs}
                out.append(group)
            return out
        
        else:
            raise KeyError(f'Key "{key}" does not exist')

class Command(RanksCheck):
    count = 0
    _instances = []

    def __init__(
        self,
        name: str,
        description: str,
        options: typing.List[Option]=[],
        sub: typing.Tuple[typing.Union[SubCommand, SubCommandGroup]]=(),
        access: str='Колокольчик'
    ):
        self.name = name
        self.description = description
        self.options = options
        self.sub = {n.name: n for n in sub}
        self.access = access
        self.id = Command.count

        if sub != {}:
            for _sub in sub:
                if _sub.access == 'hereditas':
                    _sub.access = access
                
                if isinstance(_sub, SubCommandGroup):
                    for _sub2 in _sub.sub.values():
                        if _sub2.access == 'hereditas':
                            _sub2.access = _sub.access

        Command.count += 1
        Command._instances.append(self)
    
    def __call__(self):
        return {
            'name': self.name,
            'description': self.description,
            'options': self.options
        }
    
    @staticmethod
    def sort(key: str):
        if key == 'name':
            return sorted(Command._instances, key=lambda m: m.name)

        elif key == 'id':
            return sorted(Command._instances, key=lambda m: m.id)

        else:
            raise KeyError(f'Key "{key}" does not exist')
    
    @staticmethod
    def sub_sort(key: str):
        if key == 'name':
            _instances = Command.sort(key)
            out = []
            for command in _instances:
                subs = sorted(command.sub.items(), key=lambda s: s[1].name)
                command.sub = {k: v for k, v in subs}
                out.append(command)
            return out
        
        elif key == 'id':
            _instances = Command.sort(key)
            out = []
            for command in _instances:
                subs = sorted(command.sub.items(), key=lambda s: s[1].id)
                command.sub = {k: v for k, v in subs}
                out.append(command)
            return out
        
        else:
            raise KeyError(f'Key "{key}" does not exist')
    
    @staticmethod
    def search(name: str):
        for command in Command._instances:
            if name.lower() == command.name:
                return command

ml = Command(
    'ml',
    'Все функции машинного обучения',
    sub=(
        SubCommandGroup(
            'tokenizator',
            (
                SubCommand('tokenize', 'Токенизировать текст (сырой текст принимается)',
                    [
                        Option(
                            'text',
                            'Текст для токенизации',
                            OptionType.string,
                            True
                        )
                    ]
                ),
                SubCommand('pre', 'Преподготовка текста к токенизации',
                    [
                        Option(
                            'text',
                            'Текст для преподготовки',
                            OptionType.string,
                            True
                        )
                    ]
                ),
            )
        ),
        SubCommand(
            'skip-gramm',
            'Генерация скип-граммы из текста',
            [
                Option(
                    'text',
                    'Текст, который станет скип-граммой',
                    OptionType.string,
                    True
                ),
                Option(
                    'n_gramm',
                    'n - радиус захватываемого текста',
                    OptionType.integer,
                    False,
                    [3, 5, 7, 9]
                ),
                Option(
                    'padding',
                    'Игнорирует-ли движущееся окно рамки текста',
                    OptionType.string,
                    False,
                    ['ignore', 'correspond']
                )
            ]
        )
    ),
    access='Чёрный свисток'
)

manual_request = Command(
    'manual',
    'Прямой запрос',
    [
        Option(
            'request',
            'Запрос',
            OptionType.string,
            True
        )
    ],
    access='Белый свисток'
)

extract = Command(
    'data_extract',
    'Извлечение параметров/обучаемых параметров',
    sub=(
        SubCommand('param', 'Извлечение параметров',
            [
                Option(
                    'type',
                    'Тип',
                    OptionType.string,
                    True,
                    {
                        'Пользовательские': 'users',
                        'Переменные': 'variables'
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
        SubCommand('ml', 'Извлечение обучаемых параметров',
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
    access='Красный свисток'
)

insert = Command(
    'data_insert',
    'Запись новых параметров/обучаемых параметров',
    sub=(
        SubCommand('param', 'Запись параметра',
            [
                Option(
                    'type',
                    'Тип',
                    OptionType.string,
                    True,
                    {
                        'Переменные': 'variables'
                    }
                ),
                Option(
                    'value',
                    'Значение (<val>)',
                    OptionType.string,
                    True
                )
            ]
        ),
        SubCommand('ml', 'Запись обучаемых параметров',
            [
                Option(
                    'type',
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
    access='Синий свисток'
)

update = Command(
    'data_update',
    'Обновление существующих параметров/обучаемых параметров',
    sub=(
        SubCommand('param', 'Обновление параметра',
            [
                Option(
                    'type',
                    'Тип',
                    OptionType.string,
                    True,
                    {
                        'Переменные': 'variables'
                    }
                ),
                Option(
                    'value',
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
        SubCommandGroup('ml', 
            [
                SubCommand('corpus', 'Параметры заполнения корпуса',
                    [
                        Option(
                            'condition',
                            'Включение заполнения корпуса',
                            OptionType.string,
                            True,
                            {
                                'Да': '1',
                                'Нет': '0'
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
    access='Синий свисток'
)

info = Command(
    'information',
    'Разного рода информация',
    sub=(
        SubCommand('commands', 'Список мандатов'),
        SubCommand('command', 'Описание определённого мандата',
            [
                Option(
                    'name',
                    'Название мандата, конкретное описание которого запрашивается',
                    OptionType.string,
                    True
                )
            ]
        ),
        SubCommand('avatar', 'Аватар субъекта',
            [
                Option(
                    'user',
                    'Пользователь, аватар которого требуется',
                    OptionType.user,
                    False
                )
            ]
        ),
        SubCommand('ping', 'Задержка отклика'),
        SubCommand('sticker', 'Информация о стикере',
            [
                Option(
                    'id',
                    'id стикера',
                    OptionType.integer,
                    True
                )
            ]
        ),
        SubCommand('ml', 'Информация о состоянии обучения'),
        SubCommand('member', 'Информация о пользователе',
            [
                Option(
                    'user',
                    'Пользователь',
                    OptionType.user,
                    False
                )
            ]
        ),
        SubCommand('rating', 'Рейтинг вклада в знания естественного языка',
            [
                Option(
                    'ml',
                    'Тип доктрины, рейтинг вклада которой вами требуется',
                    OptionType.string,
                    True,
                    {
                        'Словарный корпус': 'corpus'
                    }
                )
            ]
        ),
    )
)

ACTION_COMMANDS = {
    'Щекотать': 'tickle',
    'Тыкать': 'poke',
    'Целовать': 'kiss',
    'Пощёчина': 'slap',
    'Обнимать': 'cuddle',
    'Погладить': 'pat',
    'Выглядеть самодовольно': 'smug',
    'Кормить': 'feed'
}
ACTION_WORDS = {
    'tickle': 'щекочет',
    'poke': 'тыкает',
    'kiss': 'целует',
    'slap': 'даёт пощёчину',
    'cuddle': 'обнимает',
    'pat': 'гладит',
    'smug': 'выглядит самодовольно перед',
    'feed': 'кормит'
}
ACTION_COMMANDS = {k: v for k, v in sorted(ACTION_COMMANDS.items(), key=lambda a: a[1])}
images = Command(
    'images',
    'Изображения',
    sub=(
        SubCommand(
            'action',
            'Действие',
            [
                Option(
                    'type',
                    'Выберите действие',
                    OptionType.string,
                    True,
                    ACTION_COMMANDS
                ),
                Option(
                    'user',
                    'Пользователь, которому направлено действие',
                    OptionType.user,
                )
            ]
        ),
    )
)

funcs = Command(
    'funcs',
    'Функции',
    sub=(
        SubCommand(
            'calc',
            'Калькулятор',
            [
                Option(
                    'primer',
                    'Математический пример',
                    OptionType.string,
                    True
                )
            ]
        ),
        SubCommand(
            'learn-japanese',
            'Учить японский',
            [
                Option(
                    'alphabet',
                    'Азбука (для начинающий хирагана)',
                    OptionType.string,
                    True,
                    {
                        'Хирагана': 'hira'
                    }
                ),
                Option(
                    'only_complex',
                    'Только сложные иероглифы с вашего списка',
                    OptionType.boolean,
                    False,
                    {
                        'Да': True,
                        'Нет': False
                    }
                )
            ]
        )
    )
)
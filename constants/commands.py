from disnake import Option, OptionType, Permissions, ChannelType

from commands_lib import *

info = Command(
    name='info',
    description='Информация',
    sub=[
        SubCommand(
            name='commands',
            description='Список команд'
        ),
        SubCommand(
            name='member',
            description='Информация о участнике',
            options=[
                Option(
                    name='member',
                    description='Участник',
                    type=OptionType.user,
                    required=False
                )
            ]
        ),
        SubCommand(
            name='server',
            description='Информация о этом сервере'
        ),
        SubCommand(
            name='rating',
            description='Рейтинг участников'
        )
    ]
)

useful = Command(
    name='useful',
    description='Утилитарные команды',
    sub=[
        SubCommand(
            name='calculator',
            description='Калькулятор',
            options=[
                Option(
                    name='condition',
                    description='Выражение',
                    type=OptionType.string,
                    required=True
                )
            ]
        ),
        SubCommand(
            name='microcontroller_test',
            description='Тестирование функций микроконтроллера',
            options=[
                Option(
                    name='angle',
                    description='Угол сервопривода [0-180]',
                    type=OptionType.integer,
                    required=True,
                    min_value=0,
                    max_value=180
                )
            ]
        )
    ]
)

parsers = Command(
    name='parsers',
    description='Различные парсеры',
    sub=[
        SubCommandGroup(
            name='anime',
            sub=[
                SubCommand(
                    name='ero',
                    description='Тег, посвящённый эротике в аниме',
                    options=[
                        Option(
                            name='count',
                            description='Кол-во картинок',
                            type=OptionType.integer,
                            required=False,
                            min_value=1,
                            max_value=10
                        )
                    ]
                ),
                SubCommand(
                    name='ero-gif',
                    description='Тег, посвящённый эротике в аниме (в gif)',
                    options=[
                        Option(
                            name='count',
                            description='Кол-во gif',
                            type=OptionType.integer,
                            required=False,
                            min_value=1,
                            max_value=10
                        )
                    ]
                ),
                SubCommand(
                    name='monster-girl',
                    description='Тег, посвящённый девушкам с ярко выраженными "чудовищными", мифологическими чертами',
                    options=[
                        Option(
                            name='count',
                            description='Кол-во картинок',
                            type=OptionType.integer,
                            required=False,
                            min_value=1,
                            max_value=10
                        )
                    ]
                ),
            ]
        ),
    ]
)
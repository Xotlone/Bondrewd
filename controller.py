import time

from disnake.ext import commands

from database import database
from utilities import log


class Wistle:
    count = 0
    _instances = []

    def __init__(self, name: str, colour: int):
        self.name = name
        self.colour = colour
        self.priority = Wistle.count

        Wistle.count += 1
        Wistle._instances.append(self)

    def __call__(self):
        return self.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def __ne__(self, other):
        return self.priority != other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    @staticmethod
    def get(priority: int):
        for wistle in Wistle._instances:
            if priority == wistle.priority:
                return wistle

        return False


class User:
    count = 0

    def __init__(self, id: int, rank_id: int):
        self.id = id
        self.rank_id = rank_id
        self.access = RANKS_DICT.values()[rank_id]

        User.count += 1

    def insert(self):
        log(f'  Пользователь с id {self.id} добавлен в таблицу', 'Database')
        database(f'INSERT INTO users (id) VALUES ({self.id});')
        return True

    def remove(self):
        database(f'DELETE FROM users WHERE id = {self.id};')
        return True


class ML:
    @staticmethod
    def extract(name: str):
        return database(f'SELECT condition FROM ml WHERE name = \'{name}\'', 'one')[0]

    @staticmethod
    def update(name: str, condition: str):
        return database(f'UPDATE ml SET condition = \'{condition}\' WHERE name = \'{name}\'')


RANKS_DICT = {
    'Колокольчик': Wistle('Колокольчик', 0xc4986e),
    'Красный свисток': Wistle('Красный свисток', 0xe62329),
    'Синий свисток': Wistle('Синий свисток', 0x02aef1),
    'Лунный свисток': Wistle('Лунный свисток', 0x6064af),
    'Чёрный свисток': Wistle('Чёрный свисток', 0x22201e),
    'Белый свисток': Wistle('Белый свисток', 0xfefefe)
}

INDEX_VARIABLES = {}

INDEX_ML = {
    'corpus_condition': '0',
    'corpus_limit': '10000'
}


async def initialization(bot: commands.Bot):
    t = time.time()
    log('Инициализация', 'Database')

    database('''
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT UNIQUE,
            rank_id INT DEFAULT 0,
            complex_chars TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS variables (
            name TEXT UNIQUE,
            condition TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS ml (
            name TEXT UNIQUE,
            condition TEXT DEFAULT ''
        );
        
        CREATE TABLE IF NOT EXISTS servers_settings (
            id BIGINT UNIQUE,
            logging BIGINT DEFAULT 0
        );
    ''')

    log('   Инициализация стандартных параметров', 'Database')
    for k, v in INDEX_VARIABLES.items():
        if k not in map(lambda a: a[0], database(f'SELECT name FROM variables', 'all')):
            database(f'INSERT INTO variables VALUES (\'{k}\', \'{v}\')')
            log(f'      Параметр "{k}" добавлен')

    log('   Инициализация параметров ML', 'Database')
    for k, v in INDEX_ML.items():
        if k not in map(lambda a: a[0], database(f'SELECT name FROM ml', 'all')):
            database(f'INSERT INTO ml VALUES (\'{k}\', \'{v}\')')
            log(f'      Параметр "{k}" добавлен')

    log('   Добавление отсутствующих в таблицу', 'Database')
    for member in bot.get_all_members():
        if member.id not in map(lambda a: a[0], database('SELECT id FROM users', 'all')) and not member.bot:
            if await bot.is_owner(member):
                database(f'INSERT INTO users VALUES ({member.id}, 5)')
                log('      Владелец добавлен в таблицу', 'Database')

            else:
                database(f'INSERT INTO users VALUES ({member.id}, 0)')
                log(f'      Участник "{member.name}" добавлен в таблицу', 'Database')

    log('   Инициализация параметров серверов', 'Database')
    async for guild in bot.fetch_guilds(limit=None):
        if guild.id not in map(lambda a: a[0], database('SELECT id FROM servers_settings', 'all')):
            database(f'INSERT INTO servers_settings VALUES ({guild.id})')
            log(f'      Сервер "{guild.name}" добавлен в таблицу')

    log(f'Инициализация прошла успешно за {round(time.time() - t, 2)} с.', 'Database')

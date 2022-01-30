# Controlatoris diu terminus variables

import time

from disnake.ext import commands

from configuratione import config
from database import database
from utilitates import log

class Wistle:
    numerus = 0
    omnia = []

    def __init__(self, nomen: str, colour: int):
        self.nomen = nomen
        self.colour = colour
        self.prioritas = Wistle.numerus

        Wistle.numerus += 1
        Wistle.omnia.append(self)
    
    def __call__(self):
        return self.prioritas

    def __eq__(self, other):
        return self.prioritas == other.prioritas
    
    def __ne__(self, other):
        return self.prioritas != other.prioritas
    
    def __lt__(self, other):
        return self.prioritas < other.prioritas
    
    def __gt__(self, other):
        return self.prioritas > other.prioritas
    
    def __le__(self, other):
        return self.prioritas <= other.prioritas
    
    def __ge__(self, other):
        return self.prioritas >= other.prioritas
    
    @staticmethod
    def get(prioritas: int):
        for wistle in Wistle.omnia:
            if prioritas == wistle.prioritas:
                return wistle
        
        return False

class User:
    numerus = 0

    def __init__(self, id: int, occasione_id: int):
        self.id = id
        self.occasione_id = occasione_id
        self.occasiones = OCCASIONES_DICT.values()[occasione_id]

        User.numerus += 1
    
    def ingressum(self):
        log(f'  Пользователь с id {self.id} добавлен в таблицу', 'Database')
        database(f'INSERT INTO users (id) VALUES ({self.id});')
        return True
    
    def remotionem(self):
        database(f'DELETE FROM users WHERE id = {self.id};')
        return True
    
    @staticmethod
    def legere_all():
        return database(f'SELECT * FROM users', 'all')

class Doctrina:
    @staticmethod
    def extractio(nomen: str):
        return database(f'SELECT conditio FROM doctrina WHERE nomen = \'{nomen}\'', 'one')[0]
    
    @staticmethod
    def renovatio(nomen: str, conditio: str):
        return database(f'UPDATE doctrina SET conditio = \'{conditio}\' WHERE nomen = \'{nomen}\'')

OCCASIONES_DICT = {
    'Колокольчик': Wistle('Колокольчик', 0xc4986e),
    'Красный свисток': Wistle('Красный свисток', 0xe62329),
    'Синий свисток': Wistle('Синий свисток', 0x02aef1),
    'Лунный свисток': Wistle('Лунный свисток', 0x6064af),
    'Чёрный свисток': Wistle('Чёрный свисток', 0x22201e),
    'Белый свисток': Wistle('Белый свисток', 0xfefefe)
}

INDEX_VARIABILIUM = {}

INDEX_DOCTRINA = {
    'corpus_conditio': 'False',
    'corpus_limit': '10000'
}

async def initialization(machina: commands.Bot):
    t = time.time()
    log('Инициализация', 'Database')

    database('''
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT UNIQUE,
            occasione_id INT DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS variabilium (
            nomen TEXT UNIQUE,
            conditio TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS doctrina (
            nomen TEXT UNIQUE,
            conditio TEXT DEFAULT ''
        );
    ''')
    
    log('   Инициализация параметров доктрины', 'Database')
    for k, v in INDEX_DOCTRINA.items():
        if k not in map(lambda a: a[0], database(f'SELECT nomen FROM doctrina', 'all')):
            database(f'INSERT INTO doctrina VALUES (\'{k}\', \'{v}\')')
            log(f'      Параметр "{k}" добавлен')
    
    log('   Добавление отсутствующих в таблицу', 'Database')
    for member in machina.get_all_members():
        if member.id not in map(lambda a: a[0], database('SELECT id FROM users', 'all')) and not member.bot:
            if await machina.is_owner(member):
                database(f'INSERT INTO users VALUES ({member.id}, 5)')
                log('   Владелец добавлен в таблицу', 'Database')

            else:
                database(f'INSERT INTO users VALUES ({member.id}, 0)')
                log(f'   Участник "{member.name}" добавлен в таблицу', 'Database')
    
    log(f'Инициализация прошла успешно за {round(time.time() - t, 2)} с.', 'Database')
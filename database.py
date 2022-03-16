import os

import psycopg2
from dotenv import load_dotenv

from utilities import log

load_dotenv('.env')

class Database:
    def __init__(self, dbname, user, password, host, sslmode='require'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.sslmode = sslmode

        self.database = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, sslmode=sslmode)
        self.cursor = self.database.cursor()

    def __call__(self, command: str, output: str=None):
        try:
            self.cursor.execute(command)
            self.database.commit()
            log(f'Запрос "{command}"\nВыполнен', 'Database', 'debug')

            if output == 'one':
                out = self.cursor.fetchone()
            elif output == 'all':
                out = self.cursor.fetchall()
            else:
                out = True
            return out

        except psycopg2.ProgrammingError as error:
            self.database.rollback()
            log(error, 'Database', 'error')
            log('ОТКАТ', 'Database')
            raise error

database = Database(*eval(os.getenv('DATABASE_SETTINGS')).values())

def user_exist(id: int):
    return id in list(map(lambda el: el[0], database(f'''
        SELECT id FROM users
    ''', 'all')))

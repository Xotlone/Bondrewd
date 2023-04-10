import os

import sqlite3
from dotenv import load_dotenv
import disnake

from utilities import log

load_dotenv('.env')


class Database:
    def __init__(self):
        self.database = sqlite3.connect('database.db')
        self.cursor = self.database.cursor()

    def __call__(self, command: str):
        try:
            out = self.cursor.execute(command)
            self.database.commit()
            log(f'Запрос "{command}"\nВыполнен', 'Database', 'debug')
            return out

        except self.database.Error as error:
            try:
                self.cursor.execute('rollback')
                log('ОТКАТ', 'Database')
            except self.database.OperationalError:
                pass
            log(error, 'Database', 'error')
            raise error


cursor = Database()


def insert(*, users: list = None, guilds: list = None):
    """Добавление строк в таблицы"""

    def _insert_user(user: disnake.Member):
        all_users = cursor('SELECT id FROM users')
        if user.id not in map(lambda user_id: user_id[0], all_users):
            cursor(f'INSERT INTO users (id) VALUES ({user.id})')
            log(f'@{user} добавлен в таблицу', 'INSERT')

    def _insert_guild(guild: disnake.Guild):
        for member in guild.members:
            _insert_user(member)
        all_guilds = cursor('SELECT id FROM guilds')
        if guild.id not in map(lambda guild_id: guild_id[0], all_guilds):
            cursor(f'INSERT INTO guilds (id) VALUES ({guild.id})')
            log(f'Гильдия {guild.name} добавлена в таблицу', 'INSERT')

    if users is not None:
        for user in users:
            _insert_user(user)

    if guilds is not None:
        for guild in guilds:
            _insert_guild(guild)


def delete(*, users: list = None, guilds: list = None):
    """Удаление строк из таблицы"""

    def _delete_user(user: disnake.Member):
        all_users = cursor('SELECT id FROM users')
        if user.id in map(lambda user_id: user_id[0], all_users):
            cursor(f'DELETE FROM users WHERE id = {user.id}')
            log(f'@{user} удалён из таблицы', 'DELETE')

    def _delete_guild(guild: disnake.Guild):
        all_guilds = cursor('SELECT id FROM guilds')
        if guild.id in map(lambda guild_id: guild_id[0], all_guilds):
            cursor(f'DELETE FROM guilds WHERE id = {guild.id}')
            log(f'Гильдия {guild.name} удалена из таблицы', 'DELETE')

    if users is not None:
        for user in users:
            _delete_user(user)

    if guilds is not None:
        for guild in guilds:
            _delete_guild(guild)


def init():
    cursor(f'''CREATE TABLE IF NOT EXISTS users (
    id BIGINT UNIQUE,
    activity_scores BIGINT DEFAULT 0
)''')

    cursor(f'''CREATE TABLE IF NOT EXISTS guilds (
    id BIGINT UNIQUE,
    logging_chnl BIGINT DEFAULT 0
)''')

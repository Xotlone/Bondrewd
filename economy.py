from math import sqrt
import re

import disnake

from constants import config
from database import cursor

MAX_LEN = 2000
MAX_SCORES = 200
MAX_LEVEL = 80
EMOJI_FILTER = r'<:[\w]*:[0-9]*>'


def next_level(level: int):
    return level ** 3 * 5 + 100


levels_cost = [next_level(i + 1) for i in range(MAX_LEVEL - 1)]


def scores_to_levels(scores: int):
    remain_scores = scores
    for level in range(MAX_LEVEL - 1):
        if remain_scores > levels_cost[level]:
            remain_scores -= levels_cost[level]
        else:
            return {'level': level + 1, 'scores': remain_scores}


def scores_reward(msg_len: int):
    return int(sqrt(msg_len) * (MAX_SCORES / sqrt(MAX_LEN)))


async def message_check(msg: disnake.Message):
    if not config.DEVELOPMENT_MODE:
        author_scores = cursor(f'SELECT activity_scores FROM users WHERE id = {msg.author.id}')[0]
        after_level = scores_to_levels(author_scores)['level']
        if msg.content != '' and not re.match(EMOJI_FILTER, msg.content) and after_level < \
                MAX_LEVEL:
            author_scores += scores_reward(len(msg.content))
            before_level = scores_to_levels(author_scores)['level']
            if after_level < before_level:
                embed = disnake.Embed(
                    title=f'{msg.author} получает {before_level} уровень!',
                    color=disnake.Color.random()
                )
                await msg.channel.send(embed=embed)
            cursor(f'UPDATE users SET activity_scores = {author_scores} WHERE id = {msg.author.id}')

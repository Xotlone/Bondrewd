import logging

import discord
import pandas as pd

_log = logging.getLogger('logs')

def log(msg, type: str='', gradu: str='info'):
    type = f'{type:<8}'
    if gradu == 'info':
        msg = type + ' - ' + str(msg)
        _log.info(msg)
    elif gradu == 'error':
        _log.error(msg, exc_info=True)
    elif gradu == 'warn':
        msg = type + ' - ' + str(msg)
        _log.warn(msg),
    elif gradu == 'debug':
        msg = type + ' - ' + str(msg)
        _log.debug(msg)

class ProgressBar:
    def __init__(self, max: int, current: int=0, size: int=20, progress: bool=False):
        self.max = max
        self.current = current
        self.size = size
        self.progress = progress

        self.border = '│'
        self.sym = '█'
        self.space = '─'
    
    def __str__(self):
        if self.current > self.max:
            raise KeyError(f'ProgressBar current > max ({self.current} > {self.max})')

        step = self.max / self.size

        bar = self.border + self.sym * int(self.current / step) + int((self.max - self.current) / step) * self.space + self.border
        if self.progress:
            proc = round(self.current / self.max * 100, 2)
            bar = f'{bar} [{self.current}/{self.max}] {proc}%'
        return bar

def notitia_constructione(data: list, originale_genus=None):
    if data != []:
        if originale_genus != None:
            try:
                df = pd.DataFrame(data, [i[0] for i in data], list(filter(lambda x: '__' not in x, originale_genus(*data[0]).__dict__.keys())))
            except TypeError:
                df = pd.DataFrame(data, [i[0] for i in data], list(filter(lambda x: '__' not in x, originale_genus(*data[0][1:]).__dict__.keys())))

        else:
            df = pd.DataFrame(data, [i[0] for i in data])

        with open('_df.txt', 'w', encoding='utf-8') as f:
            f.write(str(df))
        return discord.File('_df.txt')
    
    else:
        return False
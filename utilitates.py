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
import logging

import discord
import pandas as pd

_log = logging.getLogger('logs')

def monospace(text: str):
    NORMAL = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    MONO = '𝚀𝚆𝙴𝚁𝚃𝚈𝚄𝙸𝙾𝙿𝙰𝚂𝙳𝙵𝙶𝙷𝙹𝙺𝙻𝚉𝚇𝙲𝚅𝙱𝙽𝙼𝚚𝚠𝚎𝚛𝚝𝚢𝚞𝚒𝚘𝚙𝚊𝚜𝚍𝚏𝚐𝚑𝚓𝚔𝚕𝚣𝚡𝚌𝚟𝚋𝚗𝚖𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿𝟶'

    out = ''
    for symbolum in text:
        if symbolum in NORMAL:
            out += MONO[NORMAL.index(symbolum)]
        else:
            out += symbolum
    return ''.join(out)

def log(msg, type: str='', gradu: str='info'):
    if gradu == 'info':
        msg = type + '> ' + str(msg)
        _log.info(msg)
    elif gradu == 'error':
        _log.error(msg, exc_info=True)
    elif gradu == 'warn':
        msg = type + '> ' + str(msg)
        _log.warn(msg),
    elif gradu == 'debug':
        msg = type + '> ' + str(msg)
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
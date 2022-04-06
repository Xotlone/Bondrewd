import os
import csv
from itertools import groupby
import re

import numpy as np

from utilities import log

normed_exponential_func = lambda z: np.exp(z) / np.sum(np.exp(z))


class Tokenizator:
    available_symbols = 'йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm'

    @staticmethod
    def corpus_init():
        pass

    @staticmethod
    def corpus_get():
        pass

    @staticmethod
    def pre(sentence: str):
        tokens = re.split(r'[-\s.,;!?]', sentence.lower())
        out = []
        for token in tokens:
            out.append(''.join(filter(lambda s: s in Tokenizator.available_symbols, token)))
            if out[-1] == '':
                del out[-1]

        return out

    @staticmethod
    def tokenize(author_id: id, sentence: str):
        pass

    @staticmethod
    def corpus_update(author_id: int, sentence: str):
        pass


def skip_gramm(sentence: str, n_gramm: int = 3, padding: str = 'correspond'):
    processed = Tokenizator.pre(sentence)

    if padding == 'ignore':
        arange = range(len(processed))
    elif padding == 'correspond':
        arange = range(int(n_gramm / 2), len(processed) - int(n_gramm / 2))
    else:
        raise ValueError('Padding must be "ignore" or "correspond"')

    output = []
    for step in arange:
        surrounding = []
        half_gramm = list(range(1, int((n_gramm - 1) / 2 + 1)))
        minus_half_gramm = list(map(lambda x: -x, half_gramm))
        minus_half_gramm.reverse()
        gramm_window = minus_half_gramm + half_gramm
        for n in gramm_window:
            if n + step < 0 or n + step > len(processed) - 1:
                continue
            surrounding.append(processed[n + step])
        output.append({processed[step]: surrounding})

    return output

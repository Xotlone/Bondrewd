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
        if not os.path.exists('ml/corpus.csv'):
            with open('ml/corpus.csv', 'w', newline='', encoding='utf-8') as f:
                pass
            log('   Корпус не был обнаружен. Создан новый', 'Corpus')

    @staticmethod
    def corpus_get():
        with open('ml/corpus.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            corpus = [token for token in reader]
        
        return corpus

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
        tokens = Tokenizator.pre(sentence)
        corpus = Tokenizator.corpus_get()
        vector = []
        for token in tokens:
            if token not in map(lambda el: el[1], corpus):
                corpus.append([author_id, token, len(corpus)])
            
            vector.append([])
            for word in map(lambda el: el[1], corpus):
                vector[-1].append(int(word == token))
        
        return np.array(vector)
    
    @staticmethod
    def corpus_update(author_id: int, sentence: str):
        corpus = Tokenizator.corpus_get()
        sentence_tokens = Tokenizator.pre(sentence)
        for token in sentence_tokens:
            if token != '' and token not in map(lambda w: w[1], corpus):
                corpus.append([author_id, token, len(corpus)])
        
        with open('ml/corpus.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(corpus)
    
    @staticmethod
    def update_rating():
        corpus = Tokenizator.corpus_get()
        groups = groupby(corpus, lambda r: r[0])
        counts = [(a, len(list(c))) for a, c in groups]
        return {k: v for (k, v) in sorted(counts, key=lambda el: el[1])}
import os
import csv
from itertools import groupby
import re

from utilitates import log

def prae_instructio_sententia(
    sententia: str,
    is_lower=True,
    _filter=r'[^a-z]',
    split=' '
):
    if is_lower:
        sententia = sententia.lower()
    if _filter != '':
        sententia = re.sub(_filter, '', sententia)
    return sententia.split(split)

def corpus_creatio():
    if not os.path.exists('apparatus_doctrina/corpus.csv'):
        with open('apparatus_doctrina/corpus.csv', 'w', newline='', encoding='utf-8') as f:
            pass
        log('   Корпус не был обнаружен. Создан новый', 'Corpus')

def corpus_addition(author_id: int, sententia: str):
    log(f'corpus_addition(\'{sententia}\')', 'Corpus')
    corpus_creatio()

    with open('apparatus_doctrina/corpus.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        sententia = prae_instructio_sententia(sententia)

        corpus = [row[1] for row in reader]
        for el in sententia:
            if len(el) <= 16 and len(el) > 2:
                corpus.append(el)
        corpus = [el for el, _ in groupby(corpus)]

    with open('apparatus_doctrina/corpus.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows([[author_id, w] for w in corpus])
        del corpus

def corpus_len():
    corpus_creatio()

    with open('apparatus_doctrina/corpus.csv', 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        return len(list(reader))
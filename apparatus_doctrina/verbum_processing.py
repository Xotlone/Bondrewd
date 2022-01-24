import json
import logging
import os

log = logging.getLogger('logs')

def prae_instructio_sententia(
    sententia: str,
    is_lower=True,
    _filter='()[]{}<>!?\"\'\\/,.;:*&%#@$^|+-=`~',
    split=' '
):  
    log.info(f'>prae_instructio_sententia(\'{sententia}\', {is_lower}, \'{_filter}\', \'{split}\')')
    if is_lower:
        sententia = sententia.lower()
    if _filter != '':
        sententia = ''.join(filter(lambda symbolum: symbolum not in _filter, sententia))
    return sententia.split(split)

def corpus_addition(sententia: str):
    log.info(f'>corpus_addition(\'{sententia}\')')
    if not os.path.exists('corpus.json'):
        json.dump([], 'corpus.json')
        log.info('\tCorpus non invenitur. Novum creatum')
    corpus = json.load('corpus.json')

    sententia = prae_instructio_sententia(sententia)
    for elementum in sententia:
        if elementum not in sententia:
            corpus.append(elementum)

    json.dump(corpus, 'corpus.json')
    log.info('\tCorpus updated')

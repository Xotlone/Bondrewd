import logging
import requests
import random
from math import exp

from bs4 import BeautifulSoup

from constants import config

_log = logging.getLogger('logs')


def log(msg, log_type: str = 'UNKNOWN', log_as: str = 'info'):
    log_type = f'{log_type:<8}'
    if log_as == 'info':
        msg = log_type + ' - ' + str(msg)
        _log.info(msg)
    elif log_as == 'error':
        _log.error(msg, exc_info=True)
    elif log_as == 'warn':
        msg = log_type + ' - ' + str(msg)
        _log.warning(msg),
    elif log_as == 'debug':
        msg = log_type + ' - ' + str(msg)
        _log.debug(msg)


def normed_exponential(z: list):
    k = 10 ** len(str(max(z)))
    x = list(map(lambda n: n / k, z))
    x_exps = list(map(lambda y: y if y != 1 else 0, list(map(lambda n: exp(n), x))))
    sum_x_exps = sum(x_exps)
    return [y / sum_x_exps for y in x_exps]


class ProgressBar:
    def __init__(self, max_size: int, current: int = 0, size: int = 10, advanced: bool = False):
        self.max_size = max_size
        self.current = current
        self.size = size
        self.advanced = advanced

        self.border = '│'
        self.sym = '█'
        self.space = '─'

    def __str__(self):
        if self.current > self.max_size:
            raise KeyError(f'ProgressBar current > max ({self.current} > {self.max_size})')

        step = self.max_size / self.size

        bar = self.border + self.sym * int(self.current / step) + int(
            (self.max_size - self.current) / step) * self.space + self.border
        if self.advanced:
            proc = round(self.current / self.max_size * 100, 2)
            bar = f'{bar} [{self.current}/{self.max_size}] {proc}%'
        return bar


class Parser:
    def __init__(self, attempts=20):
        """Родительский класс для парсинга"""
        self.attempts = attempts

    def try_parse(self, count: int = 1):
        """Попытка парсинга"""
        objects = []
        attempt = 0
        for i in range(count):
            while 1:
                try:
                    parsed = self.parse()
                    repeated_attempt = 0
                    while 1:
                        if parsed in objects or parsed is False:
                            parsed = self.parse()
                            log(f'    Существующее изображение или неудачный результат. Попытка {repeated_attempt}...')
                            repeated_attempt += 1
                            if repeated_attempt > self.attempts:
                                raise Exception('parsing', self.attempts, 'repeated attempts exhausted')
                        else:
                            objects.append(parsed)
                            break
                    break

                except TypeError:
                    log(f'    Попытка парсинга {attempt} неудачна...')
                    attempt += 1
                    if attempt > self.attempts:
                        raise Exception('parsing', self.attempts, 'attempts exhausted')

        return objects

    def parse(self) -> dict:
        """Уникальная функция парсинга одного объекта"""
        pass


class AnimeParser(Parser):
    link = config.ANIMELINK

    def parse(self):
        rnd = random.randint(1000, config.ANIMEITEMSCOUNT)
        response = requests.get(
            f'https://safebooru.donmai.us/posts/{rnd}',
            headers=config.HEADERS
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        item = soup.find('img', {'id': 'image'})['src']
        return {'image': item}


class AnimeEroParser(Parser):
    link = config.ANIMEEROLINK

    def parse(self):
        response = requests.get(
            config.ANIMEEROLINK,
            headers=config.HEADERS
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        count = int(soup.find('div', {'class': 'pagination_expanded'}).find_all('a')[0].text)
        rnd = random.randint(0, count)

        page = requests.get(
            f'{config.ANIMEEROLINK}/{rnd}',
            headers=config.HEADERS
        )
        soup = BeautifulSoup(page.content, 'html.parser')
        item = 'https:' + random.choice(soup.findAll('div', {'class': 'image'})).find('img')['src']
        return {'image': item}


class AnimeEroGifsParser(Parser):
    link = config.ANIMEEROGIFSLINK

    def parse(self):
        response = requests.get(
            config.ANIMEEROGIFSLINK,
            headers=config.HEADERS
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        count = int(soup.find('div', {'class': 'pagination_expanded'}).find_all('a')[0].text)

        for at in range(self.attempts):
            rnd = random.randint(0, count)
            page = requests.get(
                f'{config.ANIMEEROGIFSLINK}/{rnd}',
                headers=config.HEADERS
            )
            soup = BeautifulSoup(page.content, 'html.parser')
            item = 'https:' + random.choice(soup.findAll('div', {'class': 'image'})).find('img')['src']
            if '.gif' in item:
                return {'image': item}
        return False


class AnimeEarsParser(Parser):
    link = config.ANIMENEKOLINK

    def parse(self):
        response = requests.get(
            config.ANIMENEKOLINK,
            headers=config.HEADERS
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        count = int(soup.find('div', {'class': 'pagination_expanded'}).find_all('a')[0].text)
        rnd = random.randint(0, count)

        page = requests.get(
            f'{config.ANIMENEKOLINK}/{rnd}',
            headers=config.HEADERS
        )
        soup = BeautifulSoup(page.content, 'html.parser')
        item = 'https:' + random.choice(soup.findAll('div', {'class': 'image'})).find('img')['src']
        return {'image': item}


class AnimeCuteParser(Parser):
    link = config.ANIMECUTELINK

    def parse(self):
        response = requests.get(
            config.ANIMECUTELINK,
            headers=config.HEADERS
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        count = int(soup.find('div', {'class': 'pagination_expanded'}).find_all('a')[0].text)
        rnd = random.randint(0, count)

        page = requests.get(
            f'{config.ANIMECUTELINK}/{rnd}',
            headers=config.HEADERS
        )
        soup = BeautifulSoup(page.content, 'html.parser')
        item = 'https:' + random.choice(soup.findAll('div', {'class': 'image'})).find('img')['src']
        return {'image': item}


class AnimeMonsterGirlParser(Parser):
    link = config.ANIMEMONSTERGIRLLINK

    def parse(self):
        response = requests.get(
            config.ANIMEMONSTERGIRLLINK,
            headers=config.HEADERS
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        count = int(soup.find('div', {'class': 'pagination_expanded'}).find_all('a')[0].text)
        rnd = random.randint(0, count)

        page = requests.get(
            f'{config.ANIMEMONSTERGIRLLINK}/{rnd}',
            headers=config.HEADERS
        )
        soup = BeautifulSoup(page.content, 'html.parser')
        item = 'https:' + random.choice(soup.findAll('div', {'class': 'image'})).find('img')['src']
        return {'image': item}


class HentaiParser(Parser):
    link = config.HENTAILINK

    def parse(self):
        response = requests.get(
            config.HENTAILINK,
            headers=config.HEADERS
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        count = int(soup.find('div', {'class': 'navi_link'}).findAll('a')[-1].text)
        rnd = random.randint(1, count)
        if rnd != 1:
            response = requests.get(
                f'https://anitokyo.tv/hentai/page/{rnd}/',
                headers=config.HEADERS
            )
            soup = BeautifulSoup(response.content, 'html.parser')

        item = random.choice(soup.findAll('article', {'class': 'story shortstory'}))
        image = 'https://anitokyo.tv' + item.find('img', {'class': 'poster'})['src']
        link = item.find('h2', {'class': 'story-title'}).a['href']
        title = item.find('h2', {'class': 'story-title'}).a.text
        desc = item.find('div', {'class': 'story-description'}).text[10:]
        return {'image': image, 'link': link, 'title': title, 'desc': desc}

# Controlatoris diu terminus variables

from database import database
from utilitates import log

class Occasiones:
    numerus = 0

    def __init__(self, nomen: str, prioritas: int):
        self.nomen = nomen
        self.prioritas = prioritas

        self.id = Occasiones.numerus
        Occasiones.numerus += 1
    
    def __call__(self):
        return self.prioritas

    def __eq__(self, other):
        return self.prioritas == other.prioritas
    
    def __ne__(self, other):
        return self.prioritas != other.prioritas
    
    def __lt__(self, other):
        return self.prioritas < other.prioritas
    
    def __gt__(self, other):
        return self.prioritas > other.prioritas
    
    def __le__(self, other):
        return self.prioritas <= other.prioritas
    
    def __ge__(self, other):
        return self.prioritas >= other.prioritas

class AccessumCampester:
    numerus = 0

    def __init__(self, nomen: str, prioritas: int, occasiones: str):
        self.nomen = nomen
        self.prioritas = prioritas
        self.occasiones = occasiones

        self.id = AccessumCampester.numerus
        AccessumCampester.numerus += 1
    
    def __eq__(self, other):
        for occasion in self.occasiones:
            if occasion in other.occasiones:
                return True
        return False

    def ingressum(self):
        log(f'  A accessum "{self.nomen}" scriptum est database', 'Database')
        database(f'INSERT INTO accessum_campesters VALUES ({self.id}, \'{self.nomen}\', {self.prioritas}, \'{self.occasiones}\');')
        return True
    
    def remotionem(self):
        database(f'DELETE FROM accessum_campesters WHERE id = {self.id};')
        return True
    
    @staticmethod
    def legere_all():
        return database(f'SELECT * FROM accessum_campesters', 'all')
    
    @staticmethod
    def get(where: str):
        raw_accessum = database(f'SELECT * FROM accessum_campesters WHERE {where}', 'one')
        accessum = AccessumCampester(*raw_accessum[1:])
        accessum.id = raw_accessum[0]
        return accessum

class User:
    numerus = 0

    def __init__(self, id: int, accessum_id: int):
        self.id = id
        self.accessum_id = accessum_id
        self.accessum = AccessumCampester.get(f'id = {accessum_id}')

        User.numerus += 1
    
    def ingressum(self):
        log(f'  A user {self.id} scriptum est database', 'Database')
        database(f'INSERT INTO users (id) VALUES ({self.id});')
        return True
    
    def remotionem(self):
        database(f'DELETE FROM users WHERE id = {self.id};')
        return True
    
    @staticmethod
    def legere_all():
        return database(f'SELECT * FROM users', 'all')
    
    @staticmethod
    def get(where: str):
        raw_user = database(f'SELECT * FROM users WHERE {where}', 'one')
        user = User(*raw_user)
        return user

class Variabilis:
    numerus = 0

    def __init__(self, nomen: str, genus: str, valorem: str):
        self.nomen = nomen
        self.genus = genus
        self.valorem = valorem

        self.id = Variabilis.numerus
        Variabilis.numerus += 1
    
    def ingressum(self):
        log(f'  A variabilis {self.nomen} = {self.valorem} scriptum est database', 'Database')
        database(f'INSERT INTO variabilium (id, nomen, genus, velorem) VALUES ({self.id}, \'{self.nomen}\', \'{self.genus}\', \'{self.valorem}\');')
        return True
    
    def remotionem(self):
        database(f'DELETE FROM variabilium WHERE id = {self.id};')
        return True
    
    @staticmethod
    def legere_all():
        return database(f'SELECT * FROM variabilium', 'all')

TERMINUS_COMITIA = {'users': User, 'accessum_campesters': AccessumCampester, 'variabilium': Variabilis}

INDEX_OCCASIONES = [
    Occasiones('Колокольчик', 0),
    Occasiones('Красный свисток', 1),
    Occasiones('Синий свисток', 2),
    Occasiones('Лунный свисток', 3),
    Occasiones('Чёрный свисток', 4),
    Occasiones('Белый свисток', 5)
]

INDEX_ACCESSUM_CAMPESTER = [
    AccessumCampester('Omega', 0, 'Колокольчик'),
    AccessumCampester('Alpha', 23, 'Белый свисток')
]

INDEX_VARIABILIUM = [

]

INDEX_DOCTRINA = {
    'corpus_conditio': 'False',
    'corpus_limit': '10000'
}

def initialization():
    log('Initialization()', 'Database')
    for accessum in INDEX_ACCESSUM_CAMPESTER:
        if database(f'SELECT * FROM accessum_campesters WHERE id = {accessum.id}', 'all') == []:
            accessum.ingressum()
            log(f'  Accessum campester "{accessum.nomen}" additae', 'Database')
    
    for k, v in INDEX_DOCTRINA.items():
        if database(f'SELECT * FROM doctrina WHERE nomen = \'{k}\'', 'all') == []:
            database(f'INSERT INTO doctrina VALUES (\'{k}\', \'{v}\')')
            log(f'  Doctrina parametri "{k}" adiecit')
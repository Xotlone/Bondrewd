# Controlatoris diu terminus variables

from database import database
from utilitates import log

class Users:
    numerus = 0

    def __init__(self, id: int, accessum_id: int):
        self.id = id
        self.accessum_id = accessum_id

        Users.numerus += 1
    
    def ingressum(self):
        database(f'INSERT INTO users (id) VALUES ({self.id});')
        return True
    
    def remotionem(self):
        database(f'DELETE FROM users WHERE id = {self.id};')
        return True
    
    @staticmethod
    def legere_all():
        return database(f'SELECT * FROM users', 'all')

class AccessumCampester:
    numerus = 0

    def __init__(self, nomen: str, prioritas: int, occasiones):
        self.nomen = nomen
        self.prioritas = prioritas
        self.occasiones = occasiones

        self.id = AccessumCampester.numerus
        AccessumCampester.numerus += 1
    
    def ingressum(self):
        database(f'INSERT INTO accessum_campesters (id, prioritas, occasiones) VALUES ({self.id}, {self.prioritas}, \'{self.occasiones}\');')
        return True
    
    def remotionem(self):
        database(f'DELETE FROM accessum_campesters WHERE id = {self.id};')
        return True
    
    @staticmethod
    def legere_all():
        return database(f'SELECT * FROM accessum_campesters', 'all')

class Variabilis:
    numerus = 0

    def __init__(self, nomen: str, genus: str, valorem: str):
        self.nomen = nomen
        self.genus = genus
        self.valorem = valorem

        self.id = Variabilis.numerus
        Variabilis.numerus += 1
    
    def ingressum(self):
        database(f'INSERT INTO variabilium (id, nomen, genus, velorem) VALUES ({self.id}, \'{self.nomen}\', \'{self.genus}\', \'{self.valorem}\');')
        return True
    
    def remotionem(self):
        database(f'DELETE FROM variabilium WHERE id = {self.id};')
        return True
    
    @staticmethod
    def legere_all():
        return database(f'SELECT * FROM variabilium', 'all')

class Textuum:
    numerus = 0

    def __init__(self, nomen: str, valorem: str):
        self.nomen = nomen
        self.valorem = valorem

        self.id = Textuum.numerus
        Textuum.numerus += 1
    
    def ingressum(self):
        database(f'INSERT INTO textuum (id, nomen, velorem)VALUES ({self.id}, \'{self.nomen}\', \'{self.valorem}\');')
        return True
    
    def remotionem(self):
        database(f'DELETE FROM textuum WHERE id = {self.id};')
        return True
    
    @staticmethod
    def legere_all():
        return database(f'SELECT * FROM textuum', 'all')

TERMINUS_COMITIA = {'users': Users, 'accessum_campesters': AccessumCampester, 'variabilium': Variabilis, 'textuum': Textuum}

INDEX_ACCESSUM_CAMPESTER = [
    AccessumCampester('Omega', 0, 'aperta_procuratio'),
    AccessumCampester('Alpha', 23, 'aperta_procuratio;clausa_procuratio')
]

INDEX_VARIABILIUM = [

]

INDEX_TEXTORUM = [

]

def initialization():
    log('Initialization()', 'D')
    for index in INDEX_ACCESSUM_CAMPESTER:
        if database(f'SELECT * FROM accessum_campesters WHERE id = {index.id}', 'all') == []:
            index.ingressum()
            log(f'\tAccessum campester {index.nomen} additae', 'D')
# Controlatoris diu terminus variables

import logging

from database import database

log = logging.getLogger('logs')

class AccessumCampester:
    id = 0

    def __init__(self, nomen: str, prioritas: int, occasiones):
        self.nomen = nomen
        self.prioritas = prioritas
        self.occasiones = occasiones

        self.id = AccessumCampester.id
        AccessumCampester.id += 1
    
    def ingressum(self):
        database.executio('accessum_ingressum', None,
            id=self.id,
            nomen=self.nomen,
            prioritas=self.prioritas,
            occasiones=self.occasiones
        )
        return True
    
    def remotionem(self):
        database.executio('accessum_remotionem', None,
            id=self.id
        )
        return True
    
    @staticmethod
    def lectio(id: int):
        accessum = database.executio('accessum_lectio', 'one',
            id=id
        )
        return accessum
    
    @staticmethod
    def legere_all():
        return database.executio('accessum_legere_all', 'all')

class Variabilis:
    numerus = 0

    def __init__(self, nomen: str, genus: type, valorem: any):
        self.nomen = nomen
        self.genus = genus
        self.valorem = valorem

        Variabilis.numerus += 1

class Textuum:
    numerus = 0

    def __init__(self, nomen: str, valorem: str):
        self.nomen = nomen
        self.valorem = valorem

        Textuum.numerus += 1

INDEX_ACCESSUM_CAMPESTER = [
    AccessumCampester('Omega', 0, 'aperta_procuratio'),
    AccessumCampester('Alpha', 23, 'aperta_procuratio;clausa_procuratio')
]

INDEX_VARIABILIUM = [

]

INDEX_TEXTORUM = [

]
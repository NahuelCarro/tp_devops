from app.models.apuesta import Apuesta
from app.repository.apuesta_repository import ApuestaRepository


class ApuestaService:
    def __init__(self, apuesta_repository: ApuestaRepository):
        self.apuesta_repository = apuesta_repository

    def crear_apuesta(self, apuesta: Apuesta):
        self.apuesta_repository.guardar(apuesta)
        return apuesta

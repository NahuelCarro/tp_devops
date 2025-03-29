from typing import Optional


from app.models.apuesta import Apuesta
from app.models.apostador import Apostador
from app.repository.caballo_repository import CaballoRepository
from app.repository.carrera_repository import CarreraRepository
from app.repository.apuesta_repository import ApuestaRepository
from app.repository.apostador_repository import ApostadorRepository
from app.services.caballo_service import CaballoService
from app.services.carrera_service import CarreraService
from app.services.apuesta_service import ApuestaService
from app.exceptions import (
    EmailDuplicadoException,
    MontoApuestaInvalidoException,
    CarreraYaIniciadaException,
    CaballoNoInscriptoException,
    ApostadorYaApostoException
)


class ApostadorService:
    def __init__(
        self,
        apostador_repository: ApostadorRepository,
    ):
        self.apostador_repository = apostador_repository

    def crear_apostador(
        self, nombre: str, mail: str, clave: str, es_admin: bool
    ) -> Apostador:
        if self.apostador_repository.obtener_por_mail(mail):
            raise EmailDuplicadoException()

        apostador = Apostador(
            nombre=nombre, mail=mail, clave=clave, es_admin=es_admin
        )
        self.apostador_repository.guardar(apostador)
        return apostador

    def obtener_apostador(self, mail: str) -> Optional[Apostador]:
        return self.apostador_repository.obtener_por_mail(mail)

    def apostar(
        self,
        mail: str,
        carrera_id: int,
        nombre_caballo: str,
        monto: float
    ) -> Apuesta:
        apostador = self.apostador_repository.obtener_por_mail(mail)
        session = self.apostador_repository.session

        caballo_repository = CaballoRepository(session)
        caballo_service = CaballoService(caballo_repository)
        caballo = caballo_service.obtener_caballo(nombre_caballo)

        carrera_repository = CarreraRepository(session)
        carrera_service = CarreraService(carrera_repository)
        carrera = carrera_service.obtener_carrera_por_id(carrera_id)

        if monto < 0:
            raise MontoApuestaInvalidoException()
        if carrera.esta_iniciada():
            raise CarreraYaIniciadaException()
        if caballo not in carrera.caballos:
            raise CaballoNoInscriptoException()
        if any(apuesta.apostador_id == apostador.id for apuesta in carrera.apuestas):
            raise ApostadorYaApostoException()

        apuesta = apostador.apostar(caballo, carrera, monto)
        apuesta_repository = ApuestaRepository(session)
        apuesta_service = ApuestaService(apuesta_repository)
        apuesta_service.crear_apuesta(apuesta)
        carrera_service.actualizar_carrera(carrera)
        self.apostador_repository.guardar(apostador)
        return apuesta

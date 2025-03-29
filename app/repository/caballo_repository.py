from app.models.caballo import Caballo
from .base_repository import BaseRepository
from typing import Optional
from sqlmodel import select


class CaballoRepository(BaseRepository):
    def obtener_por_nombre(self, nombre: str) -> Optional[Caballo]:
        statement = select(Caballo).where(Caballo.nombre == nombre)
        return self.session.exec(statement).first()

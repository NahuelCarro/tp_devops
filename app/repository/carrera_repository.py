from datetime import datetime
from typing import Optional
from sqlmodel import select

from .base_repository import BaseRepository
from app.models.carrera import Carrera


class CarreraRepository(BaseRepository):
    def obtener_carreras_disponibles(
        self,
        fecha_actual: datetime,
        cantidad_por_pagina: int = 10,
        pagina: int = 0
    ):
        offset = pagina * cantidad_por_pagina
        statement = (
            select(Carrera)
            .where(Carrera.fecha > fecha_actual)
            .order_by(Carrera.fecha)
            .limit(cantidad_por_pagina)
            .offset(offset)
        )
        return self.session.exec(statement).all()

    def obtener_por_id(self, id: int) -> Optional[Carrera]:
        statement = select(Carrera).where(Carrera.id == id)
        return self.session.exec(statement).first()

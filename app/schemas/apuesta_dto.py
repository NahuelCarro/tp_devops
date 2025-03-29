from sqlmodel import SQLModel
from pydantic import Field
from datetime import datetime
from app.models.apuesta import Apuesta


class ApuestaCreacionDTO(SQLModel):
    monto: float = Field(description="El monto de la apuesta")


class ApuestaDTO(ApuestaCreacionDTO):
    fecha: datetime = Field(description="La fecha de la apuesta")
    carrera_id: int = Field(description="El ID de la carrera")
    caballo_nombre: str = Field(description="El nombre del caballo")

    def __init__(self, apuesta: Apuesta):
        self.monto = apuesta.monto
        self.fecha = apuesta.fecha
        self.carrera_id = apuesta.carrera.id
        self.caballo_nombre = apuesta.caballo.nombre

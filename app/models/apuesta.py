from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from app.models.carrera import Carrera
from app.models.caballo import Caballo


class Apuesta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    fecha: datetime = Field(default=datetime.now())
    monto: float = Field(nullable=False)

    apostador_id: Optional[int] = Field(foreign_key="apostador.id", nullable=False)
    carrera_id: Optional[int] = Field(foreign_key="carrera.id", nullable=False)
    caballo_id: Optional[int] = Field(foreign_key="caballo.id", nullable=False)

    apostador: Optional["Apostador"] = Relationship(back_populates="apuestas")
    carrera: Optional[Carrera] = Relationship(back_populates="apuestas")
    caballo: Optional[Caballo] = Relationship(back_populates="apuestas")

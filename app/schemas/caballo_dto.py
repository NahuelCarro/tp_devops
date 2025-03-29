from sqlmodel import SQLModel
from pydantic import Field
from app.models.caballo import Caballo
from app.models.carrera import Carrera


class CaballoDTO(SQLModel):
    nombre: str = Field(description="El nombre del caballo")
    peso: float = Field(description="El peso del caballo")

    def __init__(self, caballo: Caballo):
        self.nombre = caballo.nombre
        self.peso = caballo.peso


class CaballoConPorcentajeGanadorDTO(CaballoDTO):
    porcentaje_de_pago: float = Field(
        description="El porcentaje de pago para el caballo ganador"
    )

    def __init__(self, caballo: Caballo, carrera: Carrera):
        super().__init__(caballo)
        self.porcentaje_de_pago = carrera.porcentaje_ganador(caballo)

import random
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

from app.models.carrera_caballo_link import CarreraCaballoLink


class Carrera(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    fecha: datetime = Field(nullable=False)

    apuestas: list["Apuesta"] = Relationship(back_populates="carrera")
    caballos: list["Caballo"] = Relationship(
        back_populates="carreras", link_model=CarreraCaballoLink
    )
    caballo_ganador_id: Optional[int] = Field(default=None, foreign_key="caballo.id")
    caballo_ganador: Optional["Caballo"] = Relationship()

    def inscribir_caballo(self, caballo: "Caballo"):
        if caballo not in self.caballos:
            self.caballos.append(caballo)

    def esta_iniciada(self) -> bool:
        return self.fecha < datetime.now()

    def determinar_ganador(self):
        if not self.caballos:
            raise ValueError("No hay caballos para la carrera")
        ganador = random.choice(self.caballos)
        self.caballo_ganador = ganador
        self.caballo_ganador_id = ganador.id
        self.pagar_apuestas(self.apuestas)

    def pagar_apuestas(self, apuestas: list["Apuesta"]):
        for apuesta in apuestas:
            if apuesta.caballo == self.caballo_ganador:
                apuesta.apostador.balance_apuestas += (
                    apuesta.monto * self.porcentaje_ganador(apuesta.caballo)
                )
            else:
                apuesta.apostador.balance_apuestas -= apuesta.monto

    def porcentaje_ganador(self, caballo: "Caballo") -> float:
        """Calcula el porcentaje ganador para un caballo específico basado en
        la cantidad de apuestas realizadas a él.

        Args:
            caballo (Caballo): Instancia del caballo para el cual calcular el porcentaje.

        Returns:
            float: Porcentaje ganador como float.
        """
        cantidad_apuestas = sum(
            1 for apuesta in self.apuestas if apuesta.caballo_id == caballo.id
        )

        porcentaje = 2.00 - 0.10 * (cantidad_apuestas - 1)

        porcentaje = max(porcentaje, 1.01)

        return porcentaje

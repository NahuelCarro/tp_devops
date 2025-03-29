from typing import Optional
from datetime import datetime
from fastapi import HTTPException, status

from app.models.carrera import Carrera
from app.models.caballo import Caballo
from app.repository.carrera_repository import CarreraRepository
from app.exceptions import (
    FechaCarreraInvalidaException,
    CarreraNoIniciadaException,
    CarreraYaFinalizadaException,
    CarreraYaIniciadaException,
    CarreraNoEncontradaException
)


class CarreraService:
    def __init__(self, carrera_repository: CarreraRepository):
        self.carrera_repository: CarreraRepository = carrera_repository

    def obtener_carreras_disponibles(
        self,
        cantidad_por_pagina: int = 10,
        pagina: int = 0
    ):
        fecha_actual = datetime.now()
        return self.carrera_repository.obtener_carreras_disponibles(
            fecha_actual, cantidad_por_pagina, pagina
        )

    def crear_carrera(self, fecha: datetime):
        if fecha < datetime.now():
            raise FechaCarreraInvalidaException()
        carrera = Carrera(fecha=fecha)
        self.carrera_repository.guardar(carrera)
        return carrera

    def agregar_caballo(self, carrera: Carrera, caballo: Caballo):
        carrera_obtenida: Carrera = self.carrera_repository.obtener_por_id(
            carrera.id
        )
        if carrera_obtenida.esta_iniciada():
            raise CarreraYaIniciadaException()
        carrera_obtenida.inscribir_caballo(caballo)
        self.carrera_repository.guardar(carrera_obtenida)
        return carrera_obtenida

    def empezar_carrera(self, carrera: Carrera):
        if not carrera.esta_iniciada():
            raise CarreraNoIniciadaException()
        if carrera.caballo_ganador_id:
            raise CarreraYaFinalizadaException()
        try:
            carrera.determinar_ganador()
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        self.carrera_repository.guardar(carrera)
        return carrera

    def obtener_carrera_por_id(self, id: int) -> Optional[Carrera]:
        carrera = self.carrera_repository.obtener_por_id(id)
        if not carrera:
            raise CarreraNoEncontradaException()
        return carrera

    def actualizar_carrera(self, carrera: Carrera):
        self.carrera_repository.guardar(carrera)

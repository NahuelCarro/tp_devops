from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path, status

from app.database import SessionDep
from app.models.apostador import Apostador
from app.auth.auth import get_current_user
from app.services.carrera_service import CarreraService
from app.services.caballo_service import CaballoService
from app.repository.carrera_repository import CarreraRepository
from app.repository.caballo_repository import CaballoRepository
from app.schemas.carrera_dto import (
    CarreraCreacionDTO,
    CarreraDTO,
    CarreraConCaballosDTO,
    CarreraConCaballoGanadorDTO,
)
from app.exceptions import (
    UsuarioNoAdministradorException,
    LimiteOffsetNegativoException,
)
router = APIRouter(prefix="/carrera")


@router.post(
    "/crear",
    response_model=CarreraDTO,
    status_code=status.HTTP_201_CREATED
)
def crear_carrera(
    session: SessionDep,
    carrera_dto: CarreraCreacionDTO,
    current_user: Apostador = Depends(get_current_user),
):

    if not current_user.es_admin:
        raise UsuarioNoAdministradorException(
            "No tienes permisos para crear una carrera"
        )

    carrera_repository = CarreraRepository(session)
    carrera_service = CarreraService(carrera_repository)
    return CarreraDTO(carrera_service.crear_carrera(carrera_dto.fecha))


@router.get(
    "/listar",
    response_model=list[CarreraConCaballosDTO],
    status_code=status.HTTP_200_OK
)
def listar_carreras(
    session: SessionDep,
    cantidad_por_pagina: int = Query(
        default=10, description="El número máximo de carreras a devolver"
    ),
    pagina: int = Query(default=0, description="El número de carreras a saltar"),
):
    if cantidad_por_pagina < 0 or pagina < 0:
        raise LimiteOffsetNegativoException()
    carrera_repository = CarreraRepository(session)
    carrera_service = CarreraService(carrera_repository)
    return [
        CarreraConCaballosDTO(carrera)
        for carrera in carrera_service.obtener_carreras_disponibles(
            cantidad_por_pagina, pagina
        )
    ]


@router.put(
    "/agregar_caballo/{carrera_id}/{nombre_caballo}",
    response_model=CarreraConCaballosDTO,
    status_code=status.HTTP_200_OK
)
def agregar_caballo(
    session: SessionDep,
    carrera_id: Annotated[int, Path(description="El ID de la carrera")],
    nombre_caballo: Annotated[str, Path(description="El nombre del caballo")],
    current_user: Apostador = Depends(get_current_user),
):
    if not current_user.es_admin:
        raise UsuarioNoAdministradorException(
            "No tienes permisos para agregar un caballo a una carrera"
        )
    carrera_repository = CarreraRepository(session)
    carrera_service = CarreraService(carrera_repository)
    carrera = carrera_service.obtener_carrera_por_id(carrera_id)

    caballo_repository = CaballoRepository(session)
    caballo_service = CaballoService(caballo_repository)
    caballo = caballo_service.obtener_caballo(nombre_caballo)

    return CarreraConCaballosDTO(
        carrera_service.agregar_caballo(carrera, caballo)
    )


@router.put(
    "/empezar/{carrera_id}",
    response_model=CarreraConCaballoGanadorDTO,
    status_code=status.HTTP_200_OK
)
def empezar_carrera(
    session: SessionDep,
    carrera_id: Annotated[int, Path(description="El ID de la carrera")],
    current_user: Apostador = Depends(get_current_user),
):
    if not current_user.es_admin:
        raise UsuarioNoAdministradorException(
            "No tienes permisos para empezar una carrera"
        )
    carrera_repository = CarreraRepository(session)
    carrera_service = CarreraService(carrera_repository)
    carrera = carrera_service.obtener_carrera_por_id(carrera_id)
    return CarreraConCaballoGanadorDTO(carrera_service.empezar_carrera(carrera))

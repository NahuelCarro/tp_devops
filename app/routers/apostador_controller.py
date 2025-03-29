import bcrypt
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status

from app.database import SessionDep
from app.models.apostador import Apostador
from app.schemas.apuesta_dto import ApuestaDTO, ApuestaCreacionDTO
from app.services.apostador_service import ApostadorService
from app.auth.auth import create_access_token, get_current_user
from app.repository.apostador_repository import ApostadorRepository
from app.schemas.apostador_dto import ApostadorRegistroDTO, ApostadorDTO
from app.exceptions import EmailOClaveIncorrectaException

router = APIRouter(prefix="/apostador")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post(
    "/registrar",
    response_model=ApostadorDTO,
    status_code=status.HTTP_201_CREATED
)
def registrar_apostador(
    session: SessionDep, apostador: ApostadorRegistroDTO
) -> ApostadorDTO:
    aporador_repository = ApostadorRepository(session)
    apostador_service = ApostadorService(aporador_repository)
    clave = bcrypt.hashpw(apostador.clave.encode("utf-8"), bcrypt.gensalt())
    return ApostadorDTO(
        apostador_service.crear_apostador(
            apostador.nombre, apostador.mail, clave, apostador.es_admin
        )
    )


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    apostador_repository = ApostadorRepository(session)
    apostador_service = ApostadorService(apostador_repository)
    apostador = apostador_service.obtener_apostador(form_data.username)
    if not apostador:
        raise EmailOClaveIncorrectaException()
    is_psw_valid = bcrypt.checkpw(
        form_data.password.encode("utf-8"),
        apostador.clave
    )
    if not is_psw_valid:
        raise EmailOClaveIncorrectaException()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": apostador.mail}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/perfil",
    response_model=ApostadorDTO,
    status_code=status.HTTP_200_OK
)
def perfil_apostador(
    current_user: Apostador = Depends(get_current_user)
) -> ApostadorDTO:
    return ApostadorDTO(current_user)


@router.post(
    "/apostar/{carrera_id}/{nombre_caballo}",
    response_model=ApuestaDTO,
    status_code=status.HTTP_201_CREATED
)
def apostar(
    session: SessionDep,
    carrera_id: int,
    nombre_caballo: str,
    apuesta_creacion: ApuestaCreacionDTO,
    current_user: Apostador = Depends(get_current_user),
):
    apostador_repository = ApostadorRepository(session)
    apostador_service = ApostadorService(apostador_repository)
    return ApuestaDTO(
        apostador_service.apostar(
            current_user.mail,
            carrera_id,
            nombre_caballo,
            apuesta_creacion.monto
        )
    )

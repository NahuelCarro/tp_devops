from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from app.schemas.apuesta_dto import ApuestaDTO
from app.models.apostador import Apostador


class ApostadorBase(SQLModel):
    nombre: str = Field(
        default=None, min_length=1, description="El nombre no debe estar vacío"
    )
    mail: EmailStr = Field(
        ...,
        description="El mail debe contener un arroba y tener un formato válido",
    )


class ApostadorDTO(ApostadorBase):
    balance_apuestas: float
    apuestas: list[ApuestaDTO]

    def __init__(self, apostador: Apostador):
        self.nombre = apostador.nombre
        self.mail = apostador.mail
        self.balance_apuestas = apostador.balance_apuestas
        self.apuestas = [ApuestaDTO(apuesta) for apuesta in apostador.apuestas]


class ApostadorRegistroDTO(ApostadorBase):
    clave: str = Field(
        default=None,
        min_length=8,
        description="La clave debe tener al menos 8 caracteres",
    )
    es_admin: bool = False

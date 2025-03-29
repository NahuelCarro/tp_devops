from sqlmodel import SQLModel, Field
from typing import Optional


class CarreraCaballoLink(SQLModel, table=True):
    carrera_id: Optional[int] = Field(
        nullable=False, primary_key=True, foreign_key="carrera.id"
    )
    caballo_id: Optional[int] = Field(
        nullable=False, primary_key=True, foreign_key="caballo.id"
    )
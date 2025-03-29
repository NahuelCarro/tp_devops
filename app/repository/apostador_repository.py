from typing import Optional
from sqlmodel import select
from app.models.apostador import Apostador
from .base_repository import BaseRepository


class ApostadorRepository(BaseRepository):
    def obtener_por_mail(self, mail: str) -> Optional[Apostador]:
        statement = select(Apostador).where(Apostador.mail == mail)
        return self.session.exec(statement).first()

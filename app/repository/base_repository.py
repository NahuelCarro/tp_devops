from sqlmodel import SQLModel
from app.database import SessionDep


class BaseRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def guardar(self, model: SQLModel):
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

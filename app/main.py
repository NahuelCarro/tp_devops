from fastapi import FastAPI
from app.routers import apostador_controller, carrera_controller
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables, get_session
from app.services.caballo_service import CaballoService
from app.repository.caballo_repository import CaballoRepository

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las origins en desarrollo
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los headers
)

create_db_and_tables()
app.include_router(apostador_controller.router)
app.include_router(carrera_controller.router)

@app.on_event("startup")
def crear_caballos_iniciales():
    session = next(get_session())
    try:
        caballo_repo = CaballoRepository(session)
        caballo_service = CaballoService(caballo_repo)

        caballos_iniciales = [
            ("Relampago", 450.5),
            ("Tormenta", 480.0),
            ("Fuego", 490.0),
            ("Trueno", 500.0),
            ("Rafaga", 510.0),
            ("Viento", 520.0),
        ]

        for nombre, peso in caballos_iniciales:
            try:
                print(f"Creando caballo {nombre}...")
                caballo_service.crear_caballo(nombre, peso)
                print(f"Caballo {nombre} creado exitosamente.")
            except HTTPException:
                print(f"El caballo {nombre} ya existe. Saltando...")
                session.rollback()

        session.commit()
    except Exception as e:
        print(f"Error al crear caballos iniciales: {e}")
        session.rollback()
    finally:
        session.close()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

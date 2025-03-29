import time
from datetime import datetime, timedelta
from sqlmodel import Session
from fastapi.testclient import TestClient

from app.models.caballo import Caballo
from app.models.carrera import Carrera


def registro_apostador(client: TestClient, nombre: str, mail: str, clave: str, es_admin: bool):
    registro_data = {
        "nombre": nombre,
        "mail": mail,
        "clave": clave,
        "es_admin": es_admin,
    }
    response = client.post("/apostador/registrar", json=registro_data)
    return response


def login_apostador(client: TestClient, mail: str, clave: str):
    login_data = {
        "username": mail,
        "password": clave
    }
    response = client.post("/apostador/login", data=login_data)
    return response


def registro_y_login_correctos(
    client: TestClient,
    nombre: str,
    mail: str,
    clave: str,
    es_admin: bool
):
    response = registro_apostador(client, nombre, mail, clave, es_admin)
    assert response.status_code == 201

    response_login = login_apostador(client, mail, clave)
    assert response_login.status_code == 200

    return response_login.json()["access_token"]


def test_login_con_contrasena_incorrecta(client: TestClient):
    response = login_apostador(client, "juan@example.com", "incorrect_password")
    assert response.status_code == 401
    assert response.json()["detail"] == 'Email o contraseña incorrectos'


def test_ver_perfil_sin_login(client: TestClient):
    response = client.get("/apostador/perfil")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_apostar_con_monto_menor_a_cero(session: Session, client: TestClient):
    access_token = registro_y_login_correctos(
        client,
        "Pepe",
        "pepe@example.com",
        "password",
        es_admin=True
    )

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post(
        "/carrera/crear",
        json={"fecha": str(datetime.now() + timedelta(seconds=1))},
        headers=headers
        )
    assert response.status_code == 201

    caballo = Caballo(nombre="Relampago", peso=500.0)
    session.add(caballo)
    session.commit()
    session.refresh(caballo)

    # Intentar realizar una apuesta con monto menor a 0
    apuesta_creacion = {"monto": -50.0}
    response = client.post(
        f"/apostador/apostar/1/{caballo.nombre}",
        json=apuesta_creacion,
        headers=headers
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "El monto no puede ser negativo"


def test_apostar_con_carrera_iniciada(session: Session, client: TestClient):
    access_token = registro_y_login_correctos(
        client,
        "Pepe",
        "pepe@example.com",
        "password",
        es_admin=True
    )
    headers = {"Authorization": f"Bearer {access_token}"}

    # Se crea carrera ya iniciada
    carrera = Carrera(fecha=datetime.now() - timedelta(seconds=1))
    caballo = Caballo(nombre="Relampago", peso=500.0)
    session.add(carrera)
    session.add(caballo)
    session.commit()
    session.refresh(carrera)
    session.refresh(caballo)

    # Se intenta realizar una apuesta
    apuesta_creacion = {"monto": 50.0}
    response = client.post(
        f"/apostador/apostar/{carrera.id}/{caballo.nombre}",
        json=apuesta_creacion,
        headers=headers
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "La carrera ya ha iniciado"


def test_agregar_caballo_sin_ser_admin(session: Session, client: TestClient):
    access_token = registro_y_login_correctos(
        client,
        "Pepe",
        "pepe@example.com",
        "password",
        es_admin=False
    )
    headers = {"Authorization": f"Bearer {access_token}"}

    carrera = Carrera(fecha=datetime.now() + timedelta(seconds=1))
    session.add(carrera)
    session.commit()
    session.refresh(carrera)

    caballo = Caballo(nombre="Relampago", peso=500.0)
    response = client.put(
        f"/carrera/agregar_caballo/{carrera.id}/{caballo.nombre}",
        headers=headers
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "No tienes permisos para agregar un caballo a una carrera"


def test_iniciar_carrera_y_no_es_la_fecha(session: Session, client: TestClient):
    access_token = registro_y_login_correctos(
        client,
        "Pepe",
        "pepe@example.com",
        "password",
        es_admin=True
    )
    headers = {"Authorization": f"Bearer {access_token}"}

    carrera = Carrera(fecha=datetime.now() + timedelta(minutes=10))
    session.add(carrera)
    session.commit()
    session.refresh(carrera)

    # Se intenta iniciar una carrera antes de la fecha programada
    response = client.put(f"/carrera/empezar/{carrera.id}", headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "La carrera no puede iniciarse antes de la fecha programada"


def test_inscribir_caballo():
    carrera = Carrera(fecha=datetime.now())
    caballo = Caballo(nombre="Trueno", peso=500.0)

    caballo.inscribir(carrera)

    assert caballo in carrera.caballos, "El caballo no está en la carrera"
    assert carrera in caballo.carreras, "La carrera no está en el caballo"


def test_listar_carreras(session: Session, client: TestClient):
    carrera1 = Carrera(fecha=datetime(2025, 12, 1))
    carrera2 = Carrera(fecha=datetime(2025, 12, 2))

    caballo1 = Caballo(nombre="Relampago", peso=500.0)
    caballo2 = Caballo(nombre="Trueno", peso=480.0)
    caballo3 = Caballo(nombre="Tormenta", peso=495.0)

    # Se asignan caballos a carreras
    carrera1.caballos.append(caballo1)
    carrera1.caballos.append(caballo2)

    carrera2.caballos.append(caballo3)

    session.add(carrera1)
    session.add(carrera2)
    session.add(caballo1)
    session.add(caballo2)
    session.add(caballo3)
    session.commit()
    session.refresh(carrera1)
    session.refresh(carrera2)
    session.refresh(caballo1)
    session.refresh(caballo2)
    session.refresh(caballo3)

    response = client.get("/carrera/listar")

    assert (
        response.status_code == 200
    ), f"Se esperaba status 200, pero se obtuvo {response.status_code}"

    carreras_list = response.json()
    assert isinstance(carreras_list, list), "Se esperaba una lista de carreras."
    assert (
        len(carreras_list) == 2
    ), f"Se esperaban 2 carreras, pero se obtuvieron {len(carreras_list)}."

    # Verificar detalles de la primera carrera
    carrera1_response = carreras_list[0]

    assert carrera1_response is not None, "Carrera 1 no encontrada en la respuesta."
    assert (
        carrera1_response["fecha"] == "2025-12-01T00:00:00"
    ), "Fecha de la Carrera 1 no coincide."
    assert (
        len(carrera1_response["caballos"]) == 2
    ), "Se esperaban 2 caballos en Carrera 1."
    nombres_caballos_carrera1 = {
        caballo["nombre"] for caballo in carrera1_response["caballos"]
    }
    assert nombres_caballos_carrera1 == {
        "Relampago",
        "Trueno",
    }, "Los nombres de los caballos en Carrera 1 no coinciden."
    assert (
        carrera1_response["caballos"][0]["porcentaje_de_pago"] == 2.1
    ), "El porcentaje de pago del caballo 1 en Carrera 1 no coincide."
    assert (
        carrera1_response["caballos"][1]["porcentaje_de_pago"] == 2.1
    ), "El porcentaje de pago del caballo 2 en Carrera 1 no coincide."

    # Verificar detalles de la segunda carrera
    carrera2_response = carreras_list[1]
    assert carrera2_response is not None, "Carrera 2 no encontrada en la respuesta."
    assert (
        carrera2_response["fecha"] == "2025-12-02T00:00:00"
    ), "Fecha de la Carrera 2 no coincide."
    assert (
        len(carrera2_response["caballos"]) == 1
    ), "Se esperaba 1 caballo en Carrera 2."
    nombres_caballos_carrera2 = {
        caballo["nombre"] for caballo in carrera2_response["caballos"]
    }
    assert nombres_caballos_carrera2 == {
        "Tormenta"
    }, "El nombre del caballo en Carrera 2 no coincide."


def test_del_sistema(session: Session, client: TestClient):
    # 1. Se registra un nuevo apostador
    registro_data = {
        "nombre": "Juan",
        "mail": "juan@example.com",
        "clave": "secure_password",
        "es_admin": True,
    }
    response = client.post("/apostador/registrar", json=registro_data)
    assert response.status_code == 201
    apostador_response = response.json()
    assert (
        apostador_response["nombre"] == "Juan"
    ), "El nombre del apostador no coincide"
    assert (
        apostador_response["mail"] == "juan@example.com"
    ), "El mail del apostador no coincide"

    # 2. Se hace el login para obtener el token de acceso
    login_data = {"username": "juan@example.com", "password": "secure_password"}
    response = client.post("/apostador/login", data=login_data)
    assert response.status_code == 200
    token_response = response.json()
    assert "access_token" in token_response, "No se obtuvo un token de acceso"
    access_token = token_response["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Se crea una carrera y un caballo
    carrera = Carrera(fecha=datetime.now() + timedelta(seconds=1))
    session.add(carrera)
    session.commit()
    session.refresh(carrera)

    caballo = Caballo(nombre="Relampago", peso=500.0)
    session.add(caballo)
    session.commit()
    session.refresh(caballo)

    # 4. Se agrega el caballo a la carrera
    response = client.put(
        f"/carrera/agregar_caballo/{carrera.id}/{caballo.nombre}", headers=headers
    )
    assert response.status_code == 200, "No se pudo agregar el caballo a la carrera"

    # 5. Se realiza una apuesta a la carrera 1
    apuesta_creacion = {"monto": 50.0}
    response = client.post(
        f"/apostador/apostar/{carrera.id}/{caballo.nombre}",
        json=apuesta_creacion,
        headers=headers,
    )
    assert response.status_code == 201, "No se pudo realizar la apuesta"
    apuesta_response = response.json()
    assert apuesta_response["monto"] == 50.0, "El monto de la apuesta no coincide"
    assert (
        apuesta_response["carrera_id"] == carrera.id
    ), "El ID de la carrera no coincide"
    assert (
        apuesta_response["caballo_nombre"] == caballo.nombre
    ), "El nombre del caballo no coincide"

    # Se espera un segundo para que haya llegado la hora de empezar la carrera
    time.sleep(1)

    # 6. Empezar la carrera
    response = client.put(f"/carrera/empezar/{carrera.id}", headers=headers)

    response_perfil = client.get("/apostador/perfil", headers=headers)
    apostador_perfil = response_perfil.json()

    assert response.status_code == 200, "No se pudo empezar la carrera"
    assert carrera.caballo_ganador_id == caballo.id, "El caballo ganador no coincide"
    assert (
        apostador_perfil["balance_apuestas"] == 100.0
    ), "El balance de la apuesta no coincide"

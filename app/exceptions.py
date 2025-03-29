from fastapi import HTTPException, status


class CredencialesInvalidasException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Las credenciales son inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenExpiradoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado. Por favor, inicie sesión nuevamente.",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UsuarioNoEncontradoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )


class EmailOClaveIncorrectaException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )


class EmailDuplicadoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un apostador con ese mail",
        )


class MontoApuestaInvalidoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El monto no puede ser negativo",
        )


class CarreraYaIniciadaException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La carrera ya ha iniciado",
        )


class CaballoNoInscriptoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El caballo no está inscripto en la carrera",
        )


class ApostadorYaApostoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El apostador ya ha apostado en la carrera",
        )


class LimiteOffsetNegativoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El límite o el offset no pueden ser negativos",
        )


class UsuarioNoAdministradorException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class CaballoNoEncontradoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caballo no encontrado",
        )


class CaballoDuplicadoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un caballo con ese nombre",
        )


class FechaCarreraInvalidaException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de la carrera no puede ser del pasado",
        )


class CarreraNoIniciadaException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La carrera no puede iniciarse antes de la fecha programada",
        )


class CarreraYaFinalizadaException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La carrera ya ha terminado",
        )


class CarreraNoEncontradaException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrera no encontrada",
        )

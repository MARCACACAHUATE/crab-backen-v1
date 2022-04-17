# JWT
from datetime import timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# typing
from typing import Optional

# Fast API
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Utilies
from datetime import datetime, timedelta
from db import UserConnection

from Models.Request import User


SECRET_KEY = "Arriva las chivas"
ALGORITM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Se clara el endpoint que se debe usar para obtener un token
oauth2_sheme = OAuth2PasswordBearer(tokenUrl = "token")
# Ayudante para hashear y verificar las password
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

# db config
config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": "3306",
    "database": "db_fastapi"
}


# verifica que las contraseñas sean las mismas
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Hashea la contraseña dada en hs256
def create_password_hash(password: str):
    return pwd_context.hash(password)

#
def authenticate_user(username: str, password: str):
    """ Verifica las credenciales proporcionadas.
        Si el username no existe o la password es incorrecta
        regresa un False.

        Si son correctas regresa los datos del user
    """

    db = UserConnection(**config)
    user = db.Select(f"SELECT * FROM users WHERE username='{username}'")[0]
    
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """ Crea un token de acceso """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITM)
    
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_sheme)):
    # Excepcion cuando las credenciales no son validas  
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "No se pudieron validar las credenciales",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITM])
        username: str = payload.get("sub")

        if username is None:
            raise credential_exception
    
    except JWTError:
        raise HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Token Expired",
        headers = {"WWW-Authenticate": "Bearer"}
    )

    db = UserConnection(**config)
    data = db.Select(f"SELECT * FROM users WHERE username='{username}'")[0]
    user = User(**data)

    if user is None:
        raise credential_exception

    return user

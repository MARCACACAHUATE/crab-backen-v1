"""Modulo que maneja la verificacion y el hashed de las contraseñas"""

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from db import UserConnection
from jose import jwt, JWTError

# db config
config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": "3306",
    "database": "db_fastapi"
}


# Ayudante para hashear y verificar las password
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")


# verifica que las contraseñas sean las mismas
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#
def get_password_hash(password: str):
    return pwd_context.hash(password)

# 
def authenticate_user(username: str, password: str):
    """ Verifica las credenciales proporcionadas.
        Si el username no existe o la password es incorrecta
        regresa un False.

        Si son correctas regresa los datos del user
    """

    db = UserConnection(**config)
    user = db.Select(f"SELECT * FROM user WHERE username='{username}'")
    
    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return user


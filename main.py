# FastApi
from fastapi import FastAPI, Depends, HTTPException, status
# Models
from Models.Request import User as UserRequest
from Models.Response import User as UserResponse
from Models.Response import Token
# db
from db.userconnection import UserConnection
# JWT
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from services.tokens import create_access_token, authenticate_user, create_password_hash
# Utilities
from datetime import timedelta


# dbconection
config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": "3306",
    "database": "db_fastapi"
}


app = FastAPI()

from services.tokens import oauth2_sheme


# Users endpoints
@app.post("/user", response_model = UserResponse)
def create_new_user(user: UserRequest):
    # Crea la conexion a la base de datos.
    db = UserConnection(**config)
    pwd_hashed = create_password_hash(user.password)
    # Crea el usuario en la base de datos.
    db.Insert(
            f'''INSERT INTO users (username, email, password, first_name, last_name, is_admin, is_active) 
            VALUES ("{user.username}", "{user.email}", "{pwd_hashed}", "{user.first_name}", "{user.last_name}", "{int(user.is_admin)}", "{int(user.is_active)}")'''
        )
    return user

@app.get("/user")
def get_user(token: str = Depends(oauth2_sheme)):
    db = UserConnection(**config)
    data = db.Select("SELECT * FROM users")
    return data

@app.delete("/user/{id}")
def delete_user(id: int, token: str = Depends(oauth2_sheme)):
    db = UserConnection(**config)
    db.Delete(f"DELETE FROM users WHERE id={id}")
    return "Usuario Eliminado"

@app.put("/user/{id}", response_model = UserResponse)
def update_user(id: int, user: UserRequest, token: str = Depends(oauth2_sheme)):
    db = UserConnection(**config)
    db.Update(f'UPDATE users SET username="{user.username}" WHERE id={id}')
    return user


# Endpoint para generar los tokens
@app.post("/token", response_model = Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(username = form_data.username, password = form_data.password)

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Username o password incorrecta",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes = 30)
    access_token = create_access_token(
        data = {"sub": user["username"]},
        expires_delta = access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
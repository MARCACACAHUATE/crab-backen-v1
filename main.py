# FastApi
from fastapi import FastAPI, Depends, HTTPException, status
from h11 import Data
# Models
from Models.Request import User as UserRequest, UserStatus
from Models.Response import User as UserResponse
from Models.Request import NoticiaRequest, Noticia
from Models.Response import NoticiaResponse
from Models.Response import Token
from Models.Request import Dataset
# db
from db import UserConnection, NoticiaConnect, DatasetConnection
# JWT
from fastapi.security import OAuth2PasswordRequestForm
from services.tokens import create_access_token, authenticate_user, create_password_hash, get_current_user
from services.tokens import oauth2_sheme
# Permissions
from services.permissions import (
        AdminResource, AdminPermissions,
        OwnerPermissions, OwnerResource,
        DatasetPermissions, DatasetResource, 
        get_user, get_dataset_owner
    )

# Utilities
from datetime import timedelta, datetime, date
from services.tokens import get_current_user


# dbconection
config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": "3306",
    "database": "db_fastapi"
}


app = FastAPI()


# <---- Users ---->
@app.post("/user", response_model = UserResponse, tags = ["Users"])
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


@app.delete("/user/{id}", tags = ["Users"])
def delete_user(id: int, token: str = Depends(oauth2_sheme)):
    db = UserConnection(**config)
    db.Delete(f"DELETE FROM users WHERE id={id}")
    return "Usuario Eliminado"

@app.put("/user/{id}", response_model = UserResponse, tags = ["Users"])
def update_user(id: int,
                user: UserRequest,
                owner: OwnerResource = OwnerPermissions("edit", get_user),
                token: str = Depends(oauth2_sheme)
        ):
    db = UserConnection(**config)    
    db.Update(f"""UPDATE users 
            SET username="{user.username}" 
            email="{user.email}"
            first_name="{user.first_name}"
            last_name="{user.last_name}"   
            WHERE id={id}"""
        )
    return user


# <---- Endpoint para admins ---->
@app.get("/user", tags = ["Admin"])
def get_users_list(
    token: str = Depends(oauth2_sheme),
    ilr: AdminResource = AdminPermissions("view", AdminResource),
    user = Depends(get_current_user)
    ):

    # Crea la lista de los usuarios
    db = UserConnection(**config)
    data = db.Select("SELECT * FROM users")

    return data

@app.patch("/user/status/{id}", response_model = UserStatus, tags = ["Admin"])
def change_status_user(
        id: int,
        user: UserStatus,
        permisions: AdminResource = AdminPermissions("edit", AdminResource),
        token: str = Depends(oauth2_sheme)
    ):
    db = UserConnection(**config)
    db.Update(f"UPDATE users SET is_active={int(user.is_active)} WHERE id={id}")
    return user

# <---- Noticias ---->
@app.post("/noticias", response_model = NoticiaResponse, tags = ["Noticias"])
def save_noticias(noticias: NoticiaRequest):
    cantidad_noticias = 0
    db = UserConnection(**config)
    cursor = db.conn.cursor()

    # Transaccion para que se almacenen todas las noticias
    try:
        for noticia in noticias.data:
            cursor.execute(
                f"""INSERT INTO noticias (contenido, fecha, categoria_id, pagina_id)
                    VALUES ("{noticia.contenido}", "{noticia.fecha}", "{noticia.categoria_id}", "{noticia.pagina_id}")"""
            )
            print(noticia)
            cantidad_noticias+=1
        
        db.conn.commit()
        
        return {
            "cantidad_noticias": cantidad_noticias,
            "fecha": noticias.fecha,
            "pagina": noticias.pagina,
            "mensaje": "Almacenamiento Exitoso"
        }

    except Exception as e:
        db.conn.rollback()
        print(e)
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Almacenamiento Fallido -> {e}"
        )


@app.get("/noticias/", tags = ["Noticias"])
def list_noticias(fecha: str = date.today().isoformat(), token: str = Depends(oauth2_sheme)):
    db = NoticiaConnect(**config)
    noticias = db.List_Noticias(f"""SELECT * FROM ((noticias INNER JOIN categorias ON noticias.categoria_id = categorias.id) 
    INNER JOIN paginas_noticias ON noticias.pagina_id = paginas_noticias.id)
    WHERE fecha='{fecha}'
    """)

    return {
        "total": len(noticias),
        "noticias": noticias
    }
        

@app.delete("/noticias/{id}", tags = ["Noticias"])
def delete_noticia(
    id: int,
    token: str = Depends(oauth2_sheme),
    permission: AdminResource =  AdminPermissions("edit", AdminResource)
):
    db = NoticiaConnect(**config)
    try:
        noticia = db.Select(f"SELECT * FROM noticias WHERE id={id}")[0]
        db.Delete(f"DELETE FROM noticias WHERE id={id}")
        return {
            "message": "Noticia Eliminada con exito",
            "data": noticia
        }

    except IndexError as e:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "El elemento que quiere eliminar no existe"
        )


# <---- Datasets ---->
@app.post("/data", tags = ["Datasets"])
async def create_dataset(
        dataset: Dataset, 
        token: str = Depends(oauth2_sheme), 
        user: UserRequest = Depends(get_current_user)
    ):
    try:
        db = DatasetConnection(**config)
        db.Insert(
            f"""INSERT INTO datasets (fecha_inicio, fecha_fin, usuario_id)
            VALUES ("{dataset.fecha_inicio}","{dataset.fecha_fin}", {user.id})"""
        )
        return {
            "message": f"Dataset creado para el usuario {user.username}",
            "fecha_inicio": dataset.fecha_inicio,
            "fecha_fin": dataset.fecha_fin
        }
    except Exception as e:

        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Algo fallo al realizar la operacion"
        )


@app.delete("/dataset/{id_dataset}", tags = ["Datasets"])
def delete_dataset(
        id_dataset: int, 
        token: str = Depends(oauth2_sheme),
        owner: DatasetResource = DatasetPermissions("delete", get_dataset_owner),
    ):

    db = DatasetConnection(**config)
    data = db.Delete(id = id_dataset)
    return {
        "message": "Datasets eliminado con exito",
        "data": [
            data
        ]
    }


@app.put("/dataset/{id_dataset}", tags = ["Datasets"])
def update_dataset(
    id_dataset: int,
    dataset: Dataset,
    token: str = Depends(oauth2_sheme),
    owner: DatasetResource = DatasetPermissions("edit", get_dataset_owner)
):
    db = DatasetConnection(**config)
    db.Update(f"""UPDATE datasets SET fecha_inicio="{dataset.fecha_inicio.isoformat()}", fecha_fin="{dataset.fecha_fin.isoformat()}" WHERE id={id_dataset}""")
    return {
        "message": "Dataset actualizado con exito",
        "data": [dataset]
    }


# <---- Endpoint para generar los tokens ---->
@app.post("/token", response_model = Token, tags = ["Login"])
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
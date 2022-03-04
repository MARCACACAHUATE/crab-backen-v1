# FastApi
from fastapi import FastAPI

# Models
from Models.Request import User as UserRequest
from Models.Response import User as UserResponse

# db
from db.userconnection import UserConnection

# dbconection
config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": "3306",
    "database": "db_fastapi"
}


app = FastAPI()


# Users endpoints
@app.post("/user", response_model = UserResponse)
def post_user(user: UserRequest):
    db = UserConnection(**config)
    db.Insert(f'INSERT INTO user (username, password) values ("{user.username}", "{user.password}")')
    return user

@app.get("/user")
def get_user():
    db = UserConnection(**config)
    data = db.makequery("SELECT * FROM user")
    return data

@app.delete("/user/{id}")
def delete_user(id: int):
    db = UserConnection(**config)
    db.Delete(f"DELETE FROM user WHERE id={id}")
    return "Usuario Eliminado"

@app.put("/user/{id}", response_model = UserResponse)
def update_user(id: int, user: UserRequest):
    db = UserConnection(**config)
    db.Update(f'UPDATE user SET username="{user.username}" WHERE id={id}')
    return user
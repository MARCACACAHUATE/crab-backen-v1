from pydantic import BaseModel
from db import UserConnection, DatasetConnection
from Models.Request import User
from fastapi import Depends, HTTPException, status
from services.tokens import get_current_user
from services.fastapi_permissions import (
        Allow,
        Authenticated,
        Deny,
        Everyone,
        configure_permissions,
        list_permissions
    )

config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "port": "3306",
    "database": "db_fastapi"
}

# Lisa de los permisos y lo que se puede hacer
class AdminResource:
    __acl__ = [
        (Allow, Authenticated, "view"),
        (Allow, "role:admin", "edit")
    ]

class OwnerResource(BaseModel):
    username: str

    def __acl__(self):
       return [
            (Allow, f"owner:{self.username}", "edit")
        ]

class DatasetResource(BaseModel):
    owner_id: int

    def __acl__(self):
        return [
            (Allow, f"owner:{self.owner_id}", "delete"),
            (Allow, f"owner:{self.owner_id}", "edit")
        ]


def get_user(id: int):
    db = UserConnection(**config)
    user = db.Select(f'SELECT * FROM users WHERE id={id}')[0]
    return OwnerResource(username = user["username"])


def get_dataset_owner(id_dataset: int):
    try:
        db = DatasetConnection(**config)
        data = db.Select(f"SELECT * FROM datasets WHERE id={id_dataset}")[0]
        print(data)
        return DatasetResource(owner_id = data["usuario_id"])
    except IndexError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "El dataset no existe a la verga compa"
        )


# da los permisos al usurio
def get_admin_principals(user: User = Depends(get_current_user)):
    if user.is_admin:
        principals = [Everyone, Authenticated, "role:admin"]
        principals.extend(getattr(user, "principals", []))
    else:
        principals = [Everyone]

    return principals


def get_owner_principals(user: User = Depends(get_current_user)):
    principals = [Everyone, Authenticated, f'owner:{user.username}']
    principals.extend(getattr(user, "principals", []))
    return principals


def get_dataset_principals(user: User = Depends(get_current_user)):
    principals = [Everyone, Authenticated, f'owner:{user.id}']
    principals.extend(getattr(user, "principals", []))
    return principals


# Decimos como obtenemos los permisos
AdminPermissions = configure_permissions(get_admin_principals)
OwnerPermissions = configure_permissions(get_owner_principals)
DatasetPermissions = configure_permissions(get_dataset_principals)
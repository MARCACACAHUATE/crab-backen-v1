from pydantic import BaseModel
from db import UserConnection
from Models.Request import User
from fastapi import Depends
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


def get_user(id: int):
    db = UserConnection(**config)
    user = db.Select(f'SELECT * FROM users WHERE id={id}')[0]
    return OwnerResource(username = user["username"])


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


# Decimos como obtenemos los permisos
AdminPermissions = configure_permissions(get_admin_principals)
OwnerPermissions = configure_permissions(get_owner_principals)
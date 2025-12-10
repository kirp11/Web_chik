from typing import Union, Dict

from fastapi import FastAPI, HTTPException, status

app = FastAPI()
# 2. Пользователи и их профили
#
# Данные: список пользователей.
#
#     username: str
#     email: str
#     full_name: str | None = None
#     is_active: bool = True
#
# Добавить проверку, чтобы username был уникален (если уже есть — вернуть 400).
# Добавить маршрут GET /users/by-username/{username}.

Users = [
    {
        "username": "Kirp",
        "email": "mail",
        "full_name": "Kirpian",
        "is_active": True
    },
    {
        "username": "Ivan",
        "email": "yandex",
        "full_name": "Ivan",
        "is_active": False
    },
    {
        "username": "Kris",
        "email": "gmail",
        "full_name": "Kristian",
        "is_active": True
    },
]

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(datas: Dict[str, str]):

    for user in Users:
        if user.get("username") == datas.get("username"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="is not unique")

    new_user = {
        "username": datas.get("username"),
        "email": datas.get("email"),
        "full_name": datas.get("full_name"),
        "is_active": datas.get("is_active")
    }
    Users.append(new_user)

    return new_user

@app.get("/users/by-username/{username}")
def get_user(username: str):
    for user in Users:
        if user.get("username") == username:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
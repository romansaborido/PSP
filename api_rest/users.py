from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int


users_list = [
    User(id=1, name="Roman", surname="Saborido", age=18),
    User(id=2, name="Ruben", surname="López", age=22),
    User(id=3, name="Mario", surname="Muñoz", age=19),
]


@app.get("/users")
def get_users():
    return users_list


@app.get("/users/{id_user}")
def get_users_id(id_user: int):
    user = [user for user in users_list if user.id == id_user]
    if user:
        return user
    else:
        return "{ Error : Usuario no encontrado }"


@app.post("/users", status_code=201)
def post_user(user: User):

    # Actualizamos el id
    user.id = next_Id()

    # Añadimos el usuario
    users_list.append(user)

    # Devolvemos el usuario que ha sido agregado
    return user


@app.put("/users/{id_user}")
def modify_user(id_user: int, user:User):

    # Recorremos la lista por posiciones
    for index, saved_user in enumerate(users_list):

        # Si el usuario guardado tiene el mismo id
        if saved_user.id == id_user:
            user.id = id_user
            users_list[index] = user
            return user
    raise HTTPException(status_code=401, detail="Usuario no encontrado")


@app.delete("/users/{id_user}")
def remove_user(id_user: int):
    for saved_user in users_list:
        if saved_user.id == id_user:
            users_list.remove(saved_user)
            return {}
    raise HTTPException(status_code=401, detail="Usuario no encontrado")





def next_Id():
    return max(users_list, key=lambda u: u.id).id + 1


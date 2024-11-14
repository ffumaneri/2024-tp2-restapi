from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Auto(BaseModel):
    id: int
    marca: str
    modelo: str

auto1 = Auto(id=1, marca="Ford", modelo="Mondeo")
auto2 = Auto(id=2, marca="Fiat", modelo="Uno")
auto3 = Auto(id=3, marca="Renault", modelo="Sandero")

autos = [auto1, auto2, auto3]

@app.post("/auto")
def save_post(post: Auto):
    autos.append(post)

@app.get("/auto/ALL")
def read_list():
    return autos

@app.get("/auto/{id}")
def read_item(id: int):
    for auto in autos:
        if auto.id == id:
            return {"id": auto.id, "marca": auto.marca, "modelo": auto.modelo}

@app.delete("/auto/{id}")
def delete_item(id: int):
    for auto in autos:
        if auto.id == id:
            autos.remove(auto)

@app.patch("/auto/{id}")
def update_item(id: int, nuevo_id: int):
    for auto in autos:
        if auto.id == id:
            auto.id = nuevo_id
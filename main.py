from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Auto(BaseModel):
    id: int
    marca: str
    modelo: str

@app.post("/auto")
def post_auto(auto: Auto):
    for a in Autos:
        if a["id"] == auto.id:
            return "Auto ya existe"
    Autos.append(auto.dict())
    return auto

@app.get("/auto/all")
def get_all_auto():
    return Autos

@app.get("/auto/{id}")
def get_auto_by_id(id: int):
    for auto in Autos:
        if auto["id"] == id:
            return auto
    return "Auto no encontrado"

@app.delete("/auto/{id}")
def delete_auto_by_id(id: int):
    for i, auto in enumerate(Autos):
        if auto["id"] == id:
            Autos.pop(i)
            return "Auto eliminado"
    return "Auto no encontrado"

@app.patch("/auto/{id}")
def patch_auto_by_id(id: int, auto: Auto):
    for i, a in enumerate(Autos):
        if a["id"] == id:
            Autos[i] = auto.dict()
            return auto
    return "Auto no encontrado"

Autos = [
{"id": 1, "marca":"Ford", "modelo": "Mondeo"},
{"id": 2, "marca":"Fiat", "modelo": "Uno"},
{"id": 3, "marca":"Renault", "modelo": "Sandero"},
]

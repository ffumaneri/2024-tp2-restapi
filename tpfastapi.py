from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Auto(BaseModel):
    id: int
    marca: str
    modelo: str

autos_db = [
    {"id": 1, "marca": "Ford", "modelo": "Mondeo"},
    {"id": 2, "marca": "Fiat", "modelo": "Uno"},
    {"id": 3, "marca": "Renault", "modelo": "Sandero"},
]

@app.post("/auto", response_model=Auto)
def crear_auto(auto: Auto):
    autos_db.append(auto.dict())
    return auto

@app.get("/auto/ALL", response_model=List[Auto])
def obtener_todos_autos():
    return autos_db

@app.get("/auto/{id}", response_model=Optional[Auto])
def obtener_auto(id: int):
    auto = next((auto for auto in autos_db if auto["id"] == id), None)
    if auto is None:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return auto

@app.delete("/auto/{id}")
def eliminar_auto(id: int):
    global autos_db
    autos_db = [auto for auto in autos_db if auto["id"] != id]
    return {"mensaje": "Auto eliminado"}

@app.patch("/auto/{id}", response_model=Auto)
def actualizar_auto(id: int, auto_actualizado: Auto):
    for i, auto in enumerate(autos_db):
        if auto["id"] == id:
            autos_db[i] = auto_actualizado.dict()
            return auto_actualizado
    raise HTTPException(status_code=404, detail="Auto no encontrado")

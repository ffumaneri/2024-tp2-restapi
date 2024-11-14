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
    {"id": 3, "marca": "Renault", "modelo": "Sandero"}
]

@app.post("/auto", response_model=Auto)
async def crear_auto(auto: Auto):
    for existing_auto in autos_db:
        if existing_auto["id"] == auto.id:
            raise HTTPException(status_code=400, detail="ID ya existe")
    autos_db.append(auto.dict())
    return auto

@app.get("/auto/ALL", response_model=List[Auto])
async def obtener_todos_los_autos():
    return autos_db

@app.get("/auto/{id}", response_model=Auto)
async def obtener_auto(id: int):
    for auto in autos_db:
        if auto["id"] == id:
            return auto
    raise HTTPException(status_code=404, detail="Auto no encontrado")

@app.delete("/auto/{id}")
async def eliminar_auto(id: int):
    for index, auto in enumerate(autos_db):
        if auto["id"] == id:
            del autos_db[index]
            return {"message": "Auto eliminado"}
    raise HTTPException(status_code=404, detail="Auto no encontrado")

@app.patch("/auto/{id}", response_model=Auto)
async def actualizar_auto(id: int, auto: Auto):
    for index, existing_auto in enumerate(autos_db):
        if existing_auto["id"] == id:
            autos_db[index]["marca"] = auto.marca
            autos_db[index]["modelo"] = auto.modelo
            return autos_db[index]
    raise HTTPException(status_code=404, detail="Auto no encontrado")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Auto(BaseModel):
    id: int
    marca: str
    modelo: str

# Lista de todos los autos
autos = [
    {"id": 1, "marca": "Ford", "modelo": "Mondeo"},
    {"id": 2, "marca": "Fiat", "modelo": "Uno"},
    {"id": 3, "marca": "Renault", "modelo": "Sandero"},
]

# Lista de todos los autos
@app.get("/auto/ALL", response_model=List[Auto])
def obtener_autos():
    return autos

# Obtener un auto por ID
@app.get("/auto/{auto_id}", response_model=Auto)
def obtener_auto(auto_id: int):
    for auto in autos:
        if auto["id"] == auto_id:  
            return auto
    raise HTTPException(status_code=404, detail="Auto no encontrado.")

# Crear un nuevo auto
@app.post("/auto", response_model=Auto)
def crear_auto(auto: Auto):
    for auto_db in autos:
        if auto_db["id"] == auto.id:
            raise HTTPException(status_code=400, detail="El auto ya existe.")
    autos.append(auto.dict())  
    return auto

# Para actualizar un auto por ID
@app.put("/auto/{auto_id}", response_model=Auto)
def actualizar_auto(auto_id: int, auto_actualizado: Auto):
    for index, auto in enumerate(autos):
        if auto["id"] == auto_id: 
            autos[index] = auto_actualizado.dict() 
            return auto_actualizado
    raise HTTPException(status_code=404, detail="Auto no encontrado.")

# Para eliminar un auto por ID
@app.delete("/auto/{auto_id}", response_model=Auto)
def eliminar_auto(auto_id: int):
    for index, auto in enumerate(autos):
        if auto["id"] == auto_id: 
            return autos.pop(index)
    raise HTTPException(status_code=404, detail="Auto no encontrado.")

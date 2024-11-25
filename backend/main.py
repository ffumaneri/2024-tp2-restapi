from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],  
    allow_headers=["*"],  
)
# Base de datos en memoria
autos = [
    {"id": 1, "marca": "Ford", "modelo": "Mondeo"},
    {"id": 2, "marca": "Fiat", "modelo": "Uno"},
    {"id": 3, "marca": "Renault", "modelo": "Sandero"},
]

# Modelo de datos
class Auto(BaseModel):
    id: int
    marca: str
    modelo: str

# Crear un auto
@app.post("/auto", response_model=Auto)
def crear_auto(auto: Auto):
    for a in autos:
        if a["id"] == auto.id:
            raise HTTPException(status_code=400, detail="El ID ya existe")
    autos.append(auto.dict())
    return auto

# Obtener todos los autos
@app.get("/auto/ALL", response_model=List[Auto])
def obtener_autos():
    return autos

# Obtener un auto por ID
@app.get("/auto/{id}", response_model=Auto)
def obtener_auto(id: int):
    auto = next((a for a in autos if a["id"] == id), None)
    if auto is None:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return auto

# Actualizar un auto por ID
@app.patch("/auto/{id}", response_model=Auto)
def actualizar_auto(id: int, auto: Auto):
    for index, a in enumerate(autos):
        if a["id"] == id:
            autos[index] = auto.dict()
            return auto
    raise HTTPException(status_code=404, detail="Auto no encontrado")

# Eliminar un auto por ID
@app.delete("/auto/{id}")
def eliminar_auto(id: int):
    global autos
    autos = [a for a in autos if a["id"] != id]
    return {"detail": f"Auto con ID {id} eliminado"}

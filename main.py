from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Auto(BaseModel):
        id: int
        marca: str
        modelo: str

Autos = [
    {"id": 0, "marca": "Ford", "modelo": "Mondeo"},
    {"id": 1, "marca": "Fiat", "modelo": "Uno"},
    {"id": 2, "marca": "Renault", "modelo": "Sandero"},
]

@app.get("/autos", response_model=List[Auto])
def getAutos():
    return Autos
    
@app.get("/auto/{id}", response_model=Auto)
def getAuto(id: int):
    for auto in Autos:
        if auto["id"] == id:
            return auto
    raise HTTPException(status_code=404, detail="No existe auto con ese id")

@app.post("/auto")
def post_auto(a: Auto):
    if any(auto["id"] == a.id for auto in Autos):
        raise HTTPException (status_code=400, detail="Id ya existe")
    Autos.append(a.model_dump())
    return a

@app.patch("/auto/{id}", response_model=Auto)
def patch_auto(id: int, nuevoAuto: Auto):
    for auto in Autos:
        if auto["id"] == id:
            auto["marca"] = nuevoAuto.marca
            auto["modelo"] = nuevoAuto.modelo
            return auto
    raise HTTPException(status_code=404, detail="Auto no encontrado")

@app.delete("/auto/{id}", response_model=dict)
def delete_auto(id: int):
    index = 0
    for auto in Autos:
        if auto["id"] == id:
            Autos.pop(index)
            return {"message": "Eliminado correctamente"}
        index += 1
    raise HTTPException(status_code=404, detail="No existe ese Id")
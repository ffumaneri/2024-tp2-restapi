from typing import Union, List
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

@app.get("/")
def read_root():
    return {"TP 2: Funcionando"}

@app.get("/auto/all", response_model=List[Auto])
def get_auto():
    return Autos
    
@app.get("/auto/{id}", response_model=Auto)
def get_auto(id: int):
    for auto in Autos:
        if auto["id"] == id:
            return auto
    raise HTTPException(status_code=404, detail="No existe un auto con este número de identificación")

@app.post("/auto")
def post_auto(a: Auto):
    if any(auto["id"] == a.id for auto in Autos):
        raise HTTPException (status_code=400, detail="Ya existe un auto con este id")
    Autos.append(a.dict())
    return a

@app.patch("/auto/{id}", response_model=Auto)
def patch_auto(id: int, auto_actualizado: Auto):
    for auto in Autos:
        if auto["id"] == id:
            auto["marca"] = auto_actualizado.marca
            auto["modelo"] = auto_actualizado.modelo
            return auto
    raise HTTPException(status_code=404, detail="No existe un auto con este número de identificación")

@app.delete("/auto/{id}", response_model=dict)
def delete_auto(id: int):
    index = 0
    for auto in Autos:
        if auto["id"] == id:
            Autos.pop(index)
            return {"detail": "Auto eliminado correctamente"}
        index += 1
    raise HTTPException(status_code=404, detail="No existe un auto con este número de identificación")
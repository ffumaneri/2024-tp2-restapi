from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List


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

@app.get("/")
def home():
    return {"message": "funciona"}

@app.get("/auto/all", response_model=List[Auto])
def get_autos():
    return autos_db

@app.get("/auto/{id}", response_model=Auto)
def get_auto(id: int):
    return next((auto for auto in autos_db if auto["id"] == id), None)


@app.post("/auto", response_model=Auto)
def create_auto(auto: Auto):
    for auto_db in autos_db:
        if auto_db["marca"] == auto.marca and auto_db["modelo"] == auto.modelo:
            raise HTTPException(status_code=400, detail="El auto ya existe")
    autos_db.append(auto.model_dump())
    return auto

@app.patch("/auto/{id}", response_model=Auto)
def update_auto(id: int, auto: Auto):
    for i, auto_db in enumerate(autos_db):
        if auto_db["id"] == id:
            autos_db[i] = auto.model_dump()
            return auto  # Retorna el auto actualizado
    # Si no se encuentra el auto, lanza una excepción
    raise HTTPException(status_code=404, detail="Auto no encontrado")
    

@app.delete("/auto/{id}", response_model=Auto)
def delete_auto(id: int):
    for i, auto_db in enumerate(autos_db):
        if auto_db["id"] == id:
            del autos_db[i]
            return auto_db
    return None

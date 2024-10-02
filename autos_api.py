from typing import Annotated, List
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field


app = FastAPI(
    title='Autos API',
    description='TP2 - API de Autos',
    version="1.0",
)

# Definición de modelos 
class AutoSinId(BaseModel):
    marca: Annotated [str, Field(..., description='Marca del auto', max_length=50)]
    modelo: Annotated [str, Field(..., description='Modelo del auto', max_length=50)]

class Auto(AutoSinId):
    id: Annotated [int, Field(gt=0, description='ID del auto', default_factory=lambda: len(ListaAutos) + 1)]

# Lista de autos
ListaAutos = [Auto(id=1, marca="Ford", modelo="Mondeo"),
              Auto(id=2, marca="Fiat", modelo="Uno"),
              Auto(id=3, marca="Renault", modelo="Sandero"),
              Auto(id=4, marca="Chevrolet", modelo="Corsa")]

# Funciones auxiliares - Buscar auto por ID

def buscar_auto(id):
    idx, au = next(((idx, au) for idx, au in enumerate(ListaAutos) if au.id == id), (None, None))
    if au is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auto no encontrado")
    return idx, au

# Fin de funciones auxiliares

@app.get("/")
def read_root():
    return {"TP2": "API de Autos"}

# CRUD de autos

# CREATE
@app.post("/auto", response_model=Auto)
def add_auto(auto: AutoSinId):
    a = Auto(id=len(ListaAutos) + 1, marca=auto.marca, modelo=auto.modelo)
    ListaAutos.append(a)
    return a

# READ
@app.get("/auto/all", response_model=List[Auto]) 
def get_all_autos():
    return ListaAutos

@app.get("/auto/{id}", response_model=Auto)
def get_auto(id: int):
    idx, a = buscar_auto(id)
    return a

# UPDATE
@app.patch("/auto/{id}", response_model=Auto)
def update_auto(id: int, auto: AutoSinId):
    idx, a = buscar_auto(id)
    ListaAutos[idx] = Auto(id=a.id, marca=auto.marca, modelo=auto.modelo)
    return ListaAutos[idx]

# DELETE
@app.delete("/auto/{id}", response_model=Auto)
def delete_auto(id: int):
    idx, auto = buscar_auto(id)
    ListaAutos.remove(auto)
    return Response(status_code=status.HTTP_204_NO_CONTENT)




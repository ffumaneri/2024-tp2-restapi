from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Dict



app=FastAPI()

class Auto(BaseModel):
    id:int
    marca:str
    modelo:str


lista_autos: Dict[int,Auto] = {}

#Creo el auto.
@app.post("/auto",response_model=Auto)
def crear_auto(auto:Auto):
    if(auto.id in lista_autos):
        raise HTTPException(status_code=400,detail="El auto ya esta en la lista.")
    lista_autos[auto.id]=auto
    return auto

#Devuelvo todos los autos que estan en la lista.
@app.get("/auto/ALL",response_model=Dict[int,Auto])
def getAllAutos():
    return lista_autos

#Devolvemos un auto por su id.
@app.get("/auto/{ID}",response_model=Auto)
def getAutoID(auto_id:int):
    auto = lista_autos.get(auto_id)

    if (auto is None):
        raise HTTPException(status_code=404,detail="Auto no encontrado.")
    return auto

#Eliminamos un auto por su id.
@app.delete("/auto/{ID}")
def eliminarAutoID(auto_id:int):
    
    if(auto_id not in lista_autos):
        raise HTTPException(status_code=404,detail="Auto no encontrado.")
    del lista_autos[auto_id]
    return {"message":"Auto eliminado."}

@app.patch("/auto/{ID}", response_model=Auto)
def actualizar_auto(auto_id:int,auto:Auto):
    auto_almacenado = lista_autos.get(auto_id)

    if (auto_almacenado is None):
        raise HTTPException(status_code=404,detail="Auto no encontrado.")
    
    
    actualizar_info_auto = auto.model_dump(exclude_unset=True)
    auto_almacenado = auto_almacenado.model_copy(update=actualizar_info_auto)
    lista_autos[auto.id]=auto_almacenado
    return auto_almacenado


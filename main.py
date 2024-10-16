
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Auto(BaseModel):
    id: int
    marca: str
    modelo: str

autos = [
{"id": 1, "marca":"Ford", "modelo": "Mondeo"},
{"id": 2, "marca":"Fiat", "modelo": "Uno"},
{"id": 3, "marca":"Renault", "modelo": "Sandero"},
]

#obtiene todos los autos
@app.get("/auto/all", response_model=List[Auto],summary="devuelve una lista con todos los autos en el sistema",tags=["Autos"])
def get_all_autos():
    return autos

#recupera un auto segun ID
@app.get("/auto/{id}", response_model=Auto,summary="Recupera el auto segun la ID ingresada",tags=["Autos"])
async def Obtener_auto(id: int):

    auto = next((auto for auto in autos if auto["id"] == id), None)

    if auto:
        return auto
    else:
        raise HTTPException(status_code=404, detail=f"Auto con id: {id} no encontrados")

#almacena un nuevo auto
@app.post("/auto",summary="almacena un auto nuevo",tags=["Autos"])
def Guardar_Auto(marca:str, modelo:str):
    
    if len(autos) == 0:
        id = 1  # Si está vacía, el primer ID será 1
    else:
        id = autos[-1]["id"] +1

    autos.append(Auto(id=id,marca=marca,modelo=modelo).model_dump())

#actualiza un auto existente
@app.patch("/auto/{id}",response_model=dict, summary="Actualizar un auto por ID", description="Actualiza los detalles de un auto existente.",tags=["Autos"])
def Actualizar_Auto(id: int, unAuto: Auto):

    auto = next((auto for auto in autos if auto["id"] == id), None)

    if auto:
        auto["marca"] = unAuto.marca
        auto["modelo"] = unAuto.modelo
        return {"mensaje": f"Se actualizo el elemento con id {id} - Modelo: { unAuto.modelo}"}
    else:
        raise HTTPException(status_code=404, detail="Auto no encontrado")  

#elimina un auto
@app.delete("/auto/{id}", response_model=dict,summary="elimina un auto por ID", description="elimina los detalles de un auto existente segun una id" ,tags=["Autos"])
def Eliminar_Auto(id:int):

    auto = next((auto for auto in autos if auto["id"] == id), None)

    if auto:
        autos.remove(auto)
        return {"mensaje": f"Se Elimino el elemento con id {id} "}
    else:
        raise HTTPException(status_code=404, detail="Auto no encontrado")

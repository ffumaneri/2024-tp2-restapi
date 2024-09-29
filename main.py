from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

app=FastAPI()

#Para PATCH
class AutoSinId(BaseModel):
    marca: Optional[str]=None
    modelo: Optional[str]=None

class Auto(AutoSinId):
    id: int


autos = [
    {"id":1,
    "marca":"Toyota",
    "modelo":"Hilux"},
    {"id":2,
    "marca":"Volkswagen",
    "modelo":"Bora"}
]



@app.post("/auto")
def agregarAuto(nuevoAuto:Auto):
    autos.append(nuevoAuto)
    return{"mesage":"Auto agregado","Nuevo auto":nuevoAuto}




@app.get("/auto/{id}")
def getAuto(idAuto: int):
    buscado = None
    
    for x in autos:
        if x["id"] == idAuto:
            buscado = x
            break

    if not buscado:
        raise HTTPException(400, detail="id no encontrado")
    
    return buscado





@app.get("/autos/",response_model=list[Auto])
def getAllAutos():
    return [Auto(**auto) for auto in autos]



@app.delete("/auto/{id}")
def deleteAuto(autoId: int):
    buscado=None
    for x in autos:
            if x["id"] == autoId:
                buscado = x
                break
    
    if not buscado:
        raise HTTPException(400,detail="id no encontrado")
    autos.remove(buscado)
    return {"mensaje": "Auto eliminado", "auto": buscado}




@app.patch("/auto/{id}", response_model=AutoSinId)
def actualizarAuto(idAuto:int,autoAct:AutoSinId):
    for auto in autos:
        if auto["id"]==idAuto:
            auto["modelo"] = autoAct.modelo
            auto["marca"] = autoAct.marca
            return {"mensaje": "Auto actualizado"}
    raise HTTPException(400, detail="id no encontrado")


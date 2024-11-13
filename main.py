from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


class Auto(BaseModel):
    id: int
    marca: str
    modelo: str


autos_db: List[Auto] = [
    {"id": 1, "marca": "Ford", "modelo": "Mondeo"},
    {"id": 2, "marca": "Fiat", "modelo": "Uno"},
    {"id": 3, "marca": "Renault", "modelo": "Sandero"},
]

@app.post("/auto")
async def crear_auto(auto: Auto): 
    for item in autos_db:
        if item.id == auto.id:
            raise HTTPException(status_code=400, detail="El auto con ese ID ya existe.")
    autos_db.append(auto)
    return {"message": "Auto creado con éxito", "auto": auto}
    
#Para todos los autos
@app.get("/auto/ALL")
def obtener_todos_autos():
    return autos_db

#Con ID
@app.get("/auto/{id}")
async def obtener_auto_por_id(id: int):
   for auto in autos_db:
        if auto.id == id:
            return auto
        raise HTTPException(status_code=404, detail="Auto no encontrado.")





@app.delete("/auto/{id}")
async def eliminar_auto(id: int):
    for auto in autos_db:
        if auto.id == id:
            autos_db.remove(auto)
            return{"message": "Auto eliminado"}
        raise HTTPException(status_code=400, detail="No se encontro ningún auto con ese id")


@app.patch("/auto/{id}")
async def actualizar_auto(id: int, auto_actualizado: Auto):
    for auto in autos_db:
        if auto.id == id:
            auto.marca = auto_actualizado.marca or auto.marca
            auto.modelo = auto_actualizado.modelo or auto.modelo
            return {"message": "El auto fue actualizado", "auto": auto}
    raise HTTPException(status_code=404, detail="No se encontro ningún auto con ese id")

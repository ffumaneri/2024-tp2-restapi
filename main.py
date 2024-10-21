from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
 
app = FastAPI()

class Autos(BaseModel):
    id: int
    marca: str
    modelo: str

autos = [
    {"id": 0, "marca":"Ford", "modelo": "Mondeo"},
    {"id": 1, "marca":"Fiat", "modelo": "Uno"},
    {"id": 2, "marca":"Renault", "modelo": "Sandero"},
    {"id": 3, "marca":"Audi", "modelo": "A4"},
]

@app.post("/auto", response_model=Autos)
def crear_auto(unAuto : Autos):
    for a in autos:
        if a["id"] == unAuto.id:
            raise HTTPException(status_code=400, detail="ID ya existe")
    autos.append(unAuto.dict())
    return unAuto

@app.get("/auto/ALL" , response_model=list[Autos])
def get_autos():
    return autos

@app.get("/auto/{id}", response_model= Autos)
def get_auto(id: int):
    for auto in autos:
        if auto["id"] == id:
            return auto
    raise HTTPException(status_code=404, detail=f"Auto con id: {id} no encontrado")
    

@app.delete("/auto/{id}")
def delete_auto(id: int):
    for index, auto in enumerate(autos):
        if auto["id"] == id:
            autos.pop(index)
            return {f"Auto con id {id} ha sido eliminado"}
    raise HTTPException(status_code=404, detail=f"El auto con id {id} no está en la lista")

@app.patch("/auto/{id}", response_model=Autos)
def patch_auto(id: int, unAuto: Autos):
      existe_auto = any(auto["id"] == id for auto in autos)
      if existe_auto:
           autos[id] = unAuto
           return {
                "mensaje": "El auto ha sido actualizado correctamente",
                "auto_actualizado": unAuto
            }
      else:
         raise HTTPException(status_code=404, detail="Auto no encontrado")  
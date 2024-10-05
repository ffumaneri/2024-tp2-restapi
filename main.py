from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class AutoModel(BaseModel):
    id: int
    marca: str
    modelo: str

autos = [
    {"id": 0, "marca":"Ford", "modelo": "Mondeo"},
    {"id": 1, "marca":"Fiat", "modelo": "Uno"},
    {"id": 2, "marca":"Renault", "modelo": "Sandero"},
    {"id": 3, "marca":"Audi", "modelo": "A4"},
]

@app.get("/")
async def root():
    return {"Tp2 - by @Tristan Luna"}


@app.get("/auto/ALL" , response_model=list[AutoModel])
async def get_all():
    return autos


@app.get("/auto/{id}" , response_model=AutoModel)
async def get_auto(id: int):
    existe_auto = any(auto["id"] == id for auto in autos)
    if existe_auto:
        return autos[id]
    else:
        raise HTTPException(status_code=404, detail=f"Auto con id: {id} no encontrado")
    

@app.delete("/auto/{id}")
async def delete_auto(id: int): 
    existe_auto = any(auto["id"] == id for auto in autos)
    if existe_auto: 
        autos.pop(id)
    else:
        raise HTTPException(status_code=404, detail=f"El elemento con id {id}, no está en la lista ")
   

@app.patch("/auto/{id}", response_model=AutoModel)
async def patch_auto(id: int, unAuto: AutoModel):
      existe_auto = any(auto["id"] == id for auto in autos)
      if existe_auto:
           autos[id] = unAuto
           return {"mensaje": f"Se actualizo el elemento con id {id} - Modelo: { unAuto.modelo}"}
      else:
         raise HTTPException(status_code=404, detail="Auto no encontrado")  
      
      
@app.post("/auto", response_model=AutoModel)
async def post_auto( unAuto: AutoModel):
    id = len(autos)
    autos.append({"id": id, "marca": unAuto.marca, "modelo": unAuto.modelo})
           
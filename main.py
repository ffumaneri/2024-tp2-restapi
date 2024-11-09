from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Auto(BaseModel): 
    id: int 
    marca: str 
    modelo: str

class AutoUp(BaseModel): 
    marca: Optional[str] = None 
    modelo: Optional[str] = None

autos: List[Auto] = [ 
    Auto(id=1, marca="Ford", modelo="Mondeo"), 
    Auto(id=2, marca="Fiat", modelo="Uno"), 
    Auto(id=3, marca="Renault", modelo="Sandero"),
]

@app.get("/")
def read_root():
    return {"message": "Autos!"}

@app.get("/autos/")
def read_autos():
    return autos

@app.get("/autos/{auto_id}", response_model=Auto)
def read_autos(auto_id: int):
    for a in autos:
        if a.id == auto_id:
            return a
    raise HTTPException(status_code=404, detail="Auto no encontrado")

@app.patch("/autos/{auto_id}", response_model=Auto)
def patch_autos(auto_id: int, auto: AutoUp):
    for index, a in enumerate(autos):
        if a.id == auto_id:           
            upData = auto.model_dump(exclude_unset= True)
            for k, v in upData.items():
                setattr(autos[index], k, v)
                return autos[index]
    raise HTTPException(status_code=404, detail="Auto no encontrado")    

@app.delete("/autos/{auto_id}", response_model=Auto)
def delete_autos(auto_id: int):
    for index, a in enumerate(autos):
        if a.id == auto_id:
            autoDeleted = autos.pop(index)
            return autoDeleted
    raise HTTPException(status_code=404, detail="Auto no encontrado")    

@app.post("/autos/", response_model=Auto)
def create_auto(auto: Auto):
    for a in autos:
        if a.id == auto.id:
            raise HTTPException(status_code=400, detail="ID no disponible")
    autos.append(auto)
    return {"message": "201 - El auto se agregó exitosamente!", "auto": auto}
from fastapi import FastAPI, HTTPException, status
from model import AutoBase, AutoConID

app = FastAPI()

autos = [
    {"id": 1, "marca": "Ford", "modelo": "Mondeo"},
    {"id": 2, "marca": "Fiat", "modelo": "Uno"},
    {"id": 3, "marca": "Renault", "modelo": "Sandero"},
]

@app.get("/autos", response_model=list)
async def read_autos():
    return autos

@app.get("/autos/{auto_id}")
async def read_auto(auto_id: int):
    for auto in autos:
        if auto["id"] == auto_id:
            return auto
    raise HTTPException(status_code=404, detail="No se encontró un auto con ese ID")

@app.post("/autos", status_code=status.HTTP_201_CREATED)
async def crear_auto(auto: AutoConID):
    autos.append(auto.dict())
    return {"message": "Auto creado con éxito", "auto": auto}

@app.delete("/autos/{auto_id}")
async def borrar_auto(auto_id: int):
    for auto in autos:
        if auto["id"] == auto_id:
            autos.remove(auto)
            return {"message": "Auto borrado con éxito"}
    raise HTTPException(status_code=404, detail="No se encontró un auto con ese ID")

@app.patch("/autos/{auto_id}")
async def editar_auto(auto_id: int, auto_cambiado: AutoBase):
    for auto in autos:
        if auto["id"] == auto_id:
            auto["modelo"] = auto_cambiado.modelo
            auto["marca"] = auto_cambiado.marca
            return {"message": "Auto actualizado con éxito", "auto": auto}
    raise HTTPException(status_code=404, detail="No se encontró un auto con ese ID")

			
                

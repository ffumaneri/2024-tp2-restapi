from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Auto(BaseModel):
    id: int
    marca: str
    modelo: str

autos_database = [
    {"id": 1, "marca": "Ford", "modelo": "Mondeo"},
    {"id": 2, "marca": "Fiat", "modelo": "Uno"},
    {"id": 3, "marca": "Renault", "modelo": "Sandero"},
]

@app.post("/auto")
async def crear_auto(auto: Auto):
    for item in autos_database:
        if item["id"] == auto.id:
            raise HTTPException(status_code=400, detail="El auto con ese ID ya existe.")
    autos_database.append(auto.model_dump())
    return {"message": "Auto creado con éxito", "auto": auto}

@app.get("/auto/ALL")
async def obtener_todos_autos():
    return autos_database

@app.get("/auto/{id}")
async def obtener_auto(id: int):
    for auto in autos_database:
        if auto["id"] == id:
            return auto
    raise HTTPException(status_code=404, detail="Auto no encontrado.")

@app.delete("/auto/{id}")
async def eliminar_auto(id: int):
    for auto in autos_database:
        if auto["id"] == id:
            autos_database.remove(auto)
            return {"message": "Auto eliminado con éxito."}
    raise HTTPException(status_code=404, detail="Auto no encontrado.")

@app.patch("/auto/{id}")
async def actualizar_auto(id: int, auto_actualizado: Auto):
    for index, auto in enumerate(autos_database):
        if auto["id"] == id:
            autos_database[index] = auto_actualizado.model_dump()
            return {"message": "Auto actualizado con éxito.", "auto": auto_actualizado}
    raise HTTPException(status_code=404, detail="Auto no encontrado.")
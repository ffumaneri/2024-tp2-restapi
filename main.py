from typing import Union

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()


class Auto(BaseModel):
    id: int
    marca: str
    modelo: str

autos = [
    {"id": 1, "marca":"Ford", "modelo": "Mondeo"},
    {"id": 2, "marca":"Fiat", "modelo": "Uno"},
    {"id": 3, "marca":"Ferrari", "modelo": "296 GTS"},
    {"id": 4, "marca":"Toyota", "modelo": "Hilux"},
    {"id": 5, "marca":"Subaru ", "modelo": "WRX Concept"},
    {"id": 6, "marca":"Lamborghini", "modelo": "Aventador"},
    {"id": 7, "marca":"Mercedes", "modelo": "AMG GT"},
]

@app.get("/")
def read_root():
    return{"Bienvenido a mi REST API"}

@app.post("/auto")
def create_auto(auto: Auto):
    autos.append(auto.model_dump())
    return{'message': 'Auto creado', "id (nuevo)": auto.id, "marca (nueva)": auto.marca,"modelo (nuevo)": auto.modelo}

@app.get("/auto/ALL")
def read_all():
    return autos

@app.get("/auto/{auto_id}")
def read_id_auto(auto_id: int):
        for aut in autos:
            if aut["id"] == auto_id:
                return aut
        raise HTTPException(status_code=404, detail="Auto not found")

@app.delete("/auto/{auto_id}")
def delete_auto(auto_id: int):
        for index, aut in enumerate(autos):
                if aut["id"] == auto_id:
                    autos.pop(index)
                    return {"message": "Auto borrado satisfactoriamente"}
        raise HTTPException(status_code=404, detail="Auto for delete not found")

@app.patch("/auto/{auto_id}")
def update_auto(auto_id: int, updatedAuto: Auto):
        for index, aut in enumerate(autos):
                if aut["id"] == auto_id:
                    autos[index]["id"] = updatedAuto.id
                    autos[index]["marca"] = updatedAuto.marca
                    autos[index]["modelo"] = updatedAuto.modelo
                    return {"message": "Auto actualizado satisfactoriamente"}
        raise HTTPException(status_code=404, detail="Auto to update not found")


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

ListAutos_db = {
    1: {"id": 1, "marca":"Ford", "modelo": "Mondeo"},
    2: {"id": 2, "marca":"Fiat", "modelo": "Uno"},
    3: {"id": 3, "marca":"Renault", "modelo": "Sandero"}
}

class Auto(BaseModel):
    id: int
    marca: str
    modelo: str

@app.get('/')
def funcPrinc():
    return {"Wolcome"}

@app.get("/car/ALL") 
def get_cars():
    return {"Car List" : ListAutos_db}

@app.get("/car/{id}")
def get_carId(id: int):
    return {"car information": ListAutos_db[id]}

@app.post("/car")
def add_car(auto: Auto):
    id = auto.id
    ListAutos_db[id] = auto.model_dump()
    return {'message': f'successfully created car: {id}'}

@app.delete("/car/{id}")
def delete_carId(id: int):
    del ListAutos_db[id]
    return {"Car List" : ListAutos_db}

@app.patch("/car/{id}")
def patch_car(id: int, auto: Auto):
    ListAutos_db[id].update(auto.model_dump(exclude_unset=True))
    return {"Car List" : ListAutos_db}
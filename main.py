from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

autos_db = {
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
    return {"mensaje" : "Este es un ABM de autos"}

@app.get('/autos')
def getAutos():
    return autos_db

@app.get('/autos/{id}')
def getAutoID(id: int):
    return autos_db[id]

@app.post('/autos')
def createAuto(auto: Auto):
    id = auto.id
    autos_db[id] = auto.model_dump()
    return {'message': f'successfully created auto: {id}'}

@app.delete('/autos/{id}')
def deleteAutoID(id: int):
    del autos_db[id]
    return autos_db

@app.patch('/auto/{id}')
def patchAuto(id: int, auto: Auto):
    autos_db[id].update(auto.model_dump(exclude_unset=True))
    return autos_db

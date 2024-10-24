from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

autos = [
{"id": 1, "marca":"Ford", "modelo": "Mondeo"},
{"id": 2, "marca":"Fiat", "modelo": "Uno"},
{"id": 3, "marca":"Renault", "modelo": "Sandero"},
]

# Auto Model
class Auto(BaseModel):
        id: int
        marca: str
        modelo: str

#GET /auto/ALL
@app.get('/autos')
def read_root():
    return autos

#GET /auto/{ID}
@app.get('/autos/{auto_id}')
def get_auto(auto_id: int):
    for auto in autos:
       if auto["id"] == auto_id:
              return auto
    raise HTTPException(status_code=404, detail="Auto no encontrado")


#POST /auto
@app.post('/autos')
def save_auto(auto : Auto):
    autos.append(auto.model_dump())
    return autos[-1]


#DELETE /auto/{ID}
@app.delete('/autos/{auto_id}')
def delete_auto(auto_id : int):
    for index, auto in enumerate(autos):
       if auto["id"] == auto_id:
              autos.pop(index)
       return {"message": "Auto ha sido eliminado satisfactoriamente"}       
    raise HTTPException(status_code=404, detail="Auto no encontrado")

#PATCH /auto/{ID}
@app.patch('/autos/{auto_id}')
def update_auto(auto_id : int,updatedAuto: Auto):
    for index, auto in enumerate(autos):
       if auto["id"] == auto_id:
              autos[index]["id"] = updatedAuto.id
              autos[index]["marca"] = updatedAuto.marca
              autos[index]["modelo"] = updatedAuto.modelo
       return {"message": "Auto ha sido actualizado satisfactoriamente"}       
    raise HTTPException(status_code=404, detail="Auto no encontrado")
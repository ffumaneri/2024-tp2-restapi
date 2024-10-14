from fastapi import FastAPI, HTTPException
from model import AutoBase,AutoConID


app = FastAPI()
autos=[
{"id": 1, "marca":"Ford", "modelo": "Mondeo"},
{"id": 2, "marca":"Fiat", "modelo": "Uno"},
{"id": 3, "marca":"Renault", "modelo": "Sandero"},
]

@app.get("/Autos")
async def read_autos():
    return autos

@app.get("/auto/{auto_id}")
def read_auto(auto_id: int):
    for auto in autos:
        if auto["id"]==auto_id:
                return auto     
    raise HTTPException(500, 'No se encontro un auto con ese ID') 
       
@app.post("/CrearAuto")
def crear_auto(auto: AutoConID):
     autos.append(auto)
     return {"message: ":"Auto creado con exito: "}

@app.delete("/BorrarAuto/{auto_id}")
def borrar_auto(auto_id: int):
     for auto in autos:
          if auto["id"]==auto_id:
               autos.remove(auto)
               return {"message: ":"Auto Borrado "}
     raise HTTPException(500, 'No se encontro un auto con ese ID') 

@app.patch("/Editar_Auto/{auto_id}")
def editar_auto(auto_id: int, autoCambiado: AutoBase):
     for auto in autos:
          if auto["id"]==auto_id:
            auto['modelo'] = autoCambiado.modelo
            auto['marca'] = autoCambiado.marca
            return {"message: ":"Auto Actualizado con exito: "}
     raise HTTPException(500, 'No se encontro un auto con ese ID') 
			
                
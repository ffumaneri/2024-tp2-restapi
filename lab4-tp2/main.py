from fastapi import FastAPI, HTTPException
from Auto import Auto
from typing import List

app = FastAPI()

auto1= Auto(id=1, marca="Ford", modelo="Mondeo")
auto2= Auto(id=2, marca="Fiat", modelo="Uno")
auto3= Auto(id=3, marca="Renault", modelo="Sandero")
lista_autos:List[Auto] = [auto1,auto2,auto3]


#ENDPOINTS PARA DEVOLVER AUTOS TANTO LA LISTA COMPLETA COMO UNO EN PARTICULAR
@app.get("/auto/all", response_model = List[Auto])
def get_autos():
    return lista_autos

@app.get("/auto/{id}", response_model=Auto)
def get_auto(num_id:int):
    for auto in lista_autos:
        if auto.id == num_id:
            return auto
    raise HTTPException(status_code=404,detail="Auto no encontrado")

#ENDPONT PARA ELIMINAR UN AUTO
@app.delete("/auto/{id}")
def delete_auto(num_id:int):
    if num_id >= len(lista_autos):
        raise HTTPException(status_code=404, detail="El auto no existe en la lista")
    del lista_autos[num_id]
    return {"message": "Auto eliminada correctamente"}

#ENDPOINT PARA AGREGAR UN AUTO A LA LISTA
@app.post("/auto",status_code=201)
def add_auto(nuevo_auto:Auto):
    for a in lista_autos:
        if a.id == nuevo_auto.id:
            raise HTTPException(status_code=404,detail="El auto ya existe")
        
    lista_autos.append(nuevo_auto)
    return {"message": "Auto agregado correctamente"}

#ENDPOINT PARA ACTUALIZAR UN AUTO
@app.patch("/auto/{id}", response_model=Auto)
def update_auto(num_id:int,nuevoauto:Auto):
    if num_id >= len(lista_autos):
        raise HTTPException(status_code = 404, detail = "El auto no fue encontrado")
    lista_autos[num_id] = nuevoauto
    return nuevoauto



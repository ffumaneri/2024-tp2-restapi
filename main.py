from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

class AutoSinId(BaseModel):
	marca: str
	modelo: str

class Auto(AutoSinId):
	id: int

autos = [
	{ 'id': 1, 'marca': 'Ford', 'modelo': 'Mondeo' },
	{ 'id': 2, 'marca': 'Fiat', 'modelo': 'Uno' },
	{ 'id': 3, 'marca': 'Renault', 'modelo': 'Sandero' },
]

# Cómo mierda se escribía un comentario
app = FastAPI()

@app.get('/')
def getRaíz():
	return ':3'

@app.get('/autos')
def getAutos():
	return autos

@app.get('/autos/{id}')
def getAutoById(id: int):
	for auto in autos:
		if auto['id'] == id:
			return auto
	
	raise HTTPException(400, '>:(')

@app.post('/nuevo')
def agregarAuto(auto: Auto):
	autos.append(auto)

	return 'agregao'

@app.delete('/borrar/{id}')
def borrarAuto(id: int):
	for auto in autos:
		if auto['id'] == id:
			autoBorrado = auto
			autos.remove(auto)
			return autoBorrado

	raise HTTPException(400, '>:(')

@app.patch('/editar/{id}')
def editarAuto(id: int, autoSinId: AutoSinId):
	for auto in autos:
		if auto['id'] == id:
			auto['modelo'] = autoSinId.modelo
			auto['marca'] = autoSinId.marca
			return auto
	
	raise HTTPException(400, '>:(')

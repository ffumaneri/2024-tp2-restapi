from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles  # Importa StaticFiles
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de datos para el auto
class Auto(BaseModel):
    id: int
    marca: str
    modelo: str
    año: int
    puertas: int

# Base de datos simulada
autos_db: List[Auto] = [
    Auto(id=1, marca="Ford", modelo="Falcon", año=1995, puertas=5),
]

# Monta la carpeta estática donde están tus archivos CSS y HTML
app.mount("/static", StaticFiles(directory="."), name="static")

# Ruta principal para servir el HTML
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("index.html") as f:
        return f.read()

# Crear un nuevo auto
@app.post("/autos/", response_model=Auto)
def crear_auto(auto: Auto):
    for existing_auto in autos_db:
        if existing_auto.id == auto.id:
            raise HTTPException(status_code=400, detail="El ID del auto ya existe")
    autos_db.append(auto)
    return auto

# Leer todos los autos
@app.get("/autos/", response_model=List[Auto])
def leer_autos():
    return autos_db

# Actualizar un auto por ID
@app.put("/autos/{auto_id}", response_model=Auto)
def actualizar_auto(auto_id: int, updated_auto: Auto):
    for auto in autos_db:
        if auto.id == auto_id:
            auto.marca = updated_auto.marca
            auto.modelo = updated_auto.modelo
            auto.año = updated_auto.año
            auto.puertas = updated_auto.puertas
            return auto
    raise HTTPException(status_code=404, detail="El auto no existe")

# Eliminar un auto por ID
@app.delete("/autos/{auto_id}")
def borrar_auto(auto_id: int):
    global autos_db
    autos_db = [auto for auto in autos_db if auto.id != auto_id]
    return {"message": "Auto eliminado"}

# Obtener un auto por ID
@app.get("/autos/{auto_id}", response_model=Auto)
def obtener_auto_por_id(auto_id: int):
    for auto in autos_db:
        if auto.id == auto_id:
            return auto
    raise HTTPException(status_code=404, detail="El auto no existe")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class AutoModel(BaseModel):
    auto_id: int
    marca: str
    modelo: str


autos = [
    {"auto_id": 0, "marca": "Ford", "modelo": "Mondeo"},
    {"auto_id": 1, "marca": "Fiat", "modelo": "Uno"},
    {"auto_id": 2, "marca": "Renault", "modelo": "Sandero"},
]


@app.get("/")
async def root():
    return {"TP2": "Active"}


@app.get("/auto/ALL", response_model=list[AutoModel])
async def get_all():
    return autos


@app.get("/auto/{id}", response_model=AutoModel)
async def get_auto(id: int):
    if (id) < len(autos):
        return autos[id]
    raise HTTPException(status_code=404, detail="Car not found")


@app.post("/auto/")
async def post_auto(unAuto: AutoModel):
    try:
        if any(unAutoExistente["auto_id"] == unAuto.auto_id for unAutoExistente in autos):
            raise ValueError("Id auto already exists!")
        autos.append(unAuto.dict())
        return {"Message": f"| {unAuto} | was appended to the list!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e).split("\n"))


@app.delete("/auto/{id}")
async def delete_auto(id: int):
    try:
        unAuto = next((auto for auto in autos if auto["auto_id"] == id),None)
        if not unAuto:
            raise HTTPException(status_code=404,detail=f"ID {id} not found") 
        return {"Message": f" {unAuto}\n was removed"}
    except Exception as e:
        raise HTTPException(status_code=405, detail=str(e).split("\n"))


@app.patch("/auto/{id}", response_model= AutoModel)
async def patch_auto(id: int, unAuto: AutoModel):
    try:
        auto_existente = next((auto for auto in autos if auto['auto_id'] == id), None)
        if not auto_existente:
            raise HTTPException(status_code=404, detail=f"Auto con ID {id} no encontrado.")
        autos.remove(auto_existente)
        autos.append(unAuto.dict())
        return unAuto
    except Exception as e:
        raise HTTPException(status_code=405, detail=str(e).split("\n"))
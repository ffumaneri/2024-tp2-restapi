from typing import Annotated, List
from pytest import Session
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI()

# region DB

SQLALCHEMY_DB_URL = SQLALCHEMY_DB_URL="postgresql+psycopg2://postgres:aslan.olivia@localhost:5432/utn-lab-tp-2"

class Database():
    def __init__(self, connection_string: str = SQLALCHEMY_DB_URL, echo: bool = True):
        self.engine = create_engine(connection_string, echo=echo)

    @property
    def SessionLocal(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def create_all(self):
        ORMBase.metadata.create_all(bind=self.engine)

db_instance = Database()

ORMBase = declarative_base()

class AutoBd(ORMBase):
    __tablename__ = 'autos'
    id = Column(Integer, primary_key=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)

db_instance.create_all()

# endregion

# region FastApi

class AutoSinId(BaseModel):
    marca: str = Field(..., description="Marca del Auto", max_length=50)
    modelo: str = Field(..., description="Modelo del Auto", max_length=50)

class Auto(AutoSinId):
    id: int

@app.get("/auto/all")
def get_autos(db: Session = Depends(db_instance.get_db)):
    autos = db.query(AutoBd).all()
    return autos

@app.get("/auto/{id}", response_model=Auto)
def get_auto(id: Annotated[int, Path(description="Id del auto a buscar")], db: Session = Depends(db_instance.get_db)):
    auto = db.get(AutoBd, id)
    if not auto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encuentra un auto con el id: {id}")
    return auto

@app.post("/auto", status_code=status.HTTP_201_CREATED)
def add_auto(autos: List[AutoSinId], db: Session = Depends(db_instance.get_db)):
    for a in autos:
        auto_db = AutoBd()
        auto_db.marca = a.marca
        auto_db.modelo = a.modelo
        db.add(auto_db)
    
    db.commit()
    return {"code": "Funciona"}

@app.delete("/auto/{id}")
def delete_auto(id: Annotated[int, Path(description="Id del auto a eliminar")], db: Session = Depends(db_instance.get_db)):
    auto = db.query(AutoBd).filter(AutoBd.id == id).first()
    if not auto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontró un auto que coincida con el id {id}")
    
    db.delete(auto)
    db.commit()

    return {"code": "Auto Eliminado"}

@app.patch("/auto/{id}")
def update_auto(data: AutoSinId, id: Annotated[int, Path(description="Id del auto a modificar")], db: Session = Depends(db_instance.get_db)):
    autoAModificar = db.query(AutoBd).filter(AutoBd.id == id).first()
    autoModificado = data.model_dump(exclude_unset=True)
    if not autoAModificar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se encontró un auto que coincida con el id {id}")

    for key, value in autoModificado.items():
        setattr(autoAModificar, key, value)

    db.commit()   

    return {"code": "Auto modificado"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)

# endregion
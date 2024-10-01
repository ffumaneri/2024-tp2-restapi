from pydantic import BaseModel

class Auto(BaseModel):
    id:int
    marca:str
    modelo:str



from pydantic import BaseModel 


class AutoBase(BaseModel):
	marca: str
	modelo: str

class AutoConID(AutoBase):
	id: int
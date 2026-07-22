from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    username: str
    password: str

from pydantic import BaseModel

class ReservoirCreate(BaseModel):
    date: str
    rainfall: float
    inflow: float
    outflow: float
    evaporation: float
    demand: float
    level: float
    capacity: float
    location: str
from sqlalchemy import Column, Integer, Float, String, VARCHAR
from .database import Base

# -------- RESERVOIR TABLE --------
class ReservoirData(Base):
    __tablename__ = "reservoir_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(50))
    rainfall = Column(Float)
    inflow = Column(Float)
    outflow = Column(Float)
    evaporation = Column(Float)
    demand = Column(Float)
    level = Column(Float)
    capacity = Column(Float)
    location = Column(String(150))

# -------- USER TABLE --------
from sqlalchemy import Column, Integer, String,VARCHAR , TIMESTAMP, text
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

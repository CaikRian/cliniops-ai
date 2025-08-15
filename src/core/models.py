from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()

class Protocol(Base):
    __tablename__ = "protocols"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    specialty = Column(String(100), nullable=True)
    content = Column(Text, nullable=False)
    # embedding salvo como JSON string (lista de floats) para simplificar
    embedding = Column(Text, nullable=False)

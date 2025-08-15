from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import json, os
from .models import Base, Protocol
from ..ai.embeddings import embed_text, to_storage

DB_URL = os.getenv("DATABASE_URL", "sqlite:///cliniops.db")

engine = create_engine(
    DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed if empty
def seed_if_needed():
    db = SessionLocal()
    try:
        count = db.query(Protocol).count()
        if count == 0:
            samples = [
                dict(
                    title="Infecção de vias aéreas superiores (IVAS)",
                    specialty="Clínica Médica",
                    content=(
                        "Sintomas: coriza, dor de garganta, tosse. Manejo: analgésicos/antitérmicos, hidratação, "
                        "descanso. Antibiótico apenas se suspeita bacteriana (ex.: sinusite com critérios)."
                    ),
                ),
                dict(
                    title="Hipertensão Arterial Sistêmica (HAS)",
                    specialty="Cardiologia",
                    content=(
                        "Diagnóstico por medidas repetidas. Estilo de vida: reduzir sódio, exercício, controle de peso. "
                        "Farmacoterapia: IECA/BRA, tiazídicos, BCC conforme perfil. Acompanhar PA e função renal."
                    ),
                ),
                dict(
                    title="Diabetes Mellitus tipo 2 (DM2)",
                    specialty="Endocrinologia",
                    content=(
                        "Mudança de estilo de vida. Primeira linha: metformina se não houver contraindicação. "
                        "Adicionar agonista GLP-1 ou SGLT2 conforme risco CV. Monitorar HbA1c e complicações."
                    ),
                ),
            ]
            for s in samples:
                vec = embed_text(s["title"] + "\n" + s["content"])
                p = Protocol(
                    title=s["title"],
                    specialty=s["specialty"],
                    content=s["content"],
                    embedding=to_storage(vec),
                )
                db.add(p)
            db.commit()
    finally:
        db.close()

seed_if_needed()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

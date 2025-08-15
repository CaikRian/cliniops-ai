from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List
from .schemas import ProtocolIn, ProtocolOut, SuggestIn
from ..core.db import get_session
from ..core.models import Protocol
from ..ai.embeddings import embed_text, from_storage, cosine

from sqlalchemy.orm import Session

app = FastAPI(title="CliniOps.AI", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/protocols", response_model=ProtocolOut)
def create_protocol(p: ProtocolIn, db: Session = Depends(get_session)):
    vec = embed_text((p.title or "") + "\n" + p.content)
    pr = Protocol(title=p.title, specialty=p.specialty, content=p.content, embedding=json_dump_vec(vec))
    db.add(pr); db.commit(); db.refresh(pr)
    return ProtocolOut(id=pr.id, title=pr.title, specialty=pr.specialty, content=pr.content)

def json_dump_vec(vec):
    import json, numpy as np
    return json.dumps(vec.tolist())

@app.get("/protocols", response_model=List[ProtocolOut])
def search_protocols(q: str = Query(..., min_length=2), db: Session = Depends(get_session)):
    # carrega tudo (leve no demo) e ranqueia em Python
    qvec = embed_text(q)
    rows = db.query(Protocol).all()
    scored = []
    for r in rows:
        rvec = from_storage(r.embedding)
        scored.append((cosine(qvec, rvec), r))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = [r for _, r in scored[:10]]
    return [ProtocolOut(id=r.id, title=r.title, specialty=r.specialty, content=r.content) for r in top]

@app.post("/ai/suggest")
def ai_suggest(req: SuggestIn, db: Session = Depends(get_session)):
    q = (req.specialty + " " if req.specialty else "") + req.symptoms
    qvec = embed_text(q)
    rows = db.query(Protocol).all()
    scored = []
    for r in rows:
        rvec = from_storage(r.embedding)
        scored.append((cosine(qvec, rvec), r))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:5]
    reminders = []
    tl = q.lower()
    if "antibiótico" in tl or "antibiotico" in tl:
        reminders.append("Confirmar histórico de alergias (penicilina/cefalosporinas).")
    if "hipertens" in tl:
        reminders.append("Conferir PA em mais de uma medida e revisar adesão ao tratamento.")

    return {
        "matches": [{"id": r.id, "title": r.title, "specialty": r.specialty} for _, r in top],
        "reminders": reminders
    }

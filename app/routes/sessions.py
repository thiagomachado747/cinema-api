from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Session as CinemaSession, Reservation
from ..schemas import SessionCreate, SessionResponse
from .auth import get_current_user

router = APIRouter(prefix="/sessions", tags=["Sessões"])

def get_available_seats(session: CinemaSession, db: Session) -> int:
    reserved = db.query(Reservation).filter(Reservation.session_id == session.id).count()
    return session.total_seats - reserved

@router.get("/", response_model=List[SessionResponse],
    summary="Listar sessões",
    description="Retorna todas as sessões disponíveis com a quantidade de assentos livres.")
def list_sessions(db: Session = Depends(get_db)):
    sessions = db.query(CinemaSession).all()
    result = []
    for s in sessions:
        s_dict = {c.name: getattr(s, c.name) for c in s.__table__.columns}
        s_dict["available_seats"] = get_available_seats(s, db)
        result.append(s_dict)
    return result

@router.get("/{session_id}", response_model=SessionResponse,
    summary="Buscar sessão por ID",
    description="Retorna os detalhes de uma sessão específica, incluindo assentos disponíveis.")
def get_session(session_id: int, db: Session = Depends(get_db)):
    s = db.query(CinemaSession).filter(CinemaSession.id == session_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    s_dict = {c.name: getattr(s, c.name) for c in s.__table__.columns}
    s_dict["available_seats"] = get_available_seats(s, db)
    return s_dict

@router.post("/", response_model=SessionResponse, status_code=201,
    summary="Criar sessão",
    description="Cria uma nova sessão para um filme. **Apenas admins podem usar esse endpoint.**")
def create_session(session: SessionCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Apenas admins podem criar sessões")
    new_session = CinemaSession(**session.model_dump())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    s_dict = {c.name: getattr(new_session, c.name) for c in new_session.__table__.columns}
    s_dict["available_seats"] = new_session.total_seats
    return s_dict

@router.delete("/{session_id}", status_code=204,
    summary="Remover sessão",
    description="Remove uma sessão pelo seu ID. **Apenas admins podem usar esse endpoint.**")
def delete_session(session_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Apenas admins podem remover sessões")
    s = db.query(CinemaSession).filter(CinemaSession.id == session_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    db.delete(s)
    db.commit()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Reservation, Session as CinemaSession
from ..schemas import ReservationCreate, ReservationResponse
from .auth import get_current_user

router = APIRouter(prefix="/reservations", tags=["Reservas"])

@router.get("/", response_model=List[ReservationResponse],
    summary="Minhas reservas",
    description="Retorna todas as reservas do usuário autenticado.")
def my_reservations(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Reservation).filter(Reservation.user_id == current_user.id).all()

@router.post("/", response_model=ReservationResponse, status_code=201,
    summary="Fazer reserva",
    description="Reserva um assento em uma sessão. Informe o ID da sessão e o número do assento desejado.")
def create_reservation(data: ReservationCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    session = db.query(CinemaSession).filter(CinemaSession.id == data.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    existing = db.query(Reservation).filter(
        Reservation.session_id == data.session_id,
        Reservation.seat_number == data.seat_number
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Assento já reservado")

    total_reserved = db.query(Reservation).filter(Reservation.session_id == data.session_id).count()
    if total_reserved >= session.total_seats:
        raise HTTPException(status_code=400, detail="Sessão esgotada")

    reservation = Reservation(user_id=current_user.id, **data.model_dump())
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

@router.delete("/{reservation_id}", status_code=204,
    summary="Cancelar reserva",
    description="Cancela uma reserva pelo seu ID. O usuário só pode cancelar suas próprias reservas.")
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id,
        Reservation.user_id == current_user.id
    ).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    db.delete(reservation)
    db.commit()
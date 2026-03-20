from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Auth
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Movies
class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    duration_minutes: int
    genre: Optional[str] = None

class MovieResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    duration_minutes: int
    genre: Optional[str]
    class Config:
        from_attributes = True

# Sessions
class SessionCreate(BaseModel):
    movie_id: int
    room: str
    datetime: datetime
    total_seats: int = 50
    price: float

class SessionResponse(BaseModel):
    id: int
    movie_id: int
    room: str
    datetime: datetime
    total_seats: int
    price: float
    available_seats: int
    class Config:
        from_attributes = True

# Reservations
class ReservationCreate(BaseModel):
    session_id: int
    seat_number: int

class ReservationResponse(BaseModel):
    id: int
    session_id: int
    seat_number: int
    created_at: datetime
    class Config:
        from_attributes = True

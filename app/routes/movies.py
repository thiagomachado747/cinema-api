from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Movie
from ..schemas import MovieCreate, MovieResponse
from .auth import get_current_user

router = APIRouter(prefix="/movies", tags=["Filmes"])

@router.get("/", response_model=List[MovieResponse],
    summary="Listar filmes",
    description="Retorna todos os filmes cadastrados no sistema.")
def list_movies(db: Session = Depends(get_db)):
    return db.query(Movie).all()

@router.get("/{movie_id}", response_model=MovieResponse,
    summary="Buscar filme por ID",
    description="Retorna os detalhes de um filme específico pelo seu ID.")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return movie

@router.post("/", response_model=MovieResponse, status_code=201,
    summary="Cadastrar filme",
    description="Cadastra um novo filme no sistema. **Apenas admins podem usar esse endpoint.**")
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Apenas admins podem cadastrar filmes")
    new_movie = Movie(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie

@router.delete("/{movie_id}", status_code=204,
    summary="Remover filme",
    description="Remove um filme do sistema pelo seu ID. **Apenas admins podem usar esse endpoint.**")
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Apenas admins podem remover filmes")
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    db.delete(movie)
    db.commit()

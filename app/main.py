from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import auth, movies, sessions, reservations

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cinema API",
    version="1.0.0",
    description="API REST para gerenciamento de um sistema de cinema.",
    openapi_tags=[
        {"name": "Autenticação", "description": "Cadastro e login de usuários"},
        {"name": "Filmes", "description": "Cadastro e listagem de filmes"},
        {"name": "Sessões", "description": "Gerenciamento de sessões e horários"},
        {"name": "Reservas", "description": "Reserva e cancelamento de assentos"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(sessions.router)
app.include_router(reservations.router)

@app.get("/", tags=["Geral"], summary="Status da API", description="Verifica se a API está funcionando.")
def root():
    return {"mensagem": "Cinema API funcionando! 🎬"}
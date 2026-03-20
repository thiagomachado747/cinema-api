# Cinema API

API REST para gerenciamento de um sistema de cinema, desenvolvida como projeto de estudo e portfólio.

Desenvolvida por **Thiago Machado** — Junho/2024

---

## Sobre o projeto

Esse projeto nasceu com o objetivo de praticar desenvolvimento backend com Python e FastAPI. A ideia foi criar algo funcional do zero: autenticação de usuários, cadastro de filmes, sessões com controle de vagas e reserva de assentos.

Junto com a API, também desenvolvi um painel web simples em HTML puro para facilitar o uso sem precisar do Swagger.

## Tecnologias usadas

- Python + FastAPI
- MySQL + SQLAlchemy
- JWT para autenticação
- Passlib + bcrypt para hash de senhas
- HTML/CSS/JS puro no painel

## Como rodar

**Pré-requisitos:** Python 3.10+, MySQL instalado

```bash
# Clone o repositório
git clone https://github.com/thiagomachado747/cinema-api.git
cd cinema-api

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt
```

Crie um banco de dados MySQL chamado `cinema_db` e configure o arquivo `.env` baseado no `.env.example`:

```env
DATABASE_URL=mysql+pymysql://root:sua_senha@localhost:3306/cinema_db
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

```bash
# Rode a API
uvicorn app.main:app --reload
```

Acesse a documentação em: `http://localhost:8000/docs`

Para usar o painel, abra o arquivo `painel.html` diretamente no navegador com a API rodando.

## Endpoints

| Método | Rota | Acesso |
|--------|------|--------|
| POST | `/auth/register` | Público |
| POST | `/auth/login` | Público |
| GET | `/movies/` | Público |
| POST | `/movies/` | Admin |
| DELETE | `/movies/{id}` | Admin |
| GET | `/sessions/` | Público |
| POST | `/sessions/` | Admin |
| DELETE | `/sessions/{id}` | Admin |
| GET | `/reservations/` | Autenticado |
| POST | `/reservations/` | Autenticado |
| DELETE | `/reservations/{id}` | Autenticado |

## Observações

- Para virar admin, atualize diretamente no banco: `UPDATE users SET is_admin = 1 WHERE email = 'seu@email.com';`
- O arquivo `.env` não é enviado ao repositório por segurança

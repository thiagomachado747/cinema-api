# 🎬 Cinema API

API REST para gerenciamento de um sistema de cinema, desenvolvida com **Python**, **FastAPI** e **MySQL**.

## 📋 Funcionalidades

- Autenticação de usuários com JWT
- Cadastro e listagem de filmes
- Criação e gerenciamento de sessões com controle de vagas
- Reserva e cancelamento de assentos
- Controle de acesso por perfil (admin / usuário comum)

---

## 🛠️ Tecnologias

- [Python 3.11+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [MySQL](https://www.mysql.com/)
- [JWT (python-jose)](https://github.com/mpdavis/python-jose)
- [Passlib + bcrypt](https://passlib.readthedocs.io/)

---

## 📁 Estrutura do Projeto

```
cinema-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routes/
│       ├── __init__.py
│       ├── auth.py
│       ├── movies.py
│       ├── sessions.py
│       └── reservations.py
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/cinema-api.git
cd cinema-api
```

### 2. Crie o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/cinema_db
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Crie o banco de dados no MySQL

```sql
CREATE DATABASE cinema_db;
```

### 6. Rode a aplicação

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

Documentação interativa: `http://localhost:8000/docs`

---

## 🔚 Endpoints

### Auth
| Método | Rota | Acesso | Descrição |
|--------|------|--------|-----------|
| POST | `/auth/register` | Público | Cadastrar usuário |
| POST | `/auth/login` | Público | Login e geração de token |

### Filmes
| Método | Rota | Acesso | Descrição |
|--------|------|--------|-----------|
| GET | `/movies/` | Público | Listar todos os filmes |
| GET | `/movies/{id}` | Público | Detalhe de um filme |
| POST | `/movies/` | Admin | Cadastrar filme |
| DELETE | `/movies/{id}` | Admin | Remover filme |

### Sessões
| Método | Rota | Acesso | Descrição |
|--------|------|--------|-----------|
| GET | `/sessions/` | Público | Listar sessões com vagas disponíveis |
| GET | `/sessions/{id}` | Público | Detalhe de uma sessão |
| POST | `/sessions/` | Admin | Criar sessão |
| DELETE | `/sessions/{id}` | Admin | Remover sessão |

### Reservas
| Método | Rota | Acesso | Descrição |
|--------|------|--------|-----------|
| GET | `/reservations/` | Autenticado | Listar minhas reservas |
| POST | `/reservations/` | Autenticado | Fazer uma reserva |
| DELETE | `/reservations/{id}` | Autenticado | Cancelar uma reserva |

---

## 🔐 Autenticação

A API utiliza **JWT Bearer Token**. Após o login, inclua o token no header das requisições protegidas:

```
Authorization: Bearer <seu_token>
```

---

## 👑 Como criar um usuário admin

Após registrar um usuário normalmente, atualize diretamente no banco:

```sql
UPDATE users SET is_admin = 1 WHERE email = 'seu@email.com';
```

---

## 💡 Exemplo de uso

### 1. Registrar usuário
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@email.com", "password": "123456"}'
```

### 2. Fazer login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@email.com", "password": "123456"}'
```

### 3. Fazer uma reserva (com token)
```bash
curl -X POST http://localhost:8000/reservations/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"session_id": 1, "seat_number": 12}'
```

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

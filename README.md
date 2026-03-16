# Leads API

API desenvolvida com **FastAPI** utilizando **MongoDB** como banco de dados.

---

# Requisitos

* **Python 3.11+**
* **Docker + Docker Compose** (opcional, mas recomendado)
* **Git**

---

# Clonar o repositório

```bash
git clone https://github.com/washingtonjnr/leads-api
cd leads-api
```

---

# Criar arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
APP_MONGODB_URL=mongodb://localhost:27017
APP_MONGODB_DB=leads_db

APP_DUMMYJSON_API_BASE_URL=https://dummyjson.com
APP_DUMMYJSON_TIMEOUT=10

APP_API_TITLE=Leads API
APP_API_VERSION=1.0.0
APP_API_DESCRIPTION=API para gerenciamento de Leads
```

---

# Rodando com Docker

## Subir os containers

```bash
docker compose up --build
```

Isso irá iniciar:

* **MongoDB**
* **FastAPI**

---

## Acessar a API

Swagger UI:

```
http://localhost:8000/docs
```

---

# Rodando localmente (venv)

## Criar ambiente virtual

Linux / Mac:

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

---

## Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Subir MongoDB

Se tiver Mongo instalado localmente:

```
mongodb://localhost:27017
```

Ou usando Docker:

```bash
docker run -d -p 27017:27017 mongo
```

---

## Rodar a API

```bash
uvicorn app.main:app --reload
```

ou 

```bash
python run.py
```

---

## Acessar a API / Testar endpoints

Swagger UI:

```
http://localhost:8000/docs
```

# Arquitetura
[**ARCHITECTURE**](./docs/ARCHITECTURE.md)


## Referências Externas

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Moto](https://pypi.org/project/moto/)
- [MongoDB](https://www.mongodb.com/)

# Leads API - Layered Architecture

## Visão Geral

A **Leads API** é uma aplicação backend desenvolvida com **FastAPI** e **MongoDB**, seguindo os princípios de **Arquitetura em Camadas** com clara separação de responsabilidades. A arquitetura permite escalabilidade, manutenibilidade e facilita testes automatizados.

## Estrutura de Camadas

```
┌──────────────────────────────────────┐
│   API Routes (REST Endpoints)        │  ← Camada de Apresentação
│   app/api/controllers/                   │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│   Services (Lógica de Negócio)       │  ← Camada de Aplicação
│   app/services/                      │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│   Models | Schemas | Providers       │  ← Camada de Domínio
│   app/models/                        │
│   app/schemas/                       │
│   app/providers/                     │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│   Core (Config, Database)            │  ← Camada de Infraestrutura
│   app/core/                          │
└──────────────────────────────────────┘
```

## Estrutura de Diretórios

```
ce-api/
├── app/
│   ├── __init__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── lead.py                # Endpoints REST for leads
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.py              # Configurações da aplicação (variáveis de ambiente, settings)
│   │   ├── containers.py          # Configuração de injeção de dependências / containers da aplicação
│   │   ├── database.py            # Configuração e conexão com o banco de dados
│   │   └── types.py               # Definição de tipos e schemas utilizados na aplicação
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Settings via pydantic-settings
│   │   └── database.py            # Conexão MongoDB
│   ├── models/
│   │   ├── __init__.py
│   │   └── lead.py                # Lead model (ODM)
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py                # Classe abstrata Provider
│   │   └── dummyjson.py           # Implementação DummyJSON
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── lead.py                # Pydantic schemas (validação)
│   ├── services/
│   │   ├── __init__.py
│   │   └── lead_service.py        # Lógica de negócio
│   └── main.py                    # Aplicação FastAPI
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Responsabilidades por Camada

### **1. Camada de Apresentação (API Routes)**
**Arquivo:** `app/controllers/leads.py`

- Define os endpoints REST
- Mapeia HTTP requests/responses
- Delega processamento para services
- Retorna respostas com status codes apropriados

**Exemplo:**
```python
@router.post("/leads", status_code=201, response_model=LeadResponse)
async def create_lead(lead_data: LeadRequest, service: LeadService = Depends()):
    return await service.create_lead(lead_data)
```

### **2. Camada de Aplicação (Services)**
**Arquivo:** `app/services/lead.py`

- Implementa regras de negócio
- Orquestra operações entre models, schemas e providers
- Gerencia transações e validações
- Trata erros e exceções

**Responsabilidades:**
- Criar leads com dados da API externa
- Listar leads do banco de dados
- Buscar leads por ID
- Atualizar e deletar leads

### **3. Camada de Domínio**

#### **Models** (`app/models/lead.py`)
- Define estrutura do documento MongoDB
- Utiliza Beanie ODM (async MongoDB)
- Especifica campos, índices e validações de schema do banco

#### **Schemas** (`app/schemas/lead/lead_response.py`)
- Define estruturas Pydantic para validação
- Separados em `LeadRequest` (entrada) e `LeadResponse` (saída)
- Garante tipo-segurança nos endpoints

#### **Providers** (`app/providers/`)
- **Pattern:** Strategy Pattern + Abstract Base Class
- **Objetivo:** Abstrair integrações com APIs externas
- **Benefício:** Fácil adicionar novos providers sem modificar services

**Estrutura:**
```python
# base.py
@abstractmethod
async def fetch_user_data(user_id: int) -> dict:
    pass

# dummyjson.py
class DummyJSONProvider(Provider):
    async def fetch_user_data(user_id: int) -> dict:
        # Implementação concreta
```

### **4. Camada de Infraestrutura (Core)**

#### **Config** (`app/core/config.py`)
- Gerencia variáveis de ambiente
- Pydantic BaseSettings para validação
- Suporta múltiplos ambientes (dev, prod)

#### **Database** (`app/core/database.py`)
- Inicializa conexão MongoDB
- Gerencia lifespan da aplicação
- Funções de conectar/desconectar

## Padrões de Design Utilizados

### **1. Provider Pattern**
Abstração para integração com APIs externas, permitindo múltiplas implementações sem acoplamento.

**Vantagem:** Trocar providers é trivial (adapter pattern).

### **2. Dependency Injection**
FastAPI injeta dependências automaticamente via `Depends()`.

**Vantagem:** Facilita testes unitários (mock providers).

### **3. Service Layer**
Centralizando lógica de negócio separa responsabilidades.

**Vantagem:** Reutilização de lógica entre endpoints.

**Vantagem:** Isolamento da lógica de persistência.

## Tratamento de Falhas

**Cenário:** API externa (DummyJSON) indisponível

- **Comportamento:** Lead é criado normalmente com `birth_date = null`
- **Razão:** Falhas externas não devem bloquear operações críticas
- **Implementação:** Provider retorna dados parciais em erro

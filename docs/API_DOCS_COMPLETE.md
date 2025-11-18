# 🚀 LabTrans API - Documentação Completa

## 📋 Visão Geral

A **LabTrans API** é um sistema completo para gerenciamento de laboratórios, salas, gestores e reservas. A API foi desenvolvida usando **Clean Architecture** com **Django REST Framework**.

### 🎯 Funcionalidades

- ✅ **Gerenciamento de Locations** (Locais/Laboratórios)
- ✅ **Gerenciamento de Managers** (Gestores)
- ✅ **Gerenciamento de Rooms** (Salas)
- ✅ **Gerenciamento de Bookings** (Reservas)

### 🔧 Tecnologias

- **Backend**: Django 4.2.7 + Django REST Framework 3.14.0
- **Banco de Dados**: SQLite (desenvolvimento)
- **Arquitetura**: Clean Architecture
- **Autenticação**: Desabilitada para desenvolvimento

---

## 🌐 Base URL

```
http://127.0.0.1:8000/api
```

---

## 📍 **LOCATIONS** (Locais/Laboratórios)

### Endpoints Disponíveis

| Método | Endpoint           | Descrição                  |
| ------ | ------------------ | -------------------------- |
| GET    | `/locations/`      | Listar todos os locais     |
| POST   | `/locations/`      | Criar novo local           |
| GET    | `/locations/{id}/` | Buscar local por ID        |
| PUT    | `/locations/{id}/` | Atualizar local (completo) |
| PATCH  | `/locations/{id}/` | Atualizar local (parcial)  |
| DELETE | `/locations/{id}/` | Deletar local              |

### Filtros de Consulta

- `?name=nome_do_local`
- `?address=endereco`
- `?search=termo_de_busca`

### Exemplo de Uso

#### ➕ Criar Local

```bash
POST /api/locations/
Content-Type: application/json

{
  \"name\": \"Laboratório Principal\",
  \"address\": \"Rua das Flores, 123\",
  \"description\": \"Laboratório principal da instituição\"
}
```

#### ✅ Resposta

```json
{
  \"id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"name\": \"Laboratório Principal\",
  \"address\": \"Rua das Flores, 123\",
  \"description\": \"Laboratório principal da instituição\",
  \"created_at\": \"2025-11-18T15:32:25.123456Z\",
  \"updated_at\": \"2025-11-18T15:32:25.123456Z\"
}
```

---

## 👥 **MANAGERS** (Gestores)

### Endpoints Disponíveis

| Método | Endpoint          | Descrição                   |
| ------ | ----------------- | --------------------------- |
| GET    | `/managers/`      | Listar todos os gestores    |
| POST   | `/managers/`      | Criar novo gestor           |
| GET    | `/managers/{id}/` | Buscar gestor por ID        |
| PUT    | `/managers/{id}/` | Atualizar gestor (completo) |
| PATCH  | `/managers/{id}/` | Atualizar gestor (parcial)  |
| DELETE | `/managers/{id}/` | Deletar gestor              |

### Ações Customizadas

| Método | Endpoint                            | Descrição                |
| ------ | ----------------------------------- | ------------------------ |
| GET    | `/managers/by_email/?email={email}` | Buscar gestor por email  |
| GET    | `/managers/search/?name={name}`     | Buscar gestores por nome |

### Exemplo de Uso

#### ➕ Criar Gestor

```bash
POST /api/managers/
Content-Type: application/json

{
  \"name\": \"João Silva\",
  \"email\": \"joao@labtrans.com\",
  \"phone\": \"(11) 98765-4321\"
}
```

#### ✅ Resposta

```json
{
  \"id\": \"550e8400-e29b-41d4-a716-446655440001\",
  \"name\": \"João Silva\",
  \"email\": \"joao@labtrans.com\",
  \"phone\": \"(11) 98765-4321\",
  \"created_at\": \"2025-11-18T15:32:25.123456Z\",
  \"updated_at\": \"2025-11-18T15:32:25.123456Z\"
}
```

---

## 🏢 **ROOMS** (Salas)

### Endpoints Disponíveis

| Método | Endpoint       | Descrição                 |
| ------ | -------------- | ------------------------- |
| GET    | `/rooms/`      | Listar todas as salas     |
| POST   | `/rooms/`      | Criar nova sala           |
| GET    | `/rooms/{id}/` | Buscar sala por ID        |
| PUT    | `/rooms/{id}/` | Atualizar sala (completo) |
| PATCH  | `/rooms/{id}/` | Atualizar sala (parcial)  |
| DELETE | `/rooms/{id}/` | Deletar sala              |

### Ações Customizadas

| Método | Endpoint                               | Descrição              |
| ------ | -------------------------------------- | ---------------------- |
| GET    | `/rooms/by_location/?location_id={id}` | Buscar salas por local |

### Exemplo de Uso

#### ➕ Criar Sala

```bash
POST /api/rooms/
Content-Type: application/json

{
  \"name\": \"Sala de Reuniões A\",
  \"location\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"capacity\": 15,
  \"description\": \"Sala equipada com projetor e ar condicionado\",
  \"equipment\": \"Projetor, quadro, ar condicionado\"
}
```

#### ✅ Resposta

```json
{
  \"id\": \"550e8400-e29b-41d4-a716-446655440002\",
  \"name\": \"Sala de Reuniões A\",
  \"location_id\": \"550e8400-e29b-41d4-a716-446655440000\",
  \"location_name\": \"Laboratório Principal\",
  \"capacity\": 15,
  \"description\": \"Sala equipada com projetor e ar condicionado\",
  \"equipment\": \"Projetor, quadro, ar condicionado\",
  \"created_at\": \"2025-11-18T15:32:25.123456Z\",
  \"updated_at\": \"2025-11-18T15:32:25.123456Z\"
}
```

---

## 📅 **BOOKINGS** (Reservas)

### Endpoints Disponíveis

| Método | Endpoint          | Descrição                    |
| ------ | ----------------- | ---------------------------- |
| GET    | `/bookings/`      | Listar todas as reservas     |
| POST   | `/bookings/`      | Criar nova reserva           |
| GET    | `/bookings/{id}/` | Buscar reserva por ID        |
| PUT    | `/bookings/{id}/` | Atualizar reserva (completo) |
| PATCH  | `/bookings/{id}/` | Atualizar reserva (parcial)  |
| DELETE | `/bookings/{id}/` | Deletar/cancelar reserva     |

### Ações Customizadas

| Método | Endpoint                                | Descrição                  |
| ------ | --------------------------------------- | -------------------------- |
| GET    | `/bookings/by_room/?room_id={id}`       | Buscar reservas por sala   |
| GET    | `/bookings/by_manager/?manager_id={id}` | Buscar reservas por gestor |

### Exemplo de Uso

#### ➕ Criar Reserva

```bash
POST /api/bookings/
Content-Type: application/json

{
  \"room\": \"550e8400-e29b-41d4-a716-446655440002\",
  \"manager\": \"550e8400-e29b-41d4-a716-446655440001\",
  \"start_date\": \"2025-11-20T09:00:00Z\",
  \"end_date\": \"2025-11-20T11:00:00Z\",
  \"coffee_option\": true,
  \"coffee_quantity\": 10,
  \"coffee_description\": \"Café e água para reunião\"
}
```

#### ✅ Resposta

```json
{
  \"id\": \"550e8400-e29b-41d4-a716-446655440003\",
  \"room_id\": \"550e8400-e29b-41d4-a716-446655440002\",
  \"room_name\": \"Sala de Reuniões A\",
  \"manager_id\": \"550e8400-e29b-41d4-a716-446655440001\",
  \"manager_name\": \"João Silva\",
  \"start_date\": \"2025-11-20T09:00:00Z\",
  \"end_date\": \"2025-11-20T11:00:00Z\",
  \"coffee_option\": true,
  \"coffee_quantity\": 10,
  \"coffee_description\": \"Café e água para reunião\",
  \"status\": \"confirmed\",
  \"created_at\": \"2025-11-18T15:32:25.123456Z\",
  \"updated_at\": \"2025-11-18T15:32:25.123456Z\"
}
```

---

## 📊 Códigos de Status HTTP

| Código | Descrição                            |
| ------ | ------------------------------------ |
| 200    | OK - Sucesso                         |
| 201    | Created - Recurso criado             |
| 204    | No Content - Deletado com sucesso    |
| 400    | Bad Request - Dados inválidos        |
| 404    | Not Found - Recurso não encontrado   |
| 500    | Internal Server Error - Erro interno |

---

## 🔍 Exemplos de Filtros e Buscas

### Buscar Locations

```bash
GET /api/locations/?search=laboratório
GET /api/locations/?name=Principal
GET /api/locations/?address=Flores
```

### Buscar Managers

```bash
GET /api/managers/by_email/?email=joao@labtrans.com
GET /api/managers/search/?name=João
```

### Buscar Rooms por Local

```bash
GET /api/rooms/by_location/?location_id=550e8400-e29b-41d4-a716-446655440000
```

### Buscar Bookings por Sala ou Gestor

```bash
GET /api/bookings/by_room/?room_id=550e8400-e29b-41d4-a716-446655440002
GET /api/bookings/by_manager/?manager_id=550e8400-e29b-41d4-a716-446655440001
```

---

## 🚀 Como Executar

### 1. Ativar ambiente virtual

```bash
# Windows PowerShell
& C:/projetos/labtras-back/venv/Scripts/Activate.ps1
```

### 2. Executar migrações

```bash
python manage.py migrate
```

### 3. Popular dados iniciais (opcional)

```bash
python manage.py seed_data
```

### 4. Iniciar servidor

```bash
python manage.py runserver
```

### 5. Acessar API

```
http://127.0.0.1:8000/api/
```

---

## 📋 Collection do Postman

Importe a collection atualizada: `docs/postman_collection_v2_complete.json`

### Variáveis de Ambiente

Configure as seguintes variáveis no Postman:

```json
{
  \"base_url\": \"http://127.0.0.1:8000\",
  \"location_id\": \"\",
  \"manager_id\": \"\",
  \"room_id\": \"\",
  \"booking_id\": \"\"
}
```

---

## ✅ Status da API

🎉 **TODAS AS ROTAS ESTÃO FUNCIONANDO PERFEITAMENTE!**

- ✅ **Locations**: CRUD completo + busca
- ✅ **Managers**: CRUD completo + busca por email/nome
- ✅ **Rooms**: CRUD completo + busca por local
- ✅ **Bookings**: CRUD completo + busca por sala/gestor

### 📊 Último Teste (18/11/2025 15:33)

```
📊 LOCATIONS: 2 items criados
📊 MANAGERS: 2 items criados
📊 ROOMS: 2 items criados
📊 BOOKINGS: 1 item criado
```

**Todos os testes passaram com sucesso! ✨**

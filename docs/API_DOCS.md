# 📋 API Documentation - Sistema de Reservas

Documentação completa da API REST para o Sistema de Reservas de Salas.

## 🌐 Base URL

```
http://localhost:8000/api/
```

## 🔐 Autenticação

Atualmente a API não requer autenticação. Em produção, considere implementar:

- JWT (JSON Web Tokens)
- Session Authentication
- Token Authentication

## 📊 Models (Entidades)

### 🏢 Location (Local)

Representa prédios ou locais onde as salas estão.

```python
{
    "id": "string",              # UUID único
    "name": "string",            # Nome do local (obrigatório)
    "address": "string",         # Endereço (opcional)
    "description": "string",     # Descrição (opcional)
    "created_at": "datetime",    # Data de criação
    "updated_at": "datetime"     # Data de atualização
}
```

### 🚪 Room (Sala)

Cada sala pertence a um Local.

```python
{
    "id": "string",              # UUID único
    "name": "string",            # Nome da sala (obrigatório)
    "capacity": "integer",       # Capacidade (opcional)
    "location": "string",        # ID do local (obrigatório)
    "description": "string",     # Descrição (opcional)
    "created_at": "datetime",    # Data de criação
    "updated_at": "datetime"     # Data de atualização
}
```

### 👤 Manager (Responsável)

Pessoa responsável pela reserva.

```python
{
    "id": "string",              # UUID único
    "name": "string",            # Nome (obrigatório)
    "email": "string",           # Email único (obrigatório)
    "phone": "string",           # Telefone (opcional)
    "created_at": "datetime",    # Data de criação
    "updated_at": "datetime"     # Data de atualização
}
```

### 📅 Booking (Reserva)

Reserva de uma sala.

```python
{
    "id": "string",                    # UUID único
    "room": "string",                  # ID da sala (obrigatório)
    "manager": "string",               # ID do responsável (obrigatório)
    "start_date": "datetime",          # Data/hora início (obrigatório)
    "end_date": "datetime",            # Data/hora fim (obrigatório)
    "coffee_option": "boolean",        # Opção café (padrão: false)
    "coffee_quantity": "integer",      # Quantidade café (opcional)
    "coffee_description": "string",    # Descrição café (opcional)
    "created_at": "datetime",          # Data de criação
    "updated_at": "datetime",          # Data de atualização

    # Campos adicionais na resposta
    "room_name": "string",             # Nome da sala
    "room_location": "string",         # Nome do local
    "manager_name": "string",          # Nome do responsável
    "manager_email": "string"          # Email do responsável
}
```

## 🛣️ Endpoints

### 📅 Bookings (Reservas)

#### **GET /api/bookings/**

Lista todas as reservas.

**Query Parameters:**

- `room_id` (string, opcional) - Filtrar por sala
- `manager_id` (string, opcional) - Filtrar por responsável
- `start_date` (datetime, opcional) - Filtrar por data início
- `end_date` (datetime, opcional) - Filtrar por data fim

**Response 200:**

```json
[
  {
    "id": "cm3h4k2l0000x0cl4a1b2c3d4",
    "room": "cm3h4k2l0000y0cl4a1b2c3d5",
    "manager": "cm3h4k2l0000z0cl4a1b2c3d6",
    "start_date": "2025-01-15T10:00:00Z",
    "end_date": "2025-01-15T12:00:00Z",
    "coffee_option": true,
    "coffee_quantity": 10,
    "coffee_description": "Café da manhã",
    "room_name": "Sala de Reunião A",
    "room_location": "Prédio Principal",
    "manager_name": "João Silva",
    "manager_email": "joao@empresa.com",
    "created_at": "2025-01-10T09:00:00Z",
    "updated_at": "2025-01-10T09:00:00Z"
  }
]
```

#### **POST /api/bookings/**

Cria uma nova reserva.

**Request Body:**

```json
{
  "room": "cm3h4k2l0000y0cl4a1b2c3d5",
  "manager": "cm3h4k2l0000z0cl4a1b2c3d6",
  "start_date": "2025-01-15T10:00:00Z",
  "end_date": "2025-01-15T12:00:00Z",
  "coffee_option": true,
  "coffee_quantity": 10,
  "coffee_description": "Café da manhã para reunião"
}
```

**Response 201:**

```json
{
  "id": "cm3h4k2l0000x0cl4a1b2c3d4",
  "room": "cm3h4k2l0000y0cl4a1b2c3d5",
  "manager": "cm3h4k2l0000z0cl4a1b2c3d6",
  "start_date": "2025-01-15T10:00:00Z",
  "end_date": "2025-01-15T12:00:00Z",
  "coffee_option": true,
  "coffee_quantity": 10,
  "coffee_description": "Café da manhã para reunião",
  "room_name": "Sala de Reunião A",
  "room_location": "Prédio Principal",
  "manager_name": "João Silva",
  "manager_email": "joao@empresa.com",
  "created_at": "2025-01-10T09:00:00Z",
  "updated_at": "2025-01-10T09:00:00Z"
}
```

**Response 400 - Dados Inválidos:**

```json
{
  "error": "Start date must be before end date"
}
```

**Response 409 - Conflito de Horário:**

```json
{
  "error": "Conflito de horário detectado na sala cm3h4k2l0000y0cl4a1b2c3d5. Reservas conflitantes: Reserva cm3h4k2l0000w0cl4a1b2c3d3 de 2025-01-15 09:00:00+00:00 até 2025-01-15 11:00:00+00:00"
}
```

#### **GET /api/bookings/{id}/**

Busca uma reserva específica.

**Response 200:**

```json
{
  "id": "cm3h4k2l0000x0cl4a1b2c3d4",
  "room": "cm3h4k2l0000y0cl4a1b2c3d5",
  "manager": "cm3h4k2l0000z0cl4a1b2c3d6",
  "start_date": "2025-01-15T10:00:00Z",
  "end_date": "2025-01-15T12:00:00Z",
  "coffee_option": true,
  "coffee_quantity": 10,
  "coffee_description": "Café da manhã",
  "room_name": "Sala de Reunião A",
  "room_location": "Prédio Principal",
  "manager_name": "João Silva",
  "manager_email": "joao@empresa.com",
  "created_at": "2025-01-10T09:00:00Z",
  "updated_at": "2025-01-10T09:00:00Z"
}
```

**Response 404:**

```json
{
  "error": "Booking not found"
}
```

#### **PUT /api/bookings/{id}/**

Atualiza uma reserva existente.

**Request Body:**

```json
{
  "start_date": "2025-01-15T14:00:00Z",
  "end_date": "2025-01-15T16:00:00Z",
  "coffee_quantity": 15
}
```

**Response 200:** (mesmo formato do GET)

**Response 409 - Conflito:**

```json
{
  "error": "Conflito de horário detectado..."
}
```

#### **DELETE /api/bookings/{id}/**

Exclui uma reserva (soft delete).

**Response 204:** (sem conteúdo)

**Response 404:**

```json
{
  "error": "Booking not found"
}
```

### 🔍 Endpoints Customizados

#### **GET /api/bookings/by_room/?room_id={id}**

Lista reservas de uma sala específica.

**Query Parameters:**

- `room_id` (string, obrigatório) - ID da sala

**Response 200:** Array de reservas da sala

**Response 400:**

```json
{
  "error": "room_id parameter is required"
}
```

#### **GET /api/bookings/by_manager/?manager_id={id}**

Lista reservas de um responsável específico.

**Query Parameters:**

- `manager_id` (string, obrigatório) - ID do responsável

**Response 200:** Array de reservas do responsável

#### **GET /api/reservations/**

Alias para `/api/bookings/` - mesma funcionalidade.

## ✅ Regras de Validação

### 📅 **Validação de Datas**

- `start_date` e `end_date` são obrigatórios
- `start_date` deve ser anterior a `end_date`
- Formato: ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`)

### ⚠️ **Validação de Conflitos**

- Não permite reservas sobrepostas na mesma sala
- Conflito detectado quando: `start_date < existing_end_date` E `end_date > existing_start_date`
- Em atualizações, exclui a própria reserva da verificação

### ☕ **Validação de Café**

- Se `coffee_option = true`, `coffee_quantity` é obrigatória
- `coffee_quantity` deve ser > 0
- `coffee_description` é sempre opcional

### 🆔 **Validação de IDs**

- Todos os IDs usam formato UUID/CUID
- `room` e `manager` devem referenciar registros existentes
- Registros com `deleted_at` não são válidos

## 🔢 Códigos de Status HTTP

| Código  | Significado           | Quando ocorre                          |
| ------- | --------------------- | -------------------------------------- |
| **200** | OK                    | Sucesso em GET, PUT                    |
| **201** | Created               | Reserva criada com sucesso             |
| **204** | No Content            | Reserva excluída com sucesso           |
| **400** | Bad Request           | Dados inválidos ou parâmetros faltando |
| **404** | Not Found             | Reserva não encontrada                 |
| **409** | Conflict              | Conflito de horário detectado          |
| **500** | Internal Server Error | Erro interno do servidor               |

## 💡 Exemplos de Uso

### **Criar uma reserva simples**

```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "room": "cm3h4k2l0000y0cl4a1b2c3d5",
    "manager": "cm3h4k2l0000z0cl4a1b2c3d6",
    "start_date": "2025-01-15T10:00:00Z",
    "end_date": "2025-01-15T12:00:00Z",
    "coffee_option": false
  }'
```

### **Listar reservas com filtros**

```bash
curl "http://localhost:8000/api/bookings/?room_id=cm3h4k2l0000y0cl4a1b2c3d5&start_date=2025-01-15"
```

### **Atualizar horário de uma reserva**

```bash
curl -X PUT http://localhost:8000/api/bookings/cm3h4k2l0000x0cl4a1b2c3d4/ \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-01-15T14:00:00Z",
    "end_date": "2025-01-15T16:00:00Z"
  }'
```

### **Buscar reservas de uma sala**

```bash
curl "http://localhost:8000/api/bookings/by_room/?room_id=cm3h4k2l0000y0cl4a1b2c3d5"
```

## 🛡️ Tratamento de Erros

Todos os erros retornam um objeto JSON com a chave `error`:

```json
{
  "error": "Descrição do erro aqui"
}
```

### **Tipos de Erro Comuns:**

1. **Validação de dados:** Status 400

   - "Start date must be before end date"
   - "Coffee quantity must be specified when coffee option is enabled"

2. **Conflito de horário:** Status 409

   - "Conflito de horário detectado na sala {room_id}. Reservas conflitantes: ..."

3. **Recurso não encontrado:** Status 404

   - "Booking not found"
   - "Selected room does not exist or is deleted"

4. **Parâmetros obrigatórios:** Status 400
   - "room_id parameter is required"

## 📈 Relacionamentos

```
Location (1) ←→ (N) Room (1) ←→ (N) Booking (N) ←→ (1) Manager
```

- **Location** → **Room**: Um local pode ter várias salas
- **Room** → **Booking**: Uma sala pode ter várias reservas
- **Manager** → **Booking**: Um responsável pode ter várias reservas
- **Booking**: Liga uma sala a um responsável em um período específico

---

**📝 Esta documentação está sempre atualizada com a versão mais recente da API.**

# 🚀 Back-end Django - Sistema de Reservas de Salas

## 📋 Arquitetura Implementada

Este projeto segue uma **arquitetura limpa** inspirada em **DDD + CQRS**, mas respeitando os padrões do Django:

### 📁 Estrutura de Camadas

```
api/
├── models/           # 🗂️ Entidades de domínio (Django ORM)
│   ├── location.py   # Local/Prédio
│   ├── room.py       # Sala
│   ├── manager.py    # Responsável
│   └── booking.py    # Reserva
│
├── repositories/     # 🔄 Acesso ao banco (CRUD)
│   └── booking_repository.py
│
├── services/         # 🧠 Regras de negócio
│   └── booking_service.py (validação de conflitos)
│
├── use_cases/        # 📋 CQRS - Commands & Queries
│   ├── create_booking.py    # Command
│   ├── list_bookings.py     # Query
│   ├── update_booking.py    # Command
│   └── delete_booking.py    # Command
│
├── serializers/      # 📤 Validação e estrutura da API
│   └── booking_serializer.py
│
├── views/           # 🌐 Controllers REST (DRF)
│   └── booking_view.py
│
├── tests/           # 🧪 Testes unitários
│   ├── test_services.py
│   ├── test_repositories.py
│   └── test_use_cases.py
│
└── urls.py          # 🛣️ Rotas da API
```

## 🔧 Configuração e Execução

### 1. **Instalar Dependências**

```bash
pip install -r requirements.txt
```

### 2. **Configurar Banco de Dados**

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. **Criar Superusuário**

```bash
python manage.py createsuperuser
```

### 4. **Executar Servidor**

```bash
python manage.py runserver
```

## 🌐 Endpoints da API

### **Reservas (Bookings)**

- `GET /api/bookings/` - Listar todas as reservas
- `POST /api/bookings/` - Criar nova reserva
- `GET /api/bookings/{id}/` - Buscar reserva específica
- `PUT /api/bookings/{id}/` - Atualizar reserva
- `DELETE /api/bookings/{id}/` - Excluir reserva (soft delete)

### **Filtros Customizados**

- `GET /api/bookings/by_room/?room_id={id}` - Reservas por sala
- `GET /api/bookings/by_manager/?manager_id={id}` - Reservas por responsável

### **Alias Alternativo**

- `GET /api/reservations/` - Mesmo que `/api/bookings/`

## 📝 Estrutura de Dados

### **Booking (Reserva)**

```json
{
  "id": "string",
  "room": "room_id",
  "manager": "manager_id",
  "start_date": "2025-01-01T10:00:00Z",
  "end_date": "2025-01-01T12:00:00Z",
  "coffee_option": false,
  "coffee_quantity": null,
  "coffee_description": null,
  "created_at": "2025-01-01T09:00:00Z",
  "updated_at": "2025-01-01T09:00:00Z"
}
```

## 🎯 Principais Regras de Negócio

### ⚠️ **Validação de Conflitos**

- **Não permite** reservas sobrepostas na mesma sala
- **Valida automaticamente** conflitos de horário
- **Retorna erro 409** em caso de conflito

### ☕ **Validação de Café**

- Se `coffee_option = true`, `coffee_quantity` é obrigatória
- Quantidade deve ser > 0

### 📅 **Validação de Datas**

- Data de início deve ser anterior à data de fim
- Ambas as datas são obrigatórias

## 🧪 Executar Testes

```bash
python manage.py test api.tests
```

### **Cobertura de Testes:**

- ✅ Services (regras de negócio)
- ✅ Repositories (CRUD)
- ✅ Use Cases (orquestração)
- ✅ Validação de conflitos

## 📚 Padrões Implementados

### **🔷 Repository Pattern**

- Encapsula acesso ao banco
- Métodos: `list()`, `get()`, `create()`, `update()`, `delete()`
- Método especial: `find_conflicts()` para validação

### **🔷 Service Layer**

- Contém todas as regras de negócio
- Método principal: `validate_conflict()`
- Validações: dados, conflitos, regras de domínio

### **🔷 CQRS Pattern**

- **Commands**: `CreateBookingUseCase`, `UpdateBookingUseCase`, `DeleteBookingUseCase`
- **Queries**: `ListBookingsUseCase`
- Separação clara entre leitura e escrita

### **🔷 Clean Architecture**

- Models → dados puros (ORM Django)
- Repositories → persistência
- Services → regras de negócio
- Use Cases → orquestração
- Views → controllers REST

## 🔍 Exemplos de Uso

### **Criar Reserva**

```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "room": "room_id_aqui",
    "manager": "manager_id_aqui",
    "start_date": "2025-01-01T10:00:00Z",
    "end_date": "2025-01-01T12:00:00Z",
    "coffee_option": true,
    "coffee_quantity": 10,
    "coffee_description": "Café da manhã"
  }'
```

### **Listar com Filtros**

```bash
curl "http://localhost:8000/api/bookings/?room_id=room123&start_date=2025-01-01"
```

## 🛠️ Tecnologias Utilizadas

- **Django 4.2.7** - Framework web
- **Django REST Framework 3.14.0** - API REST
- **PostgreSQL** - Banco de dados (configurável)
- **Factory Boy** - Testes com fixtures
- **pytest-django** - Testes unitários

---

**✨ Projeto criado seguindo Clean Architecture + DDD + CQRS com Django! ✨**

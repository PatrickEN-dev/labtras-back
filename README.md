# 🏢 Sistema de Reservas de Salas - Back-end

Sistema back-end em **Django + Django REST Framework** para gerenciar reservas de salas em diferentes locais/prédios, seguindo arquitetura limpa inspirada em **DDD + CQRS**.

## 🚀 Quick Start (Para Teste Técnico)

### **1. Clonar e Configurar**

```bash
git clone https://github.com/PatrickEN-dev/labtras-back.git
cd labtras-back

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependências (apenas as essenciais)
pip install Django==4.2.7 djangorestframework==3.14.0 python-decouple==3.8 django-cors-headers
```

### **2. Configurar Banco e Dados**

```bash
# Executar migrações
python manage.py migrate

# Popular banco com dados de teste (localizações, salas, gerentes)
python manage.py seed_data
```

### **3. Executar Servidor**

```bash
python manage.py runserver
```

**Pronto!** Servidor disponível em: **http://localhost:8000/**

### **4. Testar API**

- **Listar localizações:** `GET http://localhost:8000/api/locations/`
- **Listar salas:** `GET http://localhost:8000/api/rooms/`
- **Listar gerentes:** `GET http://localhost:8000/api/managers/`
- **Listar/criar reservas:** `GET|POST http://localhost:8000/api/bookings/`

✅ **Banco já populado** com 3 localizações, 13 salas e 5 gerentes para facilitar testes!

## 🧪 Executar Testes

```bash
python manage.py test api.tests --verbosity=2
```

## 🛠️ Tecnologias e Arquitetura

- **Django 4.2.7** + **Django REST Framework** - API REST
- **SQLite** - Banco de dados (pronto para uso)
- **Arquitetura Limpa** - DDD + CQRS pattern
- **CORS** configurado para frontend React

## 📁 Estrutura do Projeto

```
api/
├── 📁 models/           # Entities (Location, Room, Manager, Booking)
├── 📁 application/      # Use Cases + DTOs + Repository Interfaces
├── 📁 infrastructure/   # Repository Implementations + ViewSets
├── 📁 domain/          # Domain Services + Business Rules
└── 📁 management/      # Comandos Django (seed_data)
```

## 📚 Documentação Completa

- **[API_DOCS.md](./docs/API_DOCS.md)** - Endpoints e exemplos
- **[DOCKER_SETUP.md](./docs/DOCKER_SETUP.md)** - Setup completo com Docker
- **[SEED_SETUP.md](./docs/SEED_SETUP.md)** - Detalhes do comando seed

## 🔧 Comandos Úteis

```bash
# Limpar e recriar dados de teste
python manage.py seed_data --clear

# Resetar banco completamente
rm db.sqlite3
python manage.py migrate
python manage.py seed_data

# Rodar em porta diferente
python manage.py runserver 8080
```

---

**📧 Contato:** [Patrick](https://github.com/PatrickEN-dev)  
**🔗 Repositório:** [labtras-back](https://github.com/PatrickEN-dev/labtras-back)

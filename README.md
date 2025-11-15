# 🏢 Sistema de Reservas de Salas - Back-end

Sistema back-end em **Django + Django REST Framework** para gerenciar reservas de salas em diferentes locais/prédios, seguindo arquitetura limpa inspirada em **DDD + CQRS**.

## 📋 Pré-requisitos

- **Python 3.8+**
- **pip** (gerenciador de pacotes Python)
- **Git** (para clonar o repositório)

## 🚀 Instalação e Configuração

### 1. **Clonar o Repositório**

```bash
git clone https://github.com/PatrickEN-dev/labtras-back.git
cd labtras-back
```

### 2. **Criar Ambiente Virtual**

```bash
# Windows
python -m venv venv

# Linux/macOS
python3 -m venv venv
```

### 3. **Ativar o Ambiente Virtual**

```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 4. **Instalar Dependências**

```bash
pip install -r requirements.txt
```

### 5. **Configurar Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

### 6. **Executar Migrações**

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. **Criar Superusuário (Opcional)**

```bash
python manage.py createsuperuser
```

## ▶️ Executar o Projeto

### **🐳 Opção 1: Docker (Recomendado)**

```bash
# Clonar repositório
git clone https://github.com/PatrickEN-dev/labtras-back.git
cd labtras-back

# Configurar ambiente
cp .env.example .env

# Subir containers
docker-compose up -d
```

Servidor disponível em: **http://localhost:8000/**

📖 **Guia completo Docker:** [DOCKER_SETUP.md](./DOCKER_SETUP.md)

### **🐍 Opção 2: Ambiente Local**

#### **Modo Desenvolvimento**

```bash
python manage.py runserver
```

O servidor estará disponível em: **http://localhost:8000/**

### **Verificar se está funcionando**

Acesse: **http://localhost:8000/api/bookings/**

## 🧪 Executar Testes

```bash
# Todos os testes
python manage.py test

# Apenas testes da API
python manage.py test api.tests

# Com verbose
python manage.py test api.tests --verbosity=2
```

## 📁 Estrutura do Projeto

```
labtras-back/
├── 📁 core/              # Configurações Django
│   ├── settings.py       # Configurações principais
│   ├── urls.py          # URLs principais
│   └── wsgi.py          # WSGI application
├── 📁 api/              # App principal
│   ├── 📁 models/       # Modelos (Location, Room, Manager, Booking)
│   ├── 📁 repositories/ # Camada de dados
│   ├── 📁 services/     # Regras de negócio
│   ├── 📁 use_cases/    # CQRS - Commands & Queries
│   ├── 📁 serializers/  # Serializers DRF
│   ├── 📁 views/        # Views/Controllers
│   └── 📁 tests/        # Testes unitários
├── 📄 manage.py         # Django CLI
├── 📄 requirements.txt  # Dependências
└── 📄 API_DOCS.md      # Documentação da API
```

## 🛠️ Tecnologias Utilizadas

- **[Django 4.2.7](https://www.djangoproject.com/)** - Framework web
- **[Django REST Framework 3.14.0](https://www.django-rest-framework.org/)** - API REST
- **[PostgreSQL](https://www.postgresql.org/)** - Banco de dados (configurável)
- **[python-decouple](https://pypi.org/project/python-decouple/)** - Gerenciamento de variáveis
- **[django-cors-headers](https://pypi.org/project/django-cors-headers/)** - CORS para frontend

## 🌐 Endpoints Principais

- **`GET /api/bookings/`** - Listar reservas
- **`POST /api/bookings/`** - Criar reserva
- **`GET /api/bookings/{id}/`** - Buscar reserva
- **`PUT /api/bookings/{id}/`** - Atualizar reserva
- **`DELETE /api/bookings/{id}/`** - Excluir reserva

📖 **Documentação completa da API:** [API_DOCS.md](./API_DOCS.md)

## 🔧 Comandos Úteis

### **Resetar Banco de Dados**

```bash
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

### **Criar Nova Migration**

```bash
python manage.py makemigrations api
```

### **Shell Django (para testes)**

```bash
python manage.py shell
```

### **Coletar Arquivos Estáticos**

```bash
python manage.py collectstatic
```

## 📝 Banco de Dados

### **SQLite (Desenvolvimento)**

Configurado por padrão. O arquivo `db.sqlite3` será criado automaticamente.

### **PostgreSQL (Produção)**

Para usar PostgreSQL, configure a `DATABASE_URL` no `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/labtras_db
```

E instale o driver:

```bash
pip install psycopg2-binary
```

## 🐛 Solução de Problemas

### **Erro de Importação do Django**

```bash
# Certifique-se que o venv está ativado
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### **Erro de Migration**

```bash
python manage.py makemigrations --empty api
python manage.py migrate
```

### **Porta em Uso**

```bash
# Use outra porta
python manage.py runserver 8080
```

## 🔒 Produção

Para deploy em produção:

1. Configure `DEBUG=False` no `.env`
2. Configure `ALLOWED_HOSTS` adequadamente
3. Use PostgreSQL ou MySQL
4. Configure servidor web (Nginx + Gunicorn)
5. Configure HTTPS

## 👥 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m "Adiciona nova funcionalidade"`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

**📧 Contato:** [Patrick](https://github.com/PatrickEN-dev)  
**🔗 Repositório:** [labtras-back](https://github.com/PatrickEN-dev/labtras-back)

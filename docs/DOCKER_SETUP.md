# 🐳 Docker Setup - Sistema de Reservas

Guia completo para executar o projeto usando Docker e Docker Compose.

## 📋 Pré-requisitos

- **[Docker](https://www.docker.com/get-started)** instalado
- **[Docker Compose](https://docs.docker.com/compose/install/)** instalado
- **Git** (para clonar o repositório)

## 🚀 Execução Rápida (Desenvolvimento)

### 1. **Clonar e Configurar**

```bash
git clone https://github.com/PatrickEN-dev/labtras-back.git
cd labtras-back

# Copiar arquivo de exemplo
cp .env.example .env
```

### 2. **Subir os Containers**

```bash
docker-compose up -d
```

### 3. **Verificar**

- **API:** http://localhost:8000/api/bookings/
- **Admin:** http://localhost:8000/admin/
- **Database:** localhost:5432

## 🛠️ Comandos Úteis

### **Gerenciamento dos Containers**

```bash
# Subir containers
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Parar containers
docker-compose down

# Rebuild containers
docker-compose up --build -d

# Parar e remover volumes
docker-compose down -v
```

### **Django Commands no Container**

```bash
# Acessar shell do container
docker-compose exec web bash

# Executar migrations
docker-compose exec web python manage.py migrate

# Criar superuser
docker-compose exec web python manage.py createsuperuser

# Executar testes
docker-compose exec web python manage.py test

# Shell Django
docker-compose exec web python manage.py shell
```

### **Database Operations**

```bash
# Conectar ao PostgreSQL
docker-compose exec db psql -U labtras_user -d labtras_db

# Backup do banco
docker-compose exec db pg_dump -U labtras_user labtras_db > backup.sql

# Restore do banco
docker-compose exec -T db psql -U labtras_user labtras_db < backup.sql
```

## 📁 Arquivos Docker

### **`Dockerfile`** (Produção)

- Baseado em Python 3.11 slim
- Otimizado para produção com Gunicorn
- Health check configurado
- Usuário não-root para segurança

### **`Dockerfile.dev`** (Desenvolvimento)

- Hot reload ativado
- Volume mounting para desenvolvimento
- Servidor de desenvolvimento Django

### **`docker-compose.yml`** (Desenvolvimento)

```yaml
services:
  db: # PostgreSQL 15
  web: # Django App (porta 8000)
  redis: # Cache (opcional - porta 6379)
```

### **`docker-compose.prod.yml`** (Produção)

```yaml
services:
  db: # PostgreSQL
  web: # Django + Gunicorn
  nginx: # Reverse proxy (porta 80/443)
  redis: # Cache
```

## 🌐 Diferentes Ambientes

### **Desenvolvimento (Padrão)**

```bash
docker-compose up -d
```

- Usa `runserver` para hot reload
- Debug ativado
- Volumes montados para edição

### **Produção**

```bash
# Configurar .env para produção
cp .env.example .env.prod
nano .env.prod

# Usar compose de produção
docker-compose -f docker-compose.prod.yml up -d
```

- Usa Gunicorn + Nginx
- Debug desativado
- SSL configurável
- Volumes persistentes

### **Desenvolvimento com Build Customizado**

```bash
# Usar Dockerfile.dev
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

## 📊 Serviços Inclusos

| Serviço   | Porta  | Descrição            |
| --------- | ------ | -------------------- |
| **web**   | 8000   | Django API REST      |
| **db**    | 5432   | PostgreSQL 15        |
| **redis** | 6379   | Cache (opcional)     |
| **nginx** | 80/443 | Reverse proxy (prod) |

## 🔧 Configuração de Ambiente

### **Variáveis do `.env`:**

```env
# Database
POSTGRES_DB=labtras_db
POSTGRES_USER=labtras_user
POSTGRES_PASSWORD=sua_senha_aqui

# Django
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database URL
DATABASE_URL=postgresql://labtras_user:sua_senha_aqui@db:5432/labtras_db
```

## 🚨 Troubleshooting

### **Problemas Comuns:**

#### **1. Erro de conexão com banco**

```bash
# Verificar se o PostgreSQL subiu
docker-compose logs db

# Recriar volumes
docker-compose down -v
docker-compose up -d
```

#### **2. Erro de migrations**

```bash
# Fazer migrations manualmente
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

#### **3. Erro de permissões**

```bash
# No Linux/macOS
sudo chown -R $USER:$USER .
```

#### **4. Porta já em uso**

```bash
# Verificar processos usando a porta
lsof -i :8000

# Ou mudar porta no docker-compose.yml
ports:
  - "8080:8000"
```

#### **5. Container não inicia**

```bash
# Ver logs detalhados
docker-compose logs web

# Rebuild forçado
docker-compose build --no-cache web
docker-compose up -d
```

## 🔒 Segurança (Produção)

### **Checklist:**

- [ ] Alterar `SECRET_KEY` no `.env`
- [ ] Configurar `DEBUG=False`
- [ ] Definir `ALLOWED_HOSTS` corretos
- [ ] Usar senhas fortes no PostgreSQL
- [ ] Configurar SSL/HTTPS no Nginx
- [ ] Implementar backup automático
- [ ] Configurar monitoramento

### **SSL/HTTPS Setup:**

```bash
# Gerar certificados SSL
mkdir ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ssl/nginx-selfsigned.key \
    -out ssl/nginx-selfsigned.crt

# Usar docker-compose.prod.yml com nginx configurado
```

## 📈 Monitoramento

### **Health Checks:**

```bash
# Verificar saúde dos containers
docker-compose ps

# Health check manual
curl http://localhost:8000/api/bookings/
```

### **Logs Centralizados:**

```bash
# Todos os logs
docker-compose logs -f

# Apenas web
docker-compose logs -f web

# Últimas 100 linhas
docker-compose logs --tail=100 web
```

## 🔄 CI/CD Pipeline

### **Exemplo GitHub Actions:**

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          docker-compose -f docker-compose.prod.yml build
          docker-compose -f docker-compose.prod.yml up -d
```

---

**🐳 Projeto dockerizado com sucesso! Use `docker-compose up -d` e comece a desenvolver!**

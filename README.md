# Sistema de Reservas de Salas

Sistema para gerenciar reservas de salas em diferentes locais/prédios.

## 📊 Estrutura do Banco de Dados

### Models / Tabelas

#### 1. Local

Representa os prédios ou locais onde as salas estão.

**Campos:**

- `id` (PK, int, auto-increment)
- `nome` (string, obrigatório)
- `endereco` (string, opcional)
- `descricao` (string, opcional)
- `created_at` (datetime)
- `updated_at` (datetime)

#### 2. Sala

Cada sala pertence a um Local.

**Campos:**

- `id` (PK, int, auto-increment)
- `nome` (string, obrigatório)
- `capacidade` (int, opcional)
- `local_id` (FK → Local.id)
- `descricao` (string, opcional)
- `created_at` (datetime)
- `updated_at` (datetime)

#### 3. Responsavel

Representa a pessoa responsável pela reserva. Pode ser um usuário do sistema.

**Campos:**

- `id` (PK, int, auto-increment)
- `nome` (string, obrigatório)
- `email` (string, obrigatório, único)
- `telefone` (string, opcional)
- `created_at` (datetime)
- `updated_at` (datetime)

#### 4. Reserva

Representa a reserva de uma sala.

**Campos:**

- `id` (PK, int, auto-increment)
- `sala_id` (FK → Sala.id)
- `responsavel_id` (FK → Responsavel.id)
- `data_inicio` (datetime, obrigatório)
- `data_fim` (datetime, obrigatório)
- `opcao_cafe` (boolean, padrão false)
- `quantidade_cafe` (int, opcional)
- `descricao_cafe` (string, opcional)
- `created_at` (datetime)
- `updated_at` (datetime)

## 🔗 Relações

- **Um Local** tem **várias Salas** (1:N)
- **Uma Sala** pertence a **um Local** (N:1)
- **Uma Reserva** está ligada a **uma Sala** e a **um Responsável** (N:1)
- **Um Responsável** pode ter **várias Reservas** (1:N)

## 📈 Diagrama de Relacionamentos

```
Local (1) ←→ (N) Sala (1) ←→ (N) Reserva (N) ←→ (1) Responsavel
```

## 🛠 Ferramentas para Criar Diagramas

### **Gratuitas:**

- **[dbdiagram.io](https://dbdiagram.io/)** - Excelente para diagramas ER, sintaxe simples
- **[Lucidchart](https://www.lucidchart.com/)** - Versão gratuita limitada
- **[Draw.io (app.diagrams.net)](https://app.diagrams.net/)** - Totalmente gratuito
- **[QuickDBD](https://www.quickdatabasediagrams.com/)** - Criação rápida de diagramas
- **[Mermaid Live Editor](https://mermaid.live/)** - Para diagramas em código

### **Pagas:**

- **[MySQL Workbench](https://www.mysql.com/products/workbench/)** - Gratuito para MySQL
- **[Vertabelo](https://vertabelo.com/)** - Especializado em modelagem de dados
- **[SqlDBM](https://sqldbm.com/)** - Modelagem visual de banco de dados

### **Recomendação:**

Para este projeto, recomendo o **[dbdiagram.io](https://dbdiagram.io/)** pela facilidade de uso e qualidade dos diagramas gerados.

## 📝 Código DBML para dbdiagram.io

```dbml
// Use DBML to define your database structure
// Sistema de Reservas de Salas
// Docs: https://dbml.dbdiagram.io/docs

Table locais {
  id integer [primary key]
  nome varchar [not null]
  endereco varchar
  descricao text
  created_at timestamp
  updated_at timestamp
}

Table salas {
  id integer [primary key]
  nome varchar [not null]
  capacidade integer
  local_id integer [not null]
  descricao text
  created_at timestamp
  updated_at timestamp
}

Table responsaveis {
  id integer [primary key]
  nome varchar [not null]
  email varchar [not null, unique]
  telefone varchar
  created_at timestamp
  updated_at timestamp
}

Table reservas {
  id integer [primary key]
  sala_id integer [not null]
  responsavel_id integer [not null]
  data_inicio timestamp [not null]
  data_fim timestamp [not null]
  opcao_cafe boolean [default: false]
  quantidade_cafe integer
  descricao_cafe text [note: 'Descrição do serviço de café']
  created_at timestamp
  updated_at timestamp
}

// Relacionamentos
Ref local_salas: salas.local_id > locais.id // many-to-one

Ref sala_reservas: reservas.sala_id > salas.id // many-to-one

Ref responsavel_reservas: reservas.responsavel_id > responsaveis.id // many-to-one
```

## 🚀 Como usar o dbdiagram.io

1. Acesse [dbdiagram.io](https://dbdiagram.io/)
2. Cole o **código DBML** acima no editor
3. O diagrama será gerado automaticamente com os relacionamentos
4. Você pode exportar como PNG, PDF ou SQL

### 📋 Instruções detalhadas:

- Copie todo o bloco de código DBML (incluindo os comentários)
- No dbdiagram.io, delete o conteúdo de exemplo e cole nosso código
- Os relacionamentos aparecerão como linhas conectando as tabelas
- Use as opções de exportação para salvar o diagrama

---

_Sistema desenvolvido para gerenciar reservas de salas com facilidade e eficiência._

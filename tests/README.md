# 🧪 Testes da API LabTrans

Este diretório contém os testes essenciais para validar as funcionalidades da API LabTrans.

## 📋 Arquivos de Teste

### `test_api.py`

- **Descrição**: Teste principal da API
- **Escopo**: Testa todas as funcionalidades principais da API
- **Como executar**: `python tests/test_api.py`

### `test_final_success.py` ⭐ **[VALIDAÇÃO DOS NOVOS CAMPOS]**

- **Descrição**: Teste de validação dos campos name e description
- **Escopo**: Valida a implementação correta dos novos campos obrigatórios e opcionais
- **Funcionalidades testadas**:
  - Campo `name` obrigatório
  - Campo `description` opcional
  - Validações de entrada
  - Criação de bookings com novos campos
- **Como executar**: `python tests/test_final_success.py`

### `test_repo.py`

- **Descrição**: Teste do repositório
- **Escopo**: Testa as funcionalidades específicas do repositório
- **Como executar**: `python tests/test_repo.py`

## 🚀 Como Executar os Testes

### Pré-requisitos

```bash
# Ativar o ambiente virtual
.\venv\Scripts\Activate.ps1

# Certificar que o servidor está rodando
python manage.py runserver
```

### Execução dos Testes

```bash
# 1. Teste principal da API
python tests/test_api.py

# 2. Teste dos campos name/description (RECOMENDADO)
python tests/test_final_success.py

# 3. Teste do repositório
python tests/test_repo.py
```

## 📊 Estrutura dos Testes

Os testes estão organizados para cobrir:

1. **Funcionalidades básicas da API** (`test_api.py`)
2. **Novos campos implementados** (`test_final_success.py`)
3. **Camada de repositório** (`test_repo.py`)

## ✅ Validações dos Novos Campos

O arquivo `test_final_success.py` valida especificamente:

- ❌ **Booking sem `name`**: Retorna erro 400 (campo obrigatório)
- ✅ **Booking só com `name`**: Criação bem-sucedida
- ✅ **Booking com `name` + `description`**: Criação completa
- ✅ **Integração com coffee service**: Funcionalidade mantida
- ✅ **Detecção de conflitos**: Sistema de horários funcionando

## 📝 Notas Importantes

- Certifique-se de que o servidor Django esteja rodando antes de executar os testes
- Os testes utilizam dados padrão criados pelo comando `python manage.py seed_data`
- Todos os testes são independentes e podem ser executados separadamente
- O `test_final_success.py` é o teste mais importante para validar a implementação dos campos `name` e `description`

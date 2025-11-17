# Seed de Dados - Labtras Backend

Este documento explica como usar o comando de seed para popular o banco de dados com dados iniciais.

## Sobre o Seed

O comando `seed_data` popula o banco de dados com:

- ✅ 3 Localizações (Prédio Principal, Anexo Administrativo, Centro de Treinamento)
- ✅ 13 Salas distribuídas entre as localizações
- ✅ 5 Gerentes prontos para fazer reservas
- ❌ Nenhuma reserva (para que você possa criar livremente)

Os dados são baseados nos mocks do frontend, garantindo consistência entre front e back.

## Como usar

### 1. Executar o seed (primeira vez)

```bash
python manage.py seed_data
```

### 2. Limpar e recriar os dados

```bash
python manage.py seed_data --clear
```

### 3. Verificar se existem dados

Se você tentar executar o seed quando já existem dados, receberá um aviso:

```
Dados já existem no banco. Use --clear para limpar antes de popular.
```

## Estrutura dos Dados

### Localizações

1. **Prédio Principal** - Rua das Empresas, 123 - Centro
2. **Anexo Administrativo** - Rua das Empresas, 125 - Centro
3. **Centro de Treinamento** - Av. do Conhecimento, 456 - Tech Park

### Salas por Localização

#### Prédio Principal (5 salas)

- Sala de Reunião A (10 pessoas)
- Sala de Reunião B (6 pessoas)
- Auditório Principal (50 pessoas)
- Sala Íntima (2 pessoas)
- Sala Média (12 pessoas)

#### Anexo Administrativo (4 salas)

- Sala de Conferência (15 pessoas)
- Sala de Brainstorming (8 pessoas)
- Sala Pequena (4 pessoas)
- Sala Executive (8 pessoas)

#### Centro de Treinamento (4 salas)

- Laboratório de Informática (20 pessoas)
- Sala de Workshop (25 pessoas)
- Sala Grande (30 pessoas)
- Sala de Apresentação (40 pessoas)

### Gerentes

1. **João Silva** - joao.silva@empresa.com - (11) 9876-5432
2. **Maria Santos** - maria.santos@empresa.com - (11) 9876-5433
3. **Pedro Oliveira** - pedro.oliveira@empresa.com - (11) 9876-5434
4. **Ana Costa** - ana.costa@empresa.com - (11) 9876-5435
5. **Carlos Ferreira** - carlos.ferreira@empresa.com - (11) 9876-5436

## Vantagens

✅ **Desenvolvimento mais rápido**: Não precisa criar localizações, salas e gerentes manualmente  
✅ **Dados consistentes**: Mesmos dados do frontend para testes  
✅ **Foco no booking**: Vai direto para a funcionalidade principal  
✅ **Fácil reset**: Comando --clear para recomeçar  
✅ **Dados realistas**: Nomes, emails e telefones plausíveis

## Próximos Passos

Após executar o seed, você pode:

1. Usar a API para listar localizações: `GET /api/locations/`
2. Usar a API para listar salas: `GET /api/rooms/`
3. Usar a API para listar gerentes: `GET /api/managers/`
4. Criar bookings facilmente usando os IDs das salas e gerentes criados

---

**Dica**: Execute o seed sempre que quiser um ambiente limpo para testes!

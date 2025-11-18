# Guia de Integração Frontend - Endpoints de Dados Padronizados

## 📋 Problema Resolvido

O frontend estava tentando criar dados que já existiam no banco, gerando erros de duplicação. Para resolver isso, criamos endpoints especiais que **sempre retornam os mesmos dados padronizados**, seja criando novos ou retornando existentes.

## 🎯 Solução: Endpoints Get-or-Create-Default

### 📍 Location Padrão

**Endpoint:** `POST /api/locations/get-or-create-default/`

**Dados retornados:**

```json
{
  "created": false, // true se foi criado, false se já existia
  "location": {
    "id": "04f51fa5-e6b7-4b3d-9f22-663f0a79be80",
    "name": "Matriz - Centro",
    "address": "Av. Principal, 123, Centro",
    "description": "Edifício corporativo principal",
    "created_at": "2025-11-18T20:05:59.726032+00:00",
    "updated_at": "2025-11-18T20:05:59.726070+00:00"
  }
}
```

### 👤 Manager Padrão

**Endpoint:** `POST /api/managers/get-or-create-default/`

**Dados retornados:**

```json
{
  "created": false,
  "manager": {
    "id": "10a9f81f-6680-4e40-a54e-828ef05e43d1",
    "name": "João Silva",
    "email": "joao.silva@empresa.com",
    "phone": "(11) 99999-1111",
    "created_at": "2025-11-17T23:18:31.589363+00:00",
    "updated_at": "2025-11-17T23:18:31.589377+00:00"
  }
}
```

### 🏢 Room Padrão

**Endpoint:** `POST /api/rooms/get-or-create-default/`

**Dados retornados:**

```json
{
  "created": false,
  "room": {
    "id": "7c5ca1c9-7492-42cd-af08-f5b0ee48bfb1",
    "name": "Sala de Reunião B",
    "capacity": 12,
    "description": "Sala média para reuniões em grupo",
    "location_id": "04f51fa5-e6b7-4b3d-9f22-663f0a79be80",
    "created_at": "2025-11-18T20:05:59.797484+00:00",
    "updated_at": "2025-11-18T20:05:59.797523+00:00"
  }
}
```

## 🔄 Fluxo de Integração Frontend

### 1. Inicialização da Aplicação

Ao carregar o frontend, chame estes endpoints para garantir que os dados padrão existem:

```javascript
// 1. Garantir location padrão
const locationResponse = await fetch("/api/locations/get-or-create-default/", {
  method: "POST",
});
const locationData = await locationResponse.json();
const defaultLocationId = locationData.location.id;

// 2. Garantir manager padrão
const managerResponse = await fetch("/api/managers/get-or-create-default/", {
  method: "POST",
});
const managerData = await managerResponse.json();
const defaultManagerId = managerData.manager.id;

// 3. Garantir room padrão
const roomResponse = await fetch("/api/rooms/get-or-create-default/", {
  method: "POST",
});
const roomData = await roomResponse.json();
const defaultRoomId = roomData.room.id;
```

### 2. Criação de Booking

Use os IDs obtidos para criar bookings:

```javascript
const bookingData = {
  room: defaultRoomId, // ID da room padrão
  manager: defaultManagerId, // ID do manager padrão
  start_datetime: "2025-11-20T09:00:00Z",
  end_datetime: "2025-11-20T10:00:00Z",
  purpose: "Reunião de Planejamento",
};

const bookingResponse = await fetch("/api/bookings/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(bookingData),
});
```

## ✅ Vantagens desta Solução

1. **Sem erros de duplicação**: Os endpoints sempre retornam dados válidos
2. **Consistência**: Mesmos dados padrão em todas as execuções
3. **Simplicidade**: Frontend não precisa se preocupar com validações de existência
4. **Performance**: Se já existe, retorna imediatamente sem criar novo
5. **Idempotência**: Pode ser chamado múltiplas vezes com segurança

## 🎯 Status dos Endpoints

- ✅ `POST /api/locations/get-or-create-default/` - **Implementado e Testado**
- ✅ `POST /api/managers/get-or-create-default/` - **Implementado e Testado**
- ✅ `POST /api/rooms/get-or-create-default/` - **Implementado e Testado**

**Resultado:** Todos sempre retornam `created: false` nas execuções subsequentes, confirmando que reutilizam dados existentes.

## 🚀 Próximos Passos

1. **Frontend**: Substituir as chamadas diretas aos endpoints de criação pelos novos endpoints `get-or-create-default`
2. **Booking**: Usar os IDs retornados para criar reservas
3. **Teste**: Validar o fluxo completo de criação de booking

Esta solução garante que seu frontend sempre tenha dados consistentes para trabalhar! 🎉

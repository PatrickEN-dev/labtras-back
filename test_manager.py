#!/usr/bin/env python3
"""
Teste específico para Manager
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"


def test_manager():
    print("🧪 Testando criação de Manager...")

    manager_data = {
        "name": "João Silva",
        "email": "joao@test.com",
        "phone": "(11) 98765-4321",
    }

    print(f"Dados: {json.dumps(manager_data, indent=2)}")

    response = requests.post(f"{BASE_URL}/managers/", json=manager_data)
    print(f"Status: {response.status_code}")

    if response.status_code == 201:
        print("✅ Manager criado com sucesso!")
        print(json.dumps(response.json(), indent=2))
    else:
        print("❌ Erro na criação:")
        try:
            error = response.json()
            print(json.dumps(error, indent=2))
        except:
            print(response.text)


if __name__ == "__main__":
    test_manager()

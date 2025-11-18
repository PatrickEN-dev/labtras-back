#!/usr/bin/env python3
"""
Script simples para testar a API de locations
"""
import requests
import json


def test_locations():
    base_url = "http://127.0.0.1:8000/api/locations/"

    print("🧪 Testando API de Locations\n")

    # 1. Listar locations existentes
    print("📋 Listando locations...")
    response = requests.get(base_url)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        locations = response.json()
        print(f"✅ {len(locations)} locations encontradas")
        for loc in locations:
            print(f"  - {loc['name']} (ID: {loc['id']})")
    else:
        print(f"❌ Erro ao listar: {response.text}")

    print("\n" + "=" * 50 + "\n")

    # 2. Criar uma nova location (apenas name - obrigatório)
    print("➕ Criando nova location...")
    new_location = {"name": "Laboratório Teste API"}

    response = requests.post(base_url, json=new_location)
    print(f"Status: {response.status_code}")

    if response.status_code == 201:
        created = response.json()
        print("✅ Location criada com sucesso!")
        print(f"   ID: {created['id']}")
        print(f"   Nome: {created['name']}")
        print(f"   Criado em: {created['created_at']}")
    else:
        print(f"❌ Erro ao criar: {response.text}")

    print("\n" + "=" * 50 + "\n")

    # 3. Criar location com dados completos
    print("➕ Criando location com dados completos...")
    complete_location = {
        "name": "Lab Completo",
        "address": "Rua da Ciência, 456",
        "description": "Laboratório para pesquisa avançada",
    }

    response = requests.post(base_url, json=complete_location)
    print(f"Status: {response.status_code}")

    if response.status_code == 201:
        created = response.json()
        print("✅ Location completa criada!")
        print(json.dumps(created, indent=2, ensure_ascii=False))
    else:
        print(f"❌ Erro ao criar: {response.text}")


if __name__ == "__main__":
    try:
        test_locations()
    except Exception as e:
        print(f"💥 Erro no teste: {e}")

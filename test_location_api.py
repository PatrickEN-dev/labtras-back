#!/usr/bin/env python3
"""
Script para testar a criação de location via API
"""
import requests
import json

# URL da API
BASE_URL = "http://127.0.0.1:8000/api"


def test_create_location():
    """Testa a criação de uma nova location"""
    url = f"{BASE_URL}/locations/"

    # Dados para criar a location - apenas com name (obrigatório)
    data = {
        "name": "Laboratório de Testes",
        "address": "Rua das Flores, 123",
        "description": "Laboratório para testes automatizados",
    }

    print("🧪 Testando criação de location...")
    print(f"URL: {url}")
    print(f"Dados: {json.dumps(data, indent=2)}")

    try:
        response = requests.post(url, json=data)

        print(f"\n📊 Resultado:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")

        if response.status_code == 201:
            result = response.json()
            print(f"✅ Location criada com sucesso!")
            print(f"Resultado: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Erro na criação:")
            try:
                error = response.json()
                print(f"Erro: {json.dumps(error, indent=2)}")
            except:
                print(f"Resposta: {response.text}")

    except Exception as e:
        print(f"💥 Erro na requisição: {e}")


def test_create_location_minimal():
    """Testa a criação de location apenas com name"""
    url = f"{BASE_URL}/locations/"

    # Dados mínimos
    data = {"name": "Lab Simples"}

    print("\n🧪 Testando criação de location com dados mínimos...")
    print(f"Dados: {json.dumps(data, indent=2)}")

    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            print(f"✅ Location criada com sucesso!")
            print(f"Resultado: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Erro na criação:")
            try:
                error = response.json()
                print(f"Erro: {json.dumps(error, indent=2)}")
            except:
                print(f"Resposta: {response.text}")

    except Exception as e:
        print(f"💥 Erro na requisição: {e}")


def test_list_locations():
    """Testa a listagem de locations"""
    url = f"{BASE_URL}/locations/"

    print("\n📋 Testando listagem de locations...")

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Locations listadas com sucesso!")
            print(f"Total: {len(result)} locations")
            print(f"Resultado: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Erro na listagem:")
            try:
                error = response.json()
                print(f"Erro: {json.dumps(error, indent=2)}")
            except:
                print(f"Resposta: {response.text}")

    except Exception as e:
        print(f"💥 Erro na requisição: {e}")


if __name__ == "__main__":
    print("🚀 Iniciando testes da API de Locations\n")

    # Primeiro, vamos listar locations existentes
    test_list_locations()

    # Testar criação com dados completos
    test_create_location()

    # Testar criação com dados mínimos
    test_create_location_minimal()

    # Listar novamente para ver as novas
    test_list_locations()

    print("\n🏁 Testes concluídos!")

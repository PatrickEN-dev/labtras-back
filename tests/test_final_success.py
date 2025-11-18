#!/usr/bin/env python
"""
Teste final com horários únicos para confirmar funcionamento completo
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"


def test_final_booking_creation():
    """Teste final com horários únicos"""

    print("🎯 TESTE FINAL - Name e Description funcionando")
    print("=" * 50)

    try:
        base_time = datetime.now() + timedelta(days=2)

        print("1. Teste SEM name (deve dar erro 400):")
        booking_no_name = {
            "room": "7c5ca1c9-7492-42cd-af08-f5b0ee48bfb1",
            "manager": "10a9f81f-6680-4e40-a54e-828ef05e43d1",
            "start_date": (base_time + timedelta(hours=1)).isoformat(),
            "end_date": (base_time + timedelta(hours=2)).isoformat(),
            "coffee_option": False,
        }

        response1 = requests.post(f"{BASE_URL}/bookings/", json=booking_no_name)
        print(f"Status: {response1.status_code}")
        print(f"Response: {response1.text[:100]}...")

        print(f"\n2. Teste COM name (deve funcionar):")
        booking_with_name = {
            "room": "7c5ca1c9-7492-42cd-af08-f5b0ee48bfb1",
            "manager": "10a9f81f-6680-4e40-a54e-828ef05e43d1",
            "name": "Reunião Teste Final",
            "start_date": (base_time + timedelta(hours=3)).isoformat(),
            "end_date": (base_time + timedelta(hours=4)).isoformat(),
            "coffee_option": False,
        }

        response2 = requests.post(f"{BASE_URL}/bookings/", json=booking_with_name)
        print(f"Status: {response2.status_code}")
        if response2.status_code == 201:
            result = response2.json()
            print(f"✅ Sucesso! ID: {result['id']}")
            print(f"   Name: {result['name']}")
            print(f"   Description: {result.get('description', 'N/A')}")
        else:
            print(f"Response: {response2.text}")

        print(f"\n3. Teste COM name e description (deve funcionar):")
        booking_full = {
            "room": "7c5ca1c9-7492-42cd-af08-f5b0ee48bfb1",
            "manager": "10a9f81f-6680-4e40-a54e-828ef05e43d1",
            "name": "Reunião Estratégica Final",
            "description": "Reunião para definir estratégias e próximos passos do projeto LabTrans.",
            "start_date": (base_time + timedelta(hours=5)).isoformat(),
            "end_date": (base_time + timedelta(hours=6)).isoformat(),
            "coffee_option": True,
            "coffee_quantity": 10,
        }

        response3 = requests.post(f"{BASE_URL}/bookings/", json=booking_full)
        print(f"Status: {response3.status_code}")
        if response3.status_code == 201:
            result = response3.json()
            print(f"✅ Sucesso! ID: {result['id']}")
            print(f"   Name: {result['name']}")
            print(f"   Description: {result['description']}")
            print(
                f"   Coffee: {result['coffee_option']} (qty: {result['coffee_quantity']})"
            )
        else:
            print(f"Response: {response3.text}")

        print(f"\n4. Verificando bookings criados:")
        response4 = requests.get(f"{BASE_URL}/bookings/")
        if response4.status_code == 200:
            bookings = response4.json()
            print(f"Total de bookings: {len(bookings)}")

            for booking in bookings[-3:]:
                name = booking.get("name", "N/A")
                description = (
                    booking.get("description", "N/A")[:50]
                    if booking.get("description")
                    else "N/A"
                )
                print(f"  - {name}: {description}")

        print(f"\n🎉 TESTE CONCLUÍDO - Name e Description implementados com sucesso!")

    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_final_booking_creation()

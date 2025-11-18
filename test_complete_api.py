#!/usr/bin/env python3
"""
Teste completo de todas as rotas da API LabTrans
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/api"


class APITester:
    def __init__(self):
        self.created_items = {
            "locations": [],
            "managers": [],
            "rooms": [],
            "bookings": [],
        }

    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🔥 {title}")
        print(f"{'='*60}")

    def print_result(self, method, url, status, data=None, error=None):
        emoji = "✅" if 200 <= status < 300 else "❌"
        print(f"{emoji} {method} {url.replace(BASE_URL, '')} - Status: {status}")

        if error:
            print(f"   Erro: {error}")
        elif data and isinstance(data, dict):
            if "id" in data:
                print(f"   ID: {data['id']}")
            if "name" in data:
                print(f"   Nome: {data['name']}")
        elif data and isinstance(data, list):
            print(f"   Items: {len(data)}")

    def test_locations(self):
        self.print_header("TESTANDO LOCATIONS")

        # 1. Listar locations
        response = requests.get(f"{BASE_URL}/locations/")
        self.print_result(
            "GET",
            f"{BASE_URL}/locations/",
            response.status_code,
            response.json() if response.status_code == 200 else None,
        )

        timestamp = datetime.now().strftime("%H%M%S")
        location_data = {"name": f"Laboratório Principal {timestamp}"}
        response = requests.post(f"{BASE_URL}/locations/", json=location_data)
        if response.status_code == 201:
            created_location = response.json()
            self.created_items["locations"].append(created_location)
            self.print_result(
                "POST", f"{BASE_URL}/locations/", response.status_code, created_location
            )
        else:
            self.print_result(
                "POST",
                f"{BASE_URL}/locations/",
                response.status_code,
                error=response.text,
            )

        location_complete = {
            "name": f"Centro de Pesquisa Avançada {timestamp}",
            "address": "Av. das Ciências, 1000",
            "description": "Centro dedicado à pesquisa em tecnologia avançada",
        }
        response = requests.post(f"{BASE_URL}/locations/", json=location_complete)
        if response.status_code == 201:
            created_location = response.json()
            self.created_items["locations"].append(created_location)
            self.print_result(
                "POST", f"{BASE_URL}/locations/", response.status_code, created_location
            )

        # 4. Buscar location por ID
        if self.created_items["locations"]:
            location_id = self.created_items["locations"][0]["id"]
            response = requests.get(f"{BASE_URL}/locations/{location_id}/")
            self.print_result(
                "GET",
                f"{BASE_URL}/locations/{location_id}/",
                response.status_code,
                response.json() if response.status_code == 200 else None,
            )

        # 5. Atualizar location
        if self.created_items["locations"]:
            location_id = self.created_items["locations"][0]["id"]
            update_data = {
                "description": "Laboratório atualizado com novos equipamentos"
            }
            response = requests.patch(
                f"{BASE_URL}/locations/{location_id}/", json=update_data
            )
            self.print_result(
                "PATCH",
                f"{BASE_URL}/locations/{location_id}/",
                response.status_code,
                response.json() if response.status_code == 200 else None,
            )

    def test_managers(self):
        self.print_header("TESTANDO MANAGERS")

        # 1. Listar managers
        response = requests.get(f"{BASE_URL}/managers/")
        self.print_result(
            "GET",
            f"{BASE_URL}/managers/",
            response.status_code,
            response.json() if response.status_code == 200 else None,
        )

        # 2. Criar manager
        timestamp = datetime.now().strftime("%H%M%S")
        manager_data = {
            "name": "João Silva",
            "email": f"joao{timestamp}@labtrans.com",
            "phone": "(11) 98765-4321",
        }
        response = requests.post(f"{BASE_URL}/managers/", json=manager_data)
        if response.status_code == 201:
            created_manager = response.json()
            self.created_items["managers"].append(created_manager)
            self.print_result(
                "POST", f"{BASE_URL}/managers/", response.status_code, created_manager
            )
        else:
            self.print_result(
                "POST",
                f"{BASE_URL}/managers/",
                response.status_code,
                error=response.text,
            )

        # 3. Criar outro manager
        manager_data2 = {
            "name": "Maria Santos",
            "email": f"maria{timestamp}@labtrans.com",
        }
        response = requests.post(f"{BASE_URL}/managers/", json=manager_data2)
        if response.status_code == 201:
            created_manager = response.json()
            self.created_items["managers"].append(created_manager)
            self.print_result(
                "POST", f"{BASE_URL}/managers/", response.status_code, created_manager
            )

    def test_rooms(self):
        self.print_header("TESTANDO ROOMS")

        # 1. Listar rooms
        response = requests.get(f"{BASE_URL}/rooms/")
        self.print_result(
            "GET",
            f"{BASE_URL}/rooms/",
            response.status_code,
            response.json() if response.status_code == 200 else None,
        )

        if not self.created_items["locations"]:
            print("❌ Não é possível criar rooms sem locations")
            return

        # 2. Criar room
        location_id = self.created_items["locations"][0]["id"]
        room_data = {
            "name": "Sala de Reuniões A",
            "location": location_id,
            "capacity": 10,
        }
        response = requests.post(f"{BASE_URL}/rooms/", json=room_data)
        if response.status_code == 201:
            created_room = response.json()
            self.created_items["rooms"].append(created_room)
            self.print_result(
                "POST", f"{BASE_URL}/rooms/", response.status_code, created_room
            )
        else:
            self.print_result(
                "POST", f"{BASE_URL}/rooms/", response.status_code, error=response.text
            )

        # 3. Criar room completa
        room_complete = {
            "name": "Laboratório de Química",
            "location": location_id,
            "capacity": 25,
            "description": "Laboratório equipado com bancadas e equipamentos de segurança",
            "equipment": "Capelas, balanças analíticas, estufas",
        }
        response = requests.post(f"{BASE_URL}/rooms/", json=room_complete)
        if response.status_code == 201:
            created_room = response.json()
            self.created_items["rooms"].append(created_room)
            self.print_result(
                "POST", f"{BASE_URL}/rooms/", response.status_code, created_room
            )

    def test_bookings(self):
        self.print_header("TESTANDO BOOKINGS")

        # 1. Listar bookings
        response = requests.get(f"{BASE_URL}/bookings/")
        self.print_result(
            "GET",
            f"{BASE_URL}/bookings/",
            response.status_code,
            response.json() if response.status_code == 200 else None,
        )

        if not self.created_items["rooms"] or not self.created_items["managers"]:
            print("❌ Não é possível criar bookings sem rooms e managers")
            return

        # 2. Criar booking
        room_id = self.created_items["rooms"][0]["id"]
        manager_id = self.created_items["managers"][0]["id"]

        start_time = datetime.now() + timedelta(days=1, hours=1)  # Amanhã
        end_time = start_time + timedelta(hours=2)

        booking_data = {
            "room": room_id,
            "manager": manager_id,
            "start_date": start_time.isoformat(),
            "end_date": end_time.isoformat(),
            "coffee_option": True,
            "coffee_quantity": 10,
            "coffee_description": "Café e água para reunião",
        }
        response = requests.post(f"{BASE_URL}/bookings/", json=booking_data)
        if response.status_code == 201:
            created_booking = response.json()
            self.created_items["bookings"].append(created_booking)
            self.print_result(
                "POST", f"{BASE_URL}/bookings/", response.status_code, created_booking
            )
        else:
            self.print_result(
                "POST",
                f"{BASE_URL}/bookings/",
                response.status_code,
                error=response.text,
            )

    def test_custom_actions(self):
        self.print_header("TESTANDO AÇÕES CUSTOMIZADAS")

        # Rooms by location
        if self.created_items["locations"]:
            location_id = self.created_items["locations"][0]["id"]
            response = requests.get(
                f"{BASE_URL}/rooms/by_location/", params={"location_id": location_id}
            )
            self.print_result(
                "GET",
                f"{BASE_URL}/rooms/by_location/?location_id={location_id}",
                response.status_code,
                response.json() if response.status_code == 200 else None,
            )

        # Manager by email
        if self.created_items["managers"]:
            manager_email = self.created_items["managers"][0]["email"]
            response = requests.get(
                f"{BASE_URL}/managers/by_email/", params={"email": manager_email}
            )
            self.print_result(
                "GET",
                f"{BASE_URL}/managers/by_email/?email={manager_email}",
                response.status_code,
                response.json() if response.status_code == 200 else None,
            )

    def test_delete_operations(self):
        self.print_header("TESTANDO OPERAÇÕES DE DELETE")

        # Delete booking
        if self.created_items["bookings"]:
            booking_id = self.created_items["bookings"][0]["id"]
            response = requests.delete(f"{BASE_URL}/bookings/{booking_id}/")
            self.print_result(
                "DELETE", f"{BASE_URL}/bookings/{booking_id}/", response.status_code
            )

        # Delete room
        if self.created_items["rooms"] and len(self.created_items["rooms"]) > 1:
            room_id = self.created_items["rooms"][-1]["id"]
            response = requests.delete(f"{BASE_URL}/rooms/{room_id}/")
            self.print_result(
                "DELETE", f"{BASE_URL}/rooms/{room_id}/", response.status_code
            )

    def run_all_tests(self):
        print("🚀 Iniciando testes completos da API LabTrans")
        print(f"Base URL: {BASE_URL}")

        try:
            self.test_locations()
            self.test_managers()
            self.test_rooms()
            self.test_bookings()
            self.test_custom_actions()
            self.test_delete_operations()

            self.print_header("RESUMO FINAL")
            for entity, items in self.created_items.items():
                print(f"📊 {entity.upper()}: {len(items)} items criados")

        except Exception as e:
            print(f"💥 Erro durante os testes: {e}")


if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()

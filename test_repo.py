#!/usr/bin/env python3
import os
import sys
import django

# Adicionar o caminho do projeto
sys.path.append(".")
sys.path.append("./api")

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


def test_room_repository():
    try:
        print("Testing Room Repository...")
        from api.infrastructure.repositories.django_room_repository import (
            DjangoRoomRepository,
        )

        repo = DjangoRoomRepository()
        print("Repository instantiated successfully!")

        # Test get_all method
        rooms = repo.get_all()
        print(f"Found {len(rooms)} rooms")

        return True

    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_room_repository()

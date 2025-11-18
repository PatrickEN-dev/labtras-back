#!/usr/bin/env python3
import os
import sys
import django

sys.path.append(".")
sys.path.append("./api")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


def test_room_repository():
    try:
        from api.infrastructure.repositories.django_room_repository import (
            DjangoRoomRepository,
        )

        repo = DjangoRoomRepository()
        rooms = repo.get_all()

        return True

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_room_repository()

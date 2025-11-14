from django.shortcuts import render
from prisma import Prisma
from rest_framework.views import APIView
from rest_framework.response import Response


class UsuariosView(APIView):
    def get(self, request):
        usuarios = prisma.usuario.find_many()
        return Response([u.dict() for u in usuarios])

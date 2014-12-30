from django.shortcuts import render

from rest_framework import viewsets

from .models import MaestraAhorro, AhorroSocio, RetiroAhorro
from .serializers import maestraAhorroSerializer, AhorroSocioSerializer, RetiroAhorroSerializer

class MaestraAhorroViewSet(viewsets.ModelViewSet):
	queryset=MaestraAhorro.objects.all()
	serializer_class=maestraAhorroSerializer

class AhorroViewSet(viewsets.ModelViewSet):
	queryset=AhorroSocio.objects.all()
	serializer_class=AhorroSocioSerializer

class RetirosAhorroViewSet(viewsets.ModelViewSet):
	queryset=RetiroAhorro.objects.all()
	serializer_class=RetiroAhorroSerializer
from django.shortcuts import render
from rest_framework import viewsets

from .models import Cuentas,Auxiliares,DiarioGeneral
from .serializers import CuentasSerializer, AuxiliarSerualizer, DiarioSerializer


class CuentasViewSet(viewsets.ModelViewSet):
	queryset=Cuentas.objects.all()
	serializer_class=CuentasSerializer


class AuxiliarViewSet(viewsets.ModelViewSet):
	queryset=Auxiliares.objects.all()
	serializer_class=AuxiliarSerualizer

class DiarioViewSet(viewsets.ModelViewSet):
	queryset=DiarioGeneral.objects.all()
	serializer_class=DiarioSerializer
	
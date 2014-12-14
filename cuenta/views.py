from django.shortcuts import render
from rest_framework import viewsets, serializers

from cuenta.models import Cuentas,Auxiliares

class CuentasSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Cuentas
		fields=('codigo','descripcion','origen')


class CuentasViewSet(viewsets.ModelViewSet):
	queryset=Cuentas.objects.all()
	serializer_class=CuentasSerializer


class AuxiliarSerualizer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Auxiliares
		fields=('codigo','descripcion','cuenta')

class AuxiliarViewSet(viewsets.ModelViewSet):
	queryset=Auxiliares.objects.all()
	serializer_class=AuxiliarSerualizer
	
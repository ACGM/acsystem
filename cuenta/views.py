from django.shortcuts import render
from rest_framework import viewsets, serializers

from cuenta.models import Cuentas

class CuentasSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Cuentas
		fields=('codigo','descripcion','origen')


class CuentasViewSet(viewsets.ModelViewSet):
	queryset=Cuentas.objects.all()
	serializer_class=CuentasSerializer
	
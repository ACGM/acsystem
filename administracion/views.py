from django.shortcuts import render

from rest_framework import viewsets, serializers
# Create your views here.

from .models import Suplidor, TipoSuplidor ,Socio, Departamento

class SuplidorTipoSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=TipoSuplidor
		fields=('descripcion')

class SuplidorTipoViewSet(viewsets.ModelViewSet):
	queryset=TipoSuplidor.objects.all()
	serializer_class=SuplidorTipoSerializer

class SuplidorSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Suplidor
		fields=('cedulaRNC','nombre', 'tipoSuplidor')

class SuplidorViewSet(viewsets.ModelViewSet):
	queryset=Suplidor.objects.all()
	serializer_class=SuplidorSerializer

class SocioSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Socio
		fields=('codigo','nombres','apellidos','departamento')

class SocioViewSet(viewsets.ModelViewSet):
	queryset=Socio.objects.all()
	serializer_class=SocioSerializer

class DepartamentoSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=Departamento
		fields=('centroCosto', 'descripcion')

class DepartamentoViewSet(viewsets.ModelViewSet):
	queryset=Departamento.objects.all()
	serializer_class=DepartamentoSerializer


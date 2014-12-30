from rest_framework import serializers

from .models import Producto, Suplidor, TipoSuplidor, Socio, Departamento

# Listado de Productos
class ProductoSerializer(serializers.HyperlinkedModelSerializer):
	unidad = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Producto
		fields = ('id','codigo','descripcion','unidad','precio','costo')
		ordering = ('descripcion',)


class SuplidorTipoSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model=TipoSuplidor
		fields=('descripcion',)


class SuplidorSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model=Suplidor
		fields=('id','cedulaRNC','nombre', 'tipoSuplidor')


class SocioSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model=Socio
		fields=('codigo','nombres','apellidos','departamento')


class DepartamentoSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model=Departamento
		fields=('centroCosto', 'descripcion')

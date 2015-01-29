#SERIALIZER -- Inventario

from rest_framework import serializers

from .models import Existencia, InventarioH, InventarioD, Almacen
from administracion.models import Suplidor

# Listado de Entradas de Inventario
class EntradasInventarioSerializer(serializers.ModelSerializer):
	suplidor = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = InventarioH
		fields = ('id','posteo','fecha','ncf','factura','suplidor','totalGeneral')
		ordering = ('-id',)


# Entrada de Inventario por ID
class EntradaInventarioByIdSerializer(serializers.ModelSerializer):
	suplidor = serializers.StringRelatedField(read_only=True)
	almacen = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = InventarioH
		field = ('id','fecha','ncf','factura','orden','condicion','suplidor', 'suplidor_id','diasPlazo','nota')


# Listado de Almacenes
class AlmacenesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Almacen


# Existencia de Producto
class ExistenciaProductoSerializer(serializers.ModelSerializer):
	producto = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Existencia
		fields = ('producto', 'getCodigo', 'cantidad', 'almacen')

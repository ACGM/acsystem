#SERIALIZER -- Inventario

from rest_framework import serializers

from .models import Existencia, InventarioH, InventarioD, Almacen, AjusteInventarioH, TransferenciasAlmacenes
from administracion.models import Suplidor

# Listado de Entradas de Inventario
class EntradasInventarioSerializer(serializers.ModelSerializer):
	suplidor = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = InventarioH
		fields = ('id','posteo','fecha','ncf','factura','suplidor','totalGeneral','getTipo')
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


# Ajustes de Inventario
class AjustesInventarioSerializer(serializers.ModelSerializer):

	class Meta:
		model = AjusteInventarioH
		fields = ('id', 'fecha', 'estatus', 'usuario')


# Transferencias entre Almacenes
class TransferenciasAlmacenesSerializer(serializers.ModelSerializer):
	producto = serializers.StringRelatedField(read_only=True)
	desdeAlmacen = serializers.StringRelatedField(read_only=True)
	hastaAlmacen = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = TransferenciasAlmacenes
		fields = ('id', 'fechaTransf', 'desdeAlmacen', 'hastaAlmacen', 'producto', 'cantidad', 'userLog')


# Existencia de Producto
class ExistenciaProductoSerializer(serializers.ModelSerializer):
	producto = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Existencia
		fields = ('producto', 'getCodigo', 'cantidad', 'almacen')

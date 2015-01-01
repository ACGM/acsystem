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


# Listado de Almacenes
class AlmacenesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Almacen

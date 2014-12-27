from rest_framework import serializers

from .models import Existencia, InventarioH, InventarioD
from administracion.models import Suplidor

# Listado de Entradas de Inventario
class EntradasInventarioSerializer(serializers.ModelSerializer):
	# suplidor = serializers.RelatedField(read_only=True)

	class Meta:
		model = InventarioH
		fields = ('id','posteo','fecha','ncf','factura','suplidor','totalGeneral')
		ordering = ('-id',)

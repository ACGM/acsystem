from rest_framework import serializers

from .models import Factura, Detalle, OrdenDespachoSuperCoop
from administracion.models import Socio, Producto, CategoriaPrestamo

# Listado de Facturas
class ListadoFacturasSerializer(serializers.ModelSerializer):
	socio = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Factura
		fields = ('id','fecha','noFactura','estatus','ordenCompra','impresa','socio','posteo','totalGeneral')
		ordering = ('-id',)


# # Entrada de Inventario por ID
# class EntradaInventarioByIdSerializer(serializers.ModelSerializer):
# 	suplidor = serializers.StringRelatedField(read_only=True)
# 	almacen = serializers.StringRelatedField(read_only=True)

# 	class Meta:
# 		model = InventarioH
# 		field = ('id','fecha','ncf','factura','orden','condicion','suplidor', 'suplidor_id','diasPlazo','nota')




# # Listado de Almacenes
# class AlmacenesSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = Almacen

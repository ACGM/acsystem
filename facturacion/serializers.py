from rest_framework import serializers

from .models import Factura, Detalle
from administracion.models import Socio, Producto

# Listado de Facturas
class ListadoFacturasSerializer(serializers.ModelSerializer):
	socio = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Factura
		fields = ('id', 'fecha', 'noFactura', 'estatus', 'ordenCompra', 'impresa', 'socio', 'posteo', 'totalGeneral')
		ordering = ('-id',)


# Detalle de facturas
class DetalleFacturasSerializer(serializers.ModelSerializer):
	producto = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Detalle
		fields = ('getFecha', 'getFactura', 'getCategoria', 'producto', 'porcentajeDescuento', 'cantidad', 'precio', 'costo', 'importeValor', 'almacen')
		ordering = ('getCategoria',)

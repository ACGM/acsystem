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


# Orden de Compra SUPERCOOP
class ListadoCategoriaPrestamoSerializer(serializers.ModelSerializer):

	class Meta:
		model = CategoriaPrestamo
		fields = ('id','descripcion','montoDesde', 'montoHasta', 'tipo', 'interesAnualSocio', 'interesAnualEmpleado', 'interesAnualDirectivo')
		ordering = ('id',)


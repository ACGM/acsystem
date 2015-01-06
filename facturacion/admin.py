from django.contrib import admin

from .models import Factura, Detalle

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):

	list_display = ['id', 'noFactura', 'fecha', 'estatus', 'socio', 'ordenCompra', 'terminos', 'impresa']
	list_editable = ('estatus','socio','ordenCompra','terminos')


@admin.register(Detalle)
class DetalleAdmin(admin.ModelAdmin):

	list_display = ['id', 'factura', 'producto', 'porcentajeDescuento', 'cantidad', 'precio', 'almacen']

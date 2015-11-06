from django.contrib import admin

from cxp.models import OrdenCompra, CxpSuperCoop, OrdenGeneral, OrdenDetalleFact, cxpSuperDetalle, cxpSuperGeneral

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'suplidor', 'socio', 'orden', 'fecha', 'monto']


@admin.register(CxpSuperCoop)
class OrdenSuperAdmin(admin.ModelAdmin):
    list_display = ['id', 'suplidor', 'factura', 'concepto', 'fecha', 'monto', 'descuento']


@admin.register(OrdenDetalleFact)
class OrdenDetalleAdmin(admin.ModelAdmin):
    list_display = ['id', 'idRegistro', 'factura', 'fecha', 'monto']

@admin.register(OrdenGeneral)
class OrdenGeneralAdmin(admin.ModelAdmin):
    list_display = ['id', 'suplidor', 'concepto', 'fecha', 'monto', 'descuento']

@admin.register(cxpSuperGeneral)
class cxpSuperGeneralAdmin(admin.ModelAdmin):
	list_display = ['id', 'suplidor', 'concepto', 'fecha', 'monto', 'descuento']

@admin.register(cxpSuperDetalle)
class cxpSuperDetAdmin(admin.ModelAdmin):
	list_display = ['id','idRegistro', 'fecha', 'monto']

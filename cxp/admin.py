from django.contrib import admin

from cxp.models import OrdenGeneral, OrdenDetalleFact, cxpSuperDetalle, cxpSuperGeneral

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

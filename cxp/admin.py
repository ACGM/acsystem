from django.contrib import admin

from cxp.models import OrdenCompra, CxpSuperCoop

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'suplidor', 'socio', 'orden', 'fecha', 'monto']


@admin.register(CxpSuperCoop)
class OrdenSuperAdmin(admin.ModelAdmin):
    list_display = ['id', 'suplidor', 'factura', 'concepto', 'fecha', 'monto', 'descuento']

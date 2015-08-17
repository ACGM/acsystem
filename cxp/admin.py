from django.contrib import admin

from cxp.models import OrdenCompra

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'suplidor', 'socio', 'orden', 'fecha', 'monto', 'cuotas', 'montocuotas', 'estatus']


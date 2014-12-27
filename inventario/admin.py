from django.contrib import admin

from .models import Almacen, InventarioH, InventarioD, Movimiento, Existencia

@admin.register(InventarioH)
class InventarioHAdmin(admin.ModelAdmin):
	list_display = ['id','fecha','suplidor','orden','factura','diasPlazo','ncf','posteo','nota','descripcionSalida','totalGeneral']
	# readonly_fields = ('total',)

@admin.register(InventarioD)
class InventarioDAdmin(admin.ModelAdmin):
	list_display = ['id','inventario','producto','almacen','cantidadTeorico','cantidadFisico','costo','tipoAccion']


admin.site.register(Almacen)
admin.site.register(Movimiento)
admin.site.register(Existencia)


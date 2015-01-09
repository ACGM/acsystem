from django.contrib import admin

from .models import Almacen, InventarioH, InventarioD, Movimiento, Existencia

@admin.register(InventarioH)
class InventarioHAdmin(admin.ModelAdmin):
	list_display = ['id','fecha','suplidor','orden','factura','diasPlazo','ncf','posteo','nota','descripcionSalida','totalGeneral']
	# readonly_fields = ('total',)

@admin.register(InventarioD)
class InventarioDAdmin(admin.ModelAdmin):
	list_display = ['id','inventario','producto','almacen','cantidadTeorico','cantidadFisico','costo','tipoAccion']

@admin.register(Existencia)
class ExistenciaAdmin(admin.ModelAdmin):
	list_display = ['producto', 'cantidad', 'almacen', 'fecha']
	search_fields = ('producto', 'almacen')

@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
	list_display = ['id', 'descripcion']
	
admin.site.register(Movimiento)


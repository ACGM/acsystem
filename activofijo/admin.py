from django.contrib import admin

from .models import CategoriaActivo, Depresiacion, Activos


@admin.register(CategoriaActivo)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']


@admin.register(Depresiacion)
class DepresiacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'dMensual', 'dAcumulada', 'dAgno', 'vLibro']


@admin.register(Activos)
class ActivosAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion', 'categoria', 'fechaAdd', 'fechaDep', 'agnosVu', 'costo', 'porcentaje',
                    'suplidor', 'factura']
from django.contrib import admin

from .models import MaestraAhorro, AhorroSocio, InteresesAhorro


@admin.register(MaestraAhorro)
class MaestraAhorroAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'ahorro', 'monto', 'estatus']
    search_fields = ('ahorro__socio__nombreCompleto',)


@admin.register(AhorroSocio)
class AhorroAdmin(admin.ModelAdmin):
    list_display = ['id', 'socio', 'balance', 'disponible']
    search_fields = ('socio__nombreCompleto',)


@admin.register(InteresesAhorro)
class InteresAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion', 'porcentaje']

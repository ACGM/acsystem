from django.contrib import admin

from .models import Cuentas, Auxiliares, DiarioGeneral


@admin.register(Cuentas)
class CuentasAdmin(admin.ModelAdmin):
    list_display = ("codigo", "descripcion", "origen", "control", 'cuentaControl')
    search_fields = ("codigo", "descripcion", "origen",)


@admin.register(Auxiliares)
class AuxiliarAdmin(admin.ModelAdmin):
    list_display = ("codigo", "descripcion", "cuenta",)
    search_fields = ("codigo", "descripcion", "cuenta",)


@admin.register(DiarioGeneral)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "cuenta", "referencia", "auxiliar", "tipoDoc", "estatus", "debito", "credito")




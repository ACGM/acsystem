from django.contrib import admin

from .models import Cuentas, Auxiliar, DiarioGeneral, CuentasControl


@admin.register(Cuentas)
class CuentasAdmin(admin.ModelAdmin):
    list_display = ("codigo", "descripcion", "origen", "tipo", "control", 'cuentaControl')
    search_fields = ("codigo", "descripcion", "origen",'tipo')


@admin.register(Auxiliar)
class AuxiliarAdmin(admin.ModelAdmin):
    list_display = ("codigo", "socio", "suplidor", "cuenta",)
    search_fields = ("codigo", "socio", "suplidor", "cuenta",)


@admin.register(DiarioGeneral)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "cuenta", "referencia", "auxiliar", "estatus", "debito", "credito")


@admin.register(CuentasControl)
class CuentasControlAdmin(admin.ModelAdmin):
    list_display = ("id", "codigoControl", "descripcion",)
    search_fields = ("codigoControl", "descripcion",)

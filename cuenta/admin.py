from django.contrib import admin

from .models import Cuentas, DiarioGeneral, CuentasControl, BalanceCuenta


@admin.register(Cuentas)
class CuentasAdmin(admin.ModelAdmin):
    list_display = ("codigo", "descripcion", "origen", "tipo", "control", 'cuentaControl','tipoSocio')
    search_fields = ("codigo", "descripcion", "origen",'tipo')
    list_editable = ('tipoSocio',)


@admin.register(DiarioGeneral)
class DiarioAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "cuenta", "referencia", "estatus", "debito", "credito")


@admin.register(CuentasControl)
class CuentasControlAdmin(admin.ModelAdmin):
    list_display = ("id", "codigoControl", "descripcion",)
    search_fields = ("codigoControl", "descripcion",)

@admin.register(BalanceCuenta)
class BalanceAdmin(admin.ModelAdmin):
	list_display = ("id", "agno", "mes", "cuenta", "Balance")
	search_fields = ("agno", "mes")

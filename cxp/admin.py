from django.contrib import admin

from .models import CuentasGenericasOrdenes

@admin.register(CuentasGenericasOrdenes)
class CuentaOrdenAdmin(admin.ModelAdmin):
    list_display = ("cuenta", "aux", "origen")
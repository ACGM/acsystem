from django.contrib import admin

from .models import ConcCheques, SolicitudCheque, NotaDCConciliacion, ConBanco


@admin.register(ConcCheques)
class ConcChequeAdmin(admin.ModelAdmin):
    list_display = ['id', 'solicitud', 'chequeNo', 'fecha', 'estatus']


@admin.register(SolicitudCheque)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'socio', 'concepto', 'monto', 'estatus']


@admin.register(NotaDCConciliacion)
class NotaConciliacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'concepto', 'fecha', 'tipo', 'monto', 'estatus']


@admin.register(ConBanco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'descripcion', 'tipo', 'monto', 'estatus']

from django.contrib import admin

from .models import ConcCheques, SolicitudCheque, NotaDCConciliacion, ConBanco, NumCheque, ConDeposito, ConPeriodo


@admin.register(ConcCheques)
class ConcChequeAdmin(admin.ModelAdmin):
    list_display = ['id','fecha', 'solicitud', 'chequeNo',  'estatus']


@admin.register(SolicitudCheque)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'socio', 'suplidor','concepto', 'monto', 'estatus']


@admin.register(NotaDCConciliacion)
class NotaConciliacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'concepto', 'fecha', 'tipo', 'monto', 'estatus']


@admin.register(ConBanco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'descripcion', 'monto', 'estatus']


@admin.register(ConDeposito)
class DepositosAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'descripcion', 'monto', 'estatus']


# @admin.register(conChequeTrans)
# class conChequeTransAdmin(admin.ModelAdmin):
#     list_display = ['id', 'fecha', 'descripcion', 'monto', 'estatus']

@admin.register(NumCheque)
class NumChequeAdmin(admin.ModelAdmin):
	list_display = ['id', 'chequeNo', 'banco']

@admin.register(ConPeriodo)
class ConPeriodoAdmin(admin.ModelAdmin):
	list_display = ['id', 'fechaInicio', 'fechaFin', 'cuenta', 'monto']
from django.contrib import admin

from .models import ReciboIngresoNomina


@admin.register(ReciboIngresoNomina)
class ReciboIngresoNominaAdmin(admin.ModelAdmin):

	list_display = ['id', 'fecha', 'concepto', 'estatus']
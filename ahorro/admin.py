from django.contrib import admin

from .models import MaestraAhorro, AhorroSocio


@admin.register(MaestraAhorro)
class MaestraAhorroAdmin(admin.ModelAdmin):
	list_display = ['id','fecha','ahorro','retiro','monto','interes','balance','estatus']

	
@admin.register(AhorroSocio)
class AhorroAdmin(admin.ModelAdmin):
    list_display = ['id','socio','balance','disponible']


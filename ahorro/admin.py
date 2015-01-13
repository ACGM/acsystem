from django.contrib import admin

from .models import MaestraAhorro
from cuenta.models import DiarioGeneral

@admin.register(MaestraAhorro)
class MaestraAhorroAdmin(admin.ModelAdmin):
	list_display = ["fecha","ahorro","retiro","monto","interes","balance","estatus"]

	
	

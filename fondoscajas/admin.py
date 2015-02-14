from django.contrib import admin

from .models import Fondo, ConceptoDesembolso, DesembolsoH, DesembolsoD


@admin.register(Fondo)
class FondoAdmin(admin.ModelAdmin):
	list_display = ['id', 'descripcion', 'estatus']
	list_editable = ('descripcion', 'estatus')

@admin.register(ConceptoDesembolso)
class ConceptoDesembolsoAdmin(admin.ModelAdmin):
	list_display = ['id', 'descripcion', 'cuentaDebito', 'cuentaCredito', 'userLog']
	list_editable = ('descripcion', 'cuentaDebito', 'cuentaCredito')

	def save_model(self, request, obj, form, change):
		obj.userLog = request.user
		obj.save()


@admin.register(DesembolsoD)
class DesembolsoDAdmin(admin.ModelAdmin):
	list_display = ['id','desembolso', 'concepto', 'monto']
	list_editable = ('desembolso', 'concepto', 'monto')

class DesembolsoDInline(admin.StackedInline):
	model = DesembolsoD
	extra = 2

@admin.register(DesembolsoH)
class DesembolsoHAdmin(admin.ModelAdmin):
	list_display = ['id','beneficiario', 'fecha', 'localidad', 'estatus', 'totalGeneral', 'userLog', 'impreso']
	list_editable = ('beneficiario', 'estatus',)

	def save_model(self, request, obj, form, change):
		obj.userLog = request.user
		obj.save()

	inlines = [DesembolsoDInline,]
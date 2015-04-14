from django.contrib import admin

from .models import DepartamentoCoop, CargoCoop, EmpleadoCoop, TipoNomina, NominaCoopH, \
					NominaCoopD, CuotasPrestamosEmpresa, CuotasAhorrosEmpresa, NominaPrestamosAhorros

@admin.register(DepartamentoCoop)
class DepartamentoCoopAdmin(admin.ModelAdmin):
	list_display = ['id', 'descripcion',]
	list_editable = ('descripcion',)

@admin.register(CargoCoop)
class CargoCooAdminp(admin.ModelAdmin):
	list_display = ['id', 'descripcion']
	list_editable = ('descripcion',)

@admin.register(EmpleadoCoop)
class EmpleadoCoopAdmin(admin.ModelAdmin):
	list_display = ['id','codigo', 'nombres', 'apellidos', 'cedula', 'departamento', 'sueldoActual']
	list_editable = ('codigo', 'nombres', 'apellidos', 'cedula', 'departamento', 'sueldoActual')
	search_fields = ('nombres', 'apellidos')

@admin.register(TipoNomina)
class TipoNominaAdmin(admin.ModelAdmin):
	list_display = ['id','descripcion']
	list_editable = ('descripcion',)

@admin.register(NominaCoopH)
class NominaCoopHAdmin(admin.ModelAdmin):
	list_display = ['id','fechaNomina', 'fechaPago', 'valorNomina', 'sueldoMensual', 'tipoNomina', 'tipoPago', 'estatus', 'quincena', 'cntEmpleados']
	list_editable = ('tipoNomina', 'tipoPago')

@admin.register(NominaCoopD)
class NominaCoopDAdmin(admin.ModelAdmin):
	list_display = ['getCodigo','nomina', 'empleado', 'salario']

	def getCodigo(self, obj):
		return '%s' % (obj.empleado.codigo)

@admin.register(CuotasPrestamosEmpresa)
class CuotasPrestamosEmpresaAdmin(admin.ModelAdmin):
	list_display = ['id', 'valorCapital', 'valorInteres', 'fecha', 'nomina', 'estatus', 'infoTipoPrestamo']
	# list_display = ['socio', 'noPrestamo', 'cuota', 'valorCapital', 'valorInteres', 'fecha', 'nomina', 'estatus']

@admin.register(CuotasAhorrosEmpresa)
class CuotasAhorrosEmpresaAdmin(admin.ModelAdmin):
	list_display = ['socio', 'valorAhorro', 'nomina', 'estatus']
	list_filter = ('nomina',)

@admin.register(NominaPrestamosAhorros)
class NominasPrestamosAhorrosAdmin(admin.ModelAdmin):
	list_display = ['nomina', 'tipo', 'estatus', 'infoTipo']

	
from django.contrib import admin

from .models import DepartamentoCoop, CargoCoop, EmpleadoCoop, TipoNomina, NominaCoopH, \
					NominaCoopD, CuotasPrestamosEmpresa, CuotasAhorrosEmpresa

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
	list_display = ['codigo', 'nombres', 'apellidos', 'cedula', 'departamento', 'sueldoActual']
	list_editable = ('nombres', 'apellidos', 'cedula', 'departamento', 'sueldoActual')
	search_fields = ('nombres', 'apellidos')

@admin.register(TipoNomina)
class TipoNominaAdmin(admin.ModelAdmin):
	list_display = ['id','descripcion']
	list_editable = ('descripcion',)

@admin.register(NominaCoopH)
class NominaCoopHAdmin(admin.ModelAdmin):
	list_display = ['fechaNomina', 'fechaPago', 'valorNomina', 'tipoNomina', 'tipoPago', 'estatus', 'quincena', 'cntEmpleados']
	list_editable = ('tipoNomina', 'tipoPago')

@admin.register(NominaCoopD)
class NominaCoopDAdmin(admin.ModelAdmin):
	list_display = ['nomina', 'empleado', 'salario']

@admin.register(CuotasPrestamosEmpresa)
class CuotasPrestamosEmpresaAdmin(admin.ModelAdmin):
	list_display = ['id','valorCapital', 'valorInteres','fecha','nomina','estatus']
	# list_display = ['socio', 'noPrestamo', 'cuota', 'valorCapital', 'valorInteres', 'fecha', 'nomina', 'estatus']

@admin.register(CuotasAhorrosEmpresa)
class CuotasAhorrosEmpresaAdmin(admin.ModelAdmin):
	list_display = ['socio', 'valorAhorro', 'fecha', 'estatus']
	
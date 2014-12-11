from django.contrib import admin

from administracion.models import Localidad, Distrito, Departamento, Representante, Unidad, Producto, TipoSuplidor, Suplidor, Socio, CoBeneficiario, CategoriaPrestamo, CuotaPrestamo

@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
	list_display = ['id','descripcion',]
	list_editable = ('descripcion',)

@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
	list_display = ['id','descripcion', 'localidad',]
	list_editable = ('descripcion','localidad',)

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
	list_display = ('id','centroCosto','descripcion')
	list_editable = ('centroCosto','descripcion',)
	search_fields = ('centroCosto','descripcion',)

@admin.register(Representante)
class RepresentanteAdmin(admin.ModelAdmin):
	list_display = ['id','nombre']
	list_editable = ('nombre',)

@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
	list_display = ['id','descripcion','nota']
	list_editable = ('descripcion', 'nota')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
	list_display = ['id','codigo','descripcion','unidad','precio','costo']
	list_editable = ('descripcion','unidad','precio','costo')
	search_fields = ('codigo','descripcion')

@admin.register(TipoSuplidor)
class TipoSuplidorAdmin(admin.ModelAdmin):
	list_display = ['id','descripcion']
	list_editable = ('descripcion',)

@admin.register(Suplidor)
class SuplidorAdmin(admin.ModelAdmin):
	list_display = ['id','tipoIdentificacion','cedulaRNC','nombre','telefono','intereses','tipoSuplidor','auxiliar','clase']
	list_editable = ('nombre','telefono','intereses','tipoSuplidor','auxiliar','clase')
	search_fields = ('cedulaRNC','nombre')

@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
	list_display = ['codigo','nombres','apellidos','fechaIngresoCoop','fechaIngresoEmpresa','departamento','estatus','salario','cuentaBancaria']
	list_editable = ('nombres','apellidos','departamento','salario','cuentaBancaria')
	search_fields = ('nombres','apellidos','cuentaBancaria')
	list_filter = ('departamento',)

@admin.register(CoBeneficiario)
class CoBeneficiarioAdmin(admin.ModelAdmin):
	list_display = ['socio','nombre','telefono','parentesco']
	list_editable = ('nombre','telefono','parentesco')
	search_fields = ('nombre',)

@admin.register(CategoriaPrestamo)
class CategoriaPrestamoAdmin(admin.ModelAdmin):
	list_display = ['id','descripcion','montoDesde','montoHasta','tipo','interesAnualSocio','interesAnualEmpleado','interesAnualDirectivo']
	list_editable = ('descripcion','montoDesde','montoHasta','tipo','interesAnualSocio','interesAnualEmpleado','interesAnualDirectivo')
	search_fields = ('descripcion',)
	list_filter = ('tipo',)

class CuotaPrestamoAdmin(admin.ModelAdmin):
	# list_display = ['id','montoDesde','montoHasta','cantidadQuincenas','cantidadMeses']
	# list_editable = ('montoDesde', 'montoHasta', 'cantidadQuincenas','cantidadMeses')

	def save_model(self, request, obj, form, change):
		obj.user = request.user
        # obj.save()

admin.site.register(CuotaPrestamo,CuotaPrestamoAdmin)
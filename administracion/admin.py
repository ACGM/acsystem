from django.contrib import admin

from administracion.models import Localidad, Distrito, Departamento, Representante, \
								 Unidad, Producto, TipoSuplidor, Suplidor, Socio, \
								 CoBeneficiario, CategoriaPrestamo, CuotaPrestamo, \
								 CuotaOrdenes, Autorizador, Perfil, Opcion, Banco, \
								 TipoDocumento, Periodo, Empresa, Cobrador, CuotaAhorroSocio, \
								 DocumentoCuentas


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

@admin.register(CategoriaPrestamo)
class CategoriaPrestamoAdmin(admin.ModelAdmin):
	list_display = ['id','descripcion','montoDesde','montoHasta','tipo','interesAnualSocio','interesAnualEmpleado','interesAnualDirectivo']
	list_editable = ('descripcion','montoDesde','montoHasta','tipo','interesAnualSocio','interesAnualEmpleado','interesAnualDirectivo')
	search_fields = ('descripcion',)
	list_filter = ('tipo',)

@admin.register(CuotaPrestamo)
class CuotaPrestamoAdmin(admin.ModelAdmin):
	list_display = ['id','montoDesde','montoHasta','cantidadQuincenas','cantidadMeses']
	list_editable = ('montoDesde', 'montoHasta', 'cantidadQuincenas','cantidadMeses')

@admin.register(CuotaOrdenes)
class CuotaOrdenesAdmin(admin.ModelAdmin):
	list_display = ['id','montoDesde','montoHasta','cantidadQuincenas','cantidadMeses']
	list_editable = ('montoDesde', 'montoHasta', 'cantidadQuincenas','cantidadMeses')

@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
	list_display = ['descripcion','tipo']
	list_editable = ('descripcion',)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
	list_display = ['id','perfilCod','opcion']
	list_editable = ('opcion',)

@admin.register(Autorizador)
class AutorizadorAdmin(admin.ModelAdmin):
	list_display = ['usuario','perfil']

@admin.register(CoBeneficiario)
class CoBeneficiarioAdmin(admin.ModelAdmin):
	list_display = ['socio','nombre','telefono','parentesco']
	list_editable = ('nombre','telefono','parentesco')
	search_fields = ('nombre',)
	raw_id_fields = ('socio',)

class CoBeneficiarioInline(admin.StackedInline):
	model = CoBeneficiario
	extra = 1

@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
	list_display = ['codigo','nombres','apellidos','fechaIngresoCoop','fechaIngresoEmpresa','departamento','estatus','salario','cuentaBancaria']
	list_editable = ('nombres','apellidos','departamento','salario','cuentaBancaria')
	search_fields = ('nombres','apellidos','cuentaBancaria')
	list_filter = ('departamento',)

	inlines = [CoBeneficiarioInline,]

@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
	list_display = ['id','codigo','nombre']
	list_editable = ('codigo','nombre')

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
	list_display = ['codigo','descripcion']
	list_editable = ('descripcion',)
	search_fields = ('descripcion',)

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
	list_display = ['id','mes','agno','estatus']

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
	list_display = ['id','nombre']
	list_editable = ('nombre',)

@admin.register(Cobrador)
class CobradorAdmin(admin.ModelAdmin):
	list_display = ['usuario','userLog']

@admin.register(CuotaAhorroSocio)
class CuotaAhorroSocioAdmin(admin.ModelAdmin):
	list_display = ['socio','cuotaAhorroQ1','cuotaAhorroQ2']
	list_editable = ('cuotaAhorroQ1','cuotaAhorroQ2')
	search_fields = ('socio',)

@admin.register(DocumentoCuentas)
class DocumentoCuentas(admin.ModelAdmin):
	list_display = ['documento','cuenta','accion']
	list_editable = ('cuenta','accion')
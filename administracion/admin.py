from django.contrib import admin

from administracion.models import Localidad, Departamento, Representante, \
								 Unidad, Producto, TipoSuplidor, Suplidor, Socio, \
								 CoBeneficiario, CategoriaPrestamo, CuotaPrestamo, \
								 CuotaOrdenes, Autorizador, Perfil, Opcion, Banco, \
								 TipoDocumento, Periodo, Empresa, Cobrador, DocumentoCuentas, \
								 CategoriaProducto, ArchivoBancoHeader, ArchivoBancoDetailN, \
								 UserExtra, ArchivoBanco



class CoBeneficiarioInline(admin.StackedInline):
	model = CoBeneficiario
	extra = 1

class OpcionInline(admin.StackedInline):
	model = Opcion
	extra = 2


@admin.register(ArchivoBanco)
class ArchivoBancoAdmin(admin.ModelAdmin):
	list_display = ['id', 'bancoAsign', 'tipoServicio', 'envio', 'secuencia', 'userLog']

@admin.register(ArchivoBancoHeader)
class ArchivoBancoHeaderAdmin(admin.ModelAdmin):
	list_display = ['id', 'tipoRegistro', 'idCompania', 'nombreCompania', 'secuencia']

@admin.register(ArchivoBancoDetailN)
class ArchivoBancoDetailNAdmin(admin.ModelAdmin):
	list_display = ['id','tipoRegistro','idCompania','secuencia','secuenciaTrans', 'lineaFormateadaN']
	list_editable = ('lineaFormateadaN',)
	
@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
	list_display = ['id','descripcion',]
	list_editable = ('descripcion',)

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

	def save_model(self, request, obj, form, change):
		obj.userLog = request.user
		obj.save()

@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
	list_display = ['id','descripcion',]
	list_editable = ('descripcion',)
	search_fields = ('descripcion',)

@admin.register(TipoSuplidor)
class TipoSuplidorAdmin(admin.ModelAdmin):
	list_display = ['id','descripcion']
	list_editable = ('descripcion',)

@admin.register(Suplidor)
class SuplidorAdmin(admin.ModelAdmin):
	list_display = ['id','tipoIdentificacion','cedulaRNC','nombre','telefono','intereses','tipoSuplidor','auxiliar','clase']
	list_editable = ('nombre','telefono','intereses','tipoSuplidor','auxiliar','clase')
	search_fields = ('cedulaRNC','nombre')

	def save_model(self, request, obj, form, change):
		obj.userLog = request.user
		obj.save()

@admin.register(CategoriaPrestamo)
class CategoriaPrestamoAdmin(admin.ModelAdmin):
	list_display = ['id','descripcion','montoDesde','montoHasta','tipo','interesAnualSocio',] #'interesAnualEmpleado','interesAnualDirectivo'
	list_editable = ('descripcion','montoDesde','montoHasta','tipo','interesAnualSocio',) #'interesAnualEmpleado','interesAnualDirectivo'
	search_fields = ('descripcion',)
	list_filter = ('tipo',)

	def save_model(self, request, obj, form, change):
		obj.userLog = request.user
		obj.save()

@admin.register(CuotaPrestamo)
class CuotaPrestamoAdmin(admin.ModelAdmin):
	list_display = ['id','montoDesde','montoHasta','cantidadQuincenas']
	list_editable = ('montoDesde', 'montoHasta', 'cantidadQuincenas')

	def save_model(self, request, obj, form, change):
		obj.userLog = request.user
		obj.save()

@admin.register(CuotaOrdenes)
class CuotaOrdenesAdmin(admin.ModelAdmin):
	list_display = ['id','montoDesde','montoHasta','cantidadQuincenas',]
	list_editable = ('montoDesde', 'montoHasta', 'cantidadQuincenas',)

	def save_model(self, request, obj, form, change):
		obj.userLog = request.user
		obj.save()

# @admin.register(Opcion)
# class OpcionAdmin(admin.ModelAdmin):
# 	list_display = ['id','descripcion','tipo']
# 	list_editable = ('descripcion',)

@admin.register(UserExtra)
class UserExtraAdmin(admin.ModelAdmin):
	list_display = ['usuario', 'localidad', 'perfil']
	list_editable = ('localidad','perfil')

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
	list_display = ['id','perfilCod',]
	list_editable = ('perfilCod',)

	inlines = [OpcionInline,]

@admin.register(Autorizador)
class AutorizadorAdmin(admin.ModelAdmin):
	list_display = ['usuario','perfil']

# @admin.register(CoBeneficiario)
# class CoBeneficiarioAdmin(admin.ModelAdmin):
# 	list_display = ['socio','nombre','telefono','parentesco']
# 	list_editable = ('nombre','telefono','parentesco')
# 	search_fields = ('nombre',)
# 	raw_id_fields = ('socio',)

@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
	list_display = ['id','codigo','nombres','apellidos', 'salario','fechaIngresoCoop','fechaIngresoEmpresa','departamento','estatus','cuentaBancaria']
	list_editable = ('codigo','nombres','apellidos','departamento','salario','cuentaBancaria')
	search_fields = ('codigo','nombres','apellidos','cuentaBancaria')
	list_filter = ('departamento',)
	raw_id_fields = ('departamento',)

	def save_model(self, request, obj, form, change):
		obj.userLog = request.user
		obj.save()

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
	list_display = ['id','nombre', 'rnc', 'bancoAsign']
	list_editable = ('nombre','rnc','bancoAsign')

@admin.register(Cobrador)
class CobradorAdmin(admin.ModelAdmin):
	list_display = ['usuario','userLog']

@admin.register(DocumentoCuentas)
class DocumentoCuentas(admin.ModelAdmin):
	list_display = ['documento','cuenta','accion']
	list_editable = ('cuenta','accion')
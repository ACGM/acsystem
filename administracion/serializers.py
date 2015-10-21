# SERIALIZERS -- Administracion

from rest_framework import serializers

from .models import Producto, Suplidor, TipoSuplidor, Socio, Departamento, CoBeneficiario, CategoriaPrestamo, \
					CuotaPrestamo, CuotaOrdenes, Autorizador, Empresa, Representante, CategoriaProducto, DocumentoCuentas


# Listado de Productos
class ProductoSerializer(serializers.HyperlinkedModelSerializer):
	unidad = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Producto
		fields = ('id','codigo','descripcion','unidad','precio','costo')
		ordering = ('descripcion',)


# Listado de Tipos de Suplidores
class SuplidorTipoSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model=TipoSuplidor
		fields=('descripcion',)


# Listado de Suplidores
class SuplidorSerializer(serializers.ModelSerializer):

	class Meta:
		model=Suplidor
		fields=('id','cedulaRNC','nombre', 'tipoSuplidor')


class SocioSerializer(serializers.HyperlinkedModelSerializer):
	departamento = serializers.StringRelatedField(read_only=False)
	localidad = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Socio
		fields = ('id', 'codigo', 'nombres', 'apellidos', 'nombreCompleto', 'estatus', 'departamento', 'cedula', \
					'salario', 'cuotaAhorroQ1', 'cuotaAhorroQ2', 'fechaIngresoEmpresa', 'fechaIngresoCoop', \
					'localidad', 'telefono')


class DepartamentoSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model=Departamento
		fields=('centroCosto', 'descripcion')


class CoBeneficiarioSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model=CoBeneficiario
		fields=('socio','nombre')


# Categorias de Prestamos
class ListadoCategoriaPrestamoSerializer(serializers.ModelSerializer):

	class Meta:
		model = CategoriaPrestamo
		fields = ('id','descripcion','montoDesde', 'montoHasta', 'tipo', 'interesAnualSocio')
		ordering = ('id',)


# Cantidad de Cuotas de Prestamos (parametro Monto)
class CantidadCuotasPrestamosSerializer(serializers.ModelSerializer):

	class Meta:
		model = CuotaPrestamo
		fields = ('montoDesde', 'montoHasta', 'cantidadQuincenas')
		ordering = ('-montoDesde',)


# Cantidad de Cuotas de Ordenes (parametro Monto)
class CantidadCuotasODSerializer(serializers.ModelSerializer):

	class Meta:
		model = CuotaOrdenes
		fields = ('montoDesde', 'montoHasta', 'cantidadQuincenas')
		ordering = ('-montoDesde',)


# Autorizadores de: Prestamos,
class AutorizadoresSerializer(serializers.ModelSerializer):

	class Meta:
		model = Autorizador
		fields = ('usuario', 'userName',)


# Empresas
class EmpresasSerializer(serializers.ModelSerializer):

	class Meta:
		model = Empresa
		fields = ('id', 'nombre', 'rnc', 'bancoAsign')

		
# Representantes
class RepresentantesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Representante
		fields = ('id', 'nombre',)

# Categorias de Productos
class CategoriasProductosSerializer(serializers.ModelSerializer):

	class Meta:
		model = CategoriaProducto
		fields = ('id', 'descripcion',)
		
# Categorias de Productos
class DocumentoCuentasSerializer(serializers.ModelSerializer):
	documento = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = DocumentoCuentas
		fields = ('getCodigo', 'documento', 'getCuentaCodigo', 'getCuentaDescrp', 'accion', 'getTipoSocio')
		
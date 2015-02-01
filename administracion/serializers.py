# SERIALIZERS -- Administracion

from rest_framework import serializers

from .models import Producto, Suplidor, TipoSuplidor, Socio, Departamento, CoBeneficiario, CategoriaPrestamo, \
					CuotaPrestamo, CuotaOrdenes, Autorizador, Empresa


# Listado de Productos
class ProductoSerializer(serializers.HyperlinkedModelSerializer):
	unidad = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Producto
		fields = ('id','codigo','descripcion','unidad','precio','costo')
		ordering = ('descripcion',)


class SuplidorTipoSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model=TipoSuplidor
		fields=('descripcion',)


class SuplidorSerializer(serializers.ModelSerializer):

	class Meta:
		model=Suplidor
		fields=('id','cedulaRNC','nombre', 'tipoSuplidor')


class SocioSerializer(serializers.HyperlinkedModelSerializer):
	departamento = serializers.StringRelatedField(read_only=False)

	class Meta:
		model = Socio
		fields = ('codigo', 'nombres', 'apellidos', 'nombreCompleto', 'estatus', 'departamento', 'cedula', 'salario', )


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
		fields = ('id','descripcion','montoDesde', 'montoHasta', 'tipo', 'interesAnualSocio', 'interesAnualEmpleado', 'interesAnualDirectivo')
		ordering = ('id',)


# Cantidad de Cuotas de Prestamos (parametro Monto)
class CantidadCuotasPrestamosSerializer(serializers.ModelSerializer):

	class Meta:
		model = CuotaPrestamo
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
		fields = ('nombre', 'rnc', 'bancoAsign')
		
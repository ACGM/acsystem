from django.db import models
from administracion.models import Suplidor, Localidad
from cuenta.models import DiarioGeneral
#Definicion de tipos de activos
class CategoriaActivo(models.Model):
	descripcion=models.CharField(max_length=100, default=None, unique=True, null=False, verbose_name='Categoria de Activo')

	def __unicode__(self):
		return descripcion

class Depresiacion(models.Model):
	dMensual=models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Depresiacion Mensual')
	dAcumulada=models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Depresiacion Acumulada')
	dAgno=models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Depresiacion en el Agno')
	vLibro=models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Valor en Libro')
	cuentas=models.ManyToManyField(DiarioGeneral, verbose_name='Cuentas', related_name='depre_rel' )

class Activos(models.Model):
	descripcion=models.CharField(max_length=100, default=None, null=False, verbose_name='Descripcion')
	categoria=models.ForeignKey(CategoriaActivo)
	#Fecha Adquisicion
	fechaAdd=models.DateTimeField(null=False, verbose_name='Fecha Adquisicion')
	#Fecha Depresiacion
	fechaDep=models.DateTimeField(null=False, verbose_name='Fecha Depresiacion')
	#Agnos de Vida Util
	agnosVu=models.PositiveIntegerField(null=False, verbose_name='Agnos vida Util')
	costo=models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Costo de adquisicion')
	porcentaje=models.DecimalField(max_digits=3, decimal_places=2, verbose_name="%. Dep Anual")
	suplidor=models.ForeignKey(Suplidor, null=False, verbose_name='Suplidor')
	factura=models.PositiveIntegerField(null=False, verbose_name='Factura')
	localidad=models.ForeignKey(Localidad, verbose_name='Localidad')

	#relaciones Many To Many a Depresiaciones y Diario General
	depresiacion=models.ManyToManyField(Depresiacion, verbose_name='Depresiaciones', related_name='ActivoDep_rel')
	cuentas=models.ManyToManyField(DiarioGeneral, verbose_name='Cuentas', related_name='ActivoCuentas_rel')



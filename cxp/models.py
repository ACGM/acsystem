from django.db import models
from administracion.models import Suplidor, Socio
from cuenta.models import Cuentas, Auxiliares

#Detalle de articulos y precio del mismo de la Orden
class DetalleOrden(models.Model):
	articulo=models.CharField(max_length=200, default=False, blank=False, null=False, verbose_name="Articulo")
	monto=models.DecimalField(max_digits=18, decimal_places=2, blank=False, null=False, verbose_name="Precio")

	def __unicode__(self):
		return self.articulo

	class Meta:
		ordering = ['articulo']

#Detalle de las cuentas afectadas en la orden
class DetalleCuentasOrden(models.Model):
	cuenta=models.ForeignKey(Cuentas,null=True, blank=True, verbose_name="Cuenta")
	auxiliar=models.ForeignKey(Auxiliares, null=True, blank=True, verbose_name="Cuenta")
	debito=models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False, verbose_name="Debito")
	credito=models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False, verbose_name="Credito")

	def __unicode__(self):
		return self.pk

	class Meta:
		ordering=['cuenta','auxiliar']

#Registro de ordenes de compra a Socio
class OrdenCompra(models.Model):
	suplidor=models.ForeignKey(Suplidor, null=False, blank=False, default=False, verbose_name="Suplidor")
	socio=models.ForeignKey(Socio, null=False, blank=False, default=False, verbose_name="Socio")
	orden=models.PositiveIntegerField(null=False, blank=False, verbose_name="# Orden")
	fecha=models.DateField(verbose_name="Fecha")
	monto=models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, verbose_name="Monto")
	cuotas=models.PositiveIntegerField(null=False, blank=False, verbose_name="Cuotas")
	montocuotas=models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False)
	detalleOrden=models.ForeignKey(DetalleOrden, verbose_name="Detalle de Orden")
	detalleCuentas=models.ForeignKey(DetalleCuentasOrden, verbose_name="Detalle Cuentas")

	def __unicode__(self):
		return self.orden

	class Meta: 
		ordering = ['suplidor','fecha']



#Cuentas Afectadas en el registro de Cxp SuperCoop
class CxpSuperCoopDetalleCuentas(models.Model):
	cuenta=models.ForeignKey(Cuentas,null=True, blank=True, verbose_name="Cuenta")
	auxiliar=models.ForeignKey(Auxiliares, null=True, blank=True, verbose_name="Cuenta")
	debito=models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False, verbose_name="Debito")
	credito=models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False, verbose_name="Credito")

	def __unicode__(self):
		return self.pk

	class Meta:
		ordering=['cuenta','auxiliar']

#Cuenta por pagar a suplidor de SuperCoop
class CxpSuperCoop(models.Model):
	suplidor=models.ForeignKey(Suplidor, null=False, blank=False, default=False, verbose_name="Suplidor")
	factura=models.CharField(max_length=10, default=False, null=False, blank=False, verbose_name="# Factura")
	fecha=models.DateField(verbose_name="Fecha")	
	concepto=models.CharField(max_length=255, null=False, blank=False, default=False, verbose_name="Concepto")
	monto=models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False, verbose_name="Monto")
	descuento=models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False, verbose_name="Desc")
	detalleCuentas=models.ForeignKey(CxpSuperCoopDetalleCuentas, verbose_name="Cuentas")

	def __unicode__(self):
		return self.concepto

	class Meta: 
		ordering = ['suplidor','fecha']

			
			
						
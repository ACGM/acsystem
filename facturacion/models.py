# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from administracion.models import Producto, Socio, CategoriaPrestamo


# Cabecera de la Factura
class Factura(models.Model):
	
	facturas_choices = (('A','Activa'),('I','Inactiva'),('N','Anulada'))
	terminos_choices = (('CO','Contado'),('CR','Credito'),)

	noFactura = models.IntegerField(unique=True)
	fecha = models.DateTimeField(auto_now_add=True)
	estatus = models.CharField(max_length=1, choices=facturas_choices, default='A')
	descrpAnulacion = models.CharField(max_length=255, blank=True)
	socio = models.ForeignKey(Socio)
	ordenCompra = models.CharField(max_length=20, blank=True)
	terminos = models.CharField(max_length=2, choices=terminos_choices, default='CO')
	impresa = models.IntegerField(default=0)

	userLog = models.ForeignKey(User)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%i' % (self.no_factura)

	class Meta:
		ordering = ['-noFactura']


# Detalle de la Factura
class Detalle(models.Model):

	factura = models.ForeignKey(Factura)	
	producto = models.ForeignKey(Producto)
	porcentajeDescuento = models.DecimalField(max_digits=6, decimal_places=2,blank=True, default=0)
	cantidad = models.PositiveIntegerField()
	precio = models.PositiveIntegerField()

	def _get_total(self):
		return '%i' % ((self.cantidad * self.precio) - descuento)

	importeValor = property(_get_total)

	def __unicode__(self):
		return u"%s %s" % (self.producto, (self.cantidad * self.precio))


# Orden de Despacho 
class OrdenDespachoSuperCoop(models.Model):

	orden_choices = (('A','Activa'),('I','Inactiva'),('N','Anulada'))
	pagar_por_choices = (('EM','Empresa'),('CA','Cajero'),)
	forma_pago_choices = (('Q','Quincenal'),('M','Mensual'),)
	quincenas_choices = (('1','1ra Quincena'),('2','2da Quincena'),)

	noSolicitud = models.IntegerField()
	categoria = models.ForeignKey(CategoriaPrestamo)
	oficial = models.ForeignKey(User)
	pagarPor = models.CharField(max_length=2, choices=pagar_por_choices, default='EM')
	formaPago = models.CharField(max_length=1, choices=forma_pago_choices, default='Q')
	tasaInteresAnual = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	tasaInteresMensual = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	quincena = models.IntegerField(choices=quincenas_choices, default='1', blank=True)
	cuotas = models.IntegerField(default=2)
	valorCuotas = models.DecimalField(max_digits=12, decimal_places=2)
	estatus = models.CharField(max_length=1, choices=orden_choices, default='A')
	
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%i' % (self.no_solicitud)

	class Meta:
		ordering =['noSolicitud']
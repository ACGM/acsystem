# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from administracion.models import Producto, Socio, CategoriaPrestamo
from inventario.models import Existencia, Movimiento, Almacen


# Cabecera de la Factura
class Factura(models.Model):
	
	facturas_choices = (('A','Activa'),('I','Inactiva'),('N','Anulada'))
	terminos_choices = (('CO','Contado'),('CR','Credito'),)
	posteo_choices = (('N','NO'),('S','SI'))

	posteo = models.CharField(max_length=1, choices=posteo_choices, default='N')
	
	noFactura = models.PositiveIntegerField("No. Factura", unique=True)
	fecha = models.DateTimeField(auto_now_add=True)
	estatus = models.CharField(max_length=1, choices=facturas_choices, default='A')
	descrpAnulacion = models.CharField(max_length=150, blank=True)
	socio = models.ForeignKey(Socio, null=True)
	ordenCompra = models.CharField(max_length=20, blank=True, null=True)
	terminos = models.CharField(max_length=2, choices=terminos_choices, default='CO')
	impresa = models.IntegerField(default=0)

	userLog = models.ForeignKey(User)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u'%i' % (self.noFactura)

	class Meta:
		ordering = ['-noFactura',]

	@property
	def totalGeneral(self):
		total = 0
		for n in Detalle.objects.filter(factura_id=self.id).values('precio','porcentajeDescuento','cantidad'):
			descuento = 0

			if(n['porcentajeDescuento'] > 0):
				descuento = (n['precio'] * float(n['porcentajeDescuento'] / 100)) * n['cantidad']
			total += (n['precio'] * n['cantidad']) - descuento
		
		if total == None:
			total = 0

		return '$%s' % str(format(total,',.2f'))


# Detalle de la Factura
class Detalle(models.Model):

	factura = models.ForeignKey(Factura)	
	producto = models.ForeignKey(Producto)
	porcentajeDescuento = models.DecimalField("Porcentaje Descuento", max_digits=6, decimal_places=2,blank=True, default=0)
	cantidad = models.PositiveIntegerField()
	precio = models.PositiveIntegerField()
	almacen = models.ForeignKey(Almacen)

	class Meta:
		ordering = ('-factura',)

	@property
	def importeValor(self):
		return '%i' % ((self.cantidad * self.precio) - ((self.porcentajeDescuento/100) * self.precio * self.cantidad))

	def __unicode__(self):
		return u"%s %s" % (self.producto, (self.cantidad * self.precio))

	def save(self, *args, **kwargs):
		
		# Actualizar la existencia del producto 
		try:
			exist = Existencia.objects.get(producto=self.producto, almacen=self.almacen)
			
			exist.cantidad -= int(self.cantidad)
			exist.save()

		except Existencia.DoesNotExist:
			raise Exception('NOT_EXISTENCIA')
			# existencia = Existencia()
			# existencia.producto = self.producto

			# existencia.cantidad = (self.cantidad * -1)
			
			# existencia.almacen = self.almacen
			# existencia.save()
			

		# Guardar el movimiento del producto
		mov = Movimiento()
		mov.producto = self.producto
		mov.cantidad = self.cantidad
		mov.almacen = self.almacen
		mov.tipo_mov = 'S'
		mov.save()

		super(Detalle, self).save(*args, **kwargs)


# Orden de Despacho 
class OrdenDespachoSuperCoop(models.Model):

	orden_choices = (('A','Activa'),('I','Inactiva'),('N','Anulada'))
	pagar_por_choices = (('EM','Empresa'),('CA','Cajero'),)
	forma_pago_choices = (('Q','Quincenal'),('M','Mensual'),)
	quincenas_choices = (('1','1ra Quincena'),('2','2da Quincena'),)

	noSolicitud = models.AutoField(primary_key=True)
	categoria = models.ForeignKey(CategoriaPrestamo)
	oficial = models.ForeignKey(User)
	pagarPor = models.CharField(max_length=2, choices=pagar_por_choices, default='EM')
	formaPago = models.CharField(max_length=1, choices=forma_pago_choices, default='Q')
	tasaInteresAnual = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	tasaInteresMensual = models.DecimalField(max_digits=6, decimal_places=2, default=0)
	quincena = models.IntegerField(choices=quincenas_choices, default=1, blank=True)
	cuotas = models.IntegerField(default=2)
	valorCuotas = models.DecimalField(max_digits=18, decimal_places=2)
	estatus = models.CharField(max_length=1, choices=orden_choices, default='A')
	
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%i' % (self.no_solicitud)

	class Meta:
		ordering =['-noSolicitud']
		verbose_name = "Orden Despacho SuperCoop"
		verbose_name_plural = "Ordenes Despacho SuperCoop"
		
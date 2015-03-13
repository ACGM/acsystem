# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from administracion.models import Producto, Socio, CategoriaPrestamo, Localidad
from inventario.models import Existencia, Movimiento, Almacen

import decimal

# Cabecera de la Factura
class Factura(models.Model):
	
	facturas_choices = (('A','Activa'),('I','Inactiva'),('N','Anulada'))
	terminos_choices = (('CO','Contado'),('CR','Credito'),)
	posteo_choices = (('N','NO'),('S','SI'))

	posteo = models.CharField(max_length=1, choices=posteo_choices, default='N')
	
	noFactura = models.PositiveIntegerField("No. Factura", unique=True)
	fecha = models.DateTimeField(auto_now_add=True)
	estatus = models.CharField(max_length=1, choices=facturas_choices, default='A')
	descrpAnulacion = models.CharField(max_length=150, blank=True, null=True)
	socio = models.ForeignKey(Socio, null=True)
	ordenCompra = models.PositiveIntegerField(null=True, blank=True)
	terminos = models.CharField(max_length=2, choices=terminos_choices, default='CO')
	localidad = models.ForeignKey(Localidad, null=True, blank=True)

	borrado = models.BooleanField(default=False)
	borradoPor = models.ForeignKey(User, related_name='+', null=True)
	borradoFecha = models.DateTimeField(null=True)

	impresa = models.PositiveIntegerField(default=0)

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
				descuento = (float(n['precio']) * float(n['porcentajeDescuento'] / 100)) * float(n['cantidad'])
			total += float(n['precio'] * n['cantidad']) - descuento
		
		if total == None:
			total = 0

		return '$%s' % str(format(total,',.2f'))


# Detalle de la Factura
class Detalle(models.Model):

	factura = models.ForeignKey(Factura)	
	producto = models.ForeignKey(Producto)
	porcentajeDescuento = models.DecimalField("Porcentaje Descuento", max_digits=6, decimal_places=2,blank=True, default=0)
	cantidad = models.DecimalField(max_digits=12, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	costo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	almacen = models.ForeignKey(Almacen)

	class Meta:
		ordering = ('-factura',)
		unique_together = ('factura','producto')

	@property
	def importeValor(self):
		return '%s' % 	str(format(
						(float(self.cantidad) * float(self.precio)) - \
						(float(self.porcentajeDescuento/100) * float(self.precio) * float(self.cantidad)) \
						,',.2f'))

	@property
	def getFactura(self):
		return self.factura.noFactura

	@property
	def getFecha(self):
		return self.factura.fecha

	@property
	def getCategoria(self):
		return self.producto.categoria.descripcion

	def __unicode__(self):
		return u"%s %s" % (self.producto, (self.cantidad * self.precio))

	def save(self, *args, **kwargs):

		# Tomar el costo actual del producto que sera vendido (para reportes futuros)
		self.costo = self.producto.costo
		
		# Actualizar la existencia del producto 
		try:
			exist = Existencia.objects.get(producto=self.producto, almacen=self.almacen)
			
			exist.cantidadAnterior = exist.cantidad
			exist.cantidad -= decimal.Decimal(self.cantidad)
			exist.save()

		except Existencia.DoesNotExist:
			raise Exception('Intenta facturar un producto que no tiene existencia ' + self.producto.descripcion)

		# Guardar el movimiento del producto
		mov = Movimiento()
		mov.producto = self.producto
		mov.cantidad = float(self.cantidad)
		mov.precio = self.precio
		mov.costo = self.costo
		mov.almacen = self.almacen
		mov.tipo_mov = 'S'
		mov.documento = 'FACT'
		mov.documentoNo = self.factura.noFactura
		mov.userLog = self.factura.userLog
		mov.save()

		super(Detalle, self).save(*args, **kwargs)

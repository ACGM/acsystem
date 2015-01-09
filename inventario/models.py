# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from administracion.models import Producto, Suplidor

from datetime import timedelta, datetime


# Almacenes disponibles
class Almacen(models.Model):

	descripcion = models.CharField(max_length=20)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Cabecera del Inventario
class InventarioH(models.Model):

	dias_plazo_choices = (('30','30'),('60','60'), ('120','120'),)
	posteo_choices = (('N','NO'),('S','SI'))
	condicion_choices = (('CO','Contado'),('CR','Credito'),)

	fecha = models.DateField(default=datetime.now)
	orden = models.CharField(max_length=30, blank=True, null=True)
	factura = models.CharField(max_length=12, blank=True, null=True)
	
	diasPlazo = models.CharField("Dias de Plazo", max_length=3, choices=dias_plazo_choices,
									default=dias_plazo_choices[0][0], null=True, blank=True)

	nota = models.TextField(blank=True, null=True)
	ncf = models.CharField("NCF", max_length=25, blank=True, null=True)
	descripcionSalida = models.CharField("Descripción de Salida", max_length=255, blank=True, null=True)
	posteo = models.CharField(max_length=1, choices=posteo_choices, default='N')
	condicion = models.CharField(max_length=2, choices=condicion_choices, default='CO')

	suplidor = models.ForeignKey(Suplidor, null=True, blank=True)
	userLog = models.ForeignKey(User)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Inventario Cabecera'
		verbose_name_plural = 'Inventario Cabecera'
		ordering = ('-id',)

	def _get_fecha_vencimiento(self):
		if(self.diasPlazo != None):
			return  (self.fecha+timedelta(days=self.diasPlazo))
		else:
			return ''
	fechaVencimiento = property(_get_fecha_vencimiento)

	@property
	def totalGeneral(self):
		total = 0
		for n in InventarioD.objects.filter(inventario_id=self.id).values('costo','cantidadTeorico'):
			total += n['costo'] * n['cantidadTeorico']
		#total = (InventarioD.objects.filter(inventario_id=self.id).aggregate(total=Sum('costo')))['total'] * InventarioD.objects.filter(inventario_id=self.id).values('cantidadTeorico')
		
		if total == None:
			total = 0

		return '$%s' % str(format(total,',.2f'))

	def __unicode__(self):
		return '%i' % (self.id)

# Detalle del Inventario
class InventarioD(models.Model):

	tipo_accion_choices = (('E','Entrada'),('S','Salida'),)

	inventario = models.ForeignKey(InventarioH)
	producto = models.ForeignKey(Producto)
	almacen = models.ForeignKey(Almacen)
	cantidadTeorico = models.PositiveIntegerField()
	cantidadFisico = models.PositiveIntegerField(null=True, blank=True)
	costo = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
	tipoAccion = models.CharField(max_length=1, 
								choices=tipo_accion_choices, 
								default='E',
								verbose_name="Tipo de Accion")

	class Meta:
		verbose_name = 'Inventario Detalle'
		verbose_name_plural = 'Inventario Detalle'

	def __unicode__(self):
		return '%i' % (self.id)

	def save(self, *args, **kwargs):
		
		# Actualizar la existencia del producto 
		try:
			exist = Existencia.objects.get(producto=self.producto, almacen=self.almacen)
			
			if self.tipoAccion == 'S':
				exist.cantidad -= int(self.cantidadTeorico)
			else:
				exist.cantidad = int(exist.cantidad) + int(self.cantidadTeorico)

			exist.save()
		except Existencia.DoesNotExist:
			existencia = Existencia()
			existencia.producto = self.producto
			
			if self.tipoAccion == 'S':
				existencia.cantidad = -self.cantidadTeorico
			else:
				existencia.cantidad = self.cantidadTeorico
			
			existencia.almacen = self.almacen
			existencia.tipo_mov = self.tipoAccion
			existencia.save()

		# Guardar el movimiento del producto
		mov = Movimiento()
		mov.producto = self.producto
		mov.cantidad = self.cantidadTeorico
		mov.almacen = self.almacen
		mov.tipo_mov = self.tipoAccion
		mov.save()

		super(InventarioD, self).save(*args, **kwargs)


# Movimiento de productos del inventario
class Movimiento(models.Model):

	tipo_mov_choices = (('E','Entrada'),('S','Salida'),)

	producto = models.ForeignKey(Producto)
	cantidad = models.IntegerField()
	almacen = models.ForeignKey(Almacen)
	fecha_movimiento = models.DateField(auto_now_add=True)
	tipo_mov = models.CharField(max_length=1,
								choices=tipo_mov_choices,
								default=tipo_mov_choices[0][0],
								verbose_name="Tipo de Movimiento")
	
	datetime_server = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s - %i (%s) - Almacen: %s' % (self.producto,self.cantidad,self.tipo_mov,self.almacen)

	class Meta:
		ordering = ['producto']


#Existencia de cada producto en cada almacen
class Existencia(models.Model):
	
	producto = models.ForeignKey(Producto)
	cantidad = models.IntegerField()
	almacen = models.ForeignKey(Almacen)
	fecha = models.DateField(auto_now=True)

	def __unicode__(self):
		return '%s - %i' % (self.producto,self.cantidad)

	class Meta:
		ordering = ['producto']
		unique_together = ('producto','almacen')

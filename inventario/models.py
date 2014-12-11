# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from administracion.models import Producto

from datetime import timedelta, datetime


# Almacenes disponibles
class Almacen(models.Model):

	descripcion = models.CharField(max_length=100)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Cabecera del Inventario
class InventarioH(models.Model):

	tipo_accion_choices = (('E','Entrada'),('S','Salida'),)
	dias_plazo_choices = (('30','30'),('60','60'), ('120','120'),)

	fecha = models.DateField(default=datetime.now)
	almacen = models.ForeignKey(Almacen)
	orden = models.CharField(max_length=30)
	factura = models.CharField(max_length=30)
	
	diasPlazo = models.IntegerField(choices=dias_plazo_choices,
									default=dias_plazo_choices[0][0])

	tipoAccion = models.CharField(max_length=1, 
								choices=tipo_accion_choices, 
								default=tipo_accion_choices[0][0],
								verbose_name="Tipo de Accion")

	nota = models.TextField(blank=True)
	ncf = models.CharField(max_length=25, blank=True)
	descripcionSalida = models.CharField(max_length=255, blank=True, verbose_name="Descripción de Salida")

	userLog = models.ForeignKey(User)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def _get_fecha_vencimiento(self):
		return  (self.fecha+timedelta(days=self.diasPlazo))
	fechaVencimiento = property(_get_fecha_vencimiento)


# Detalle del Inventario
class InventarioD(models.Model):

	inventario = models.ForeignKey(InventarioH)
	producto = models.ForeignKey(Producto)
	almacen = models.ForeignKey(Almacen)
	cantidadTeorico = models.PositiveIntegerField()
	cantidadFisico = models.PositiveIntegerField()
	costo = models.DecimalField(max_digits=12, decimal_places=2, blank=True)

	def save(self, *args, **kwargs):
		
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
	
	usr_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s - %i (%s)' % (self.producto,self.cantidad,self.tipo_mov)

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

from django.db import models
from django.contrib.auth import User

from administracion.models import Producto

from datetime import timedelta, datetime


# Almacenes disponibles
class Almacen(models.Model):

	descripcion = models.CharField(max_length=100)


# Cabecera del Inventario
class InventarioH(models.Model):

	tipo_accion_choices = (('E','Entrada'),('S','Salida'),)
	dias_plazo_choices = (('30','30'),('60','60'), ('120','120'),)

	fecha = models.DateField(default=datetime.now)
	almacen = models.ForeignKey(Almacen)
	orden = models.CharField(max_length=30)
	factura = models.CharField(max_length=30)
	
	dias_plazo = models.IntegerField(choices=dias_plazo_choices,
									default=dias_plazo_choices[0][0])

	tipo_accion = models.CharField(max_length=1, 
								choices=tipo_accion_choices, 
								default=tipo_accion_choices[0][0],
								verbose_name="Tipo de Accion")

	fecha_vencimiento = models.DateField(default=fecha+timedelta(days=dias_plazo))
	nota = models.TextField(blank=True)
	ncf = models.CharField(max_length=25, blank=True)
	descripcion_salida = models.CharField(max_length=255, blank=True, verbose_name="Descripción de Salida")

	usr_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)


# Detalle del Inventario
class InventarioD(models.Model):

	inventario = models.ForeignKey(InventarioH)
	producto = models.ForeignKey(Producto)
	almacen = models.ForeignKey(Almacen)
	cantidad_teorico = models.PositiveIntegerField()
	cantidad_fisico = models.PositiveIntegerField()
	costo = models.DecimalField(max_digits=12, decimal_places=2, blank=True)


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

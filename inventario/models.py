# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from administracion.models import Producto, Suplidor

from datetime import timedelta, datetime
import decimal


# Almacenes disponibles
class Almacen(models.Model):

	descripcion = models.CharField(max_length=20)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']
		verbose_name_plural = 'Almacenes'


# Cabecera del Inventario SALIDAS
class InventarioHSalidas(models.Model):

	posteo_choices = (('N','NO'),('S','SI'))

	fecha = models.DateField(default=datetime.now)
	descripcionSalida = models.CharField("Descripción de Salida", max_length=255, blank=True, null=True)
	usuarioSalida = models.ForeignKey(User)
	posteo = models.CharField(max_length=1, choices=posteo_choices, default='N')
	borrado = models.BooleanField(default=False)
	borradoPor = models.ForeignKey(User, related_name='+', null=True, editable=False)
	borradoFecha = models.DateTimeField(null=True)
	
	datetimeServer = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Inventario Cabecera SALIDAS'
		verbose_name_plural = 'Inventario Cabecera SALIDAS'
		ordering = ('-id',)

	@property
	def totalGeneral(self):
		total = 0.0
		for n in InventarioD.objects.filter(inventarioSalida_id=self.id).values('costo','cantidadTeorico'):
			total += float(n['costo']) * float(n['cantidadTeorico'])
		
		if total == None:
			total = 0

		return '$%s' % str(format(total,',.2f'))

	def __unicode__(self):
		return '%i' % (self.id)


# Cabecera del Inventario ENTRADAS
class InventarioH(models.Model):

	posteo_choices = (('N','NO'),('S','SI'))
	cxp_choices = (('E','EN PROCESO'),('P','PROCESADA'))
	condicion_choices = (('CO','Contado'),('CR','Credito'),)

	fecha = models.DateField(default=datetime.now)
	orden = models.CharField(max_length=30, blank=True, null=True)
	factura = models.CharField(max_length=12, blank=True, null=True)
	diasPlazo = models.CharField("Dias de Plazo", max_length=3, null=True, blank=True)
	nota = models.TextField(blank=True, null=True)
	ncf = models.CharField("NCF", max_length=25, blank=True, null=True)
	posteo = models.CharField(max_length=1, choices=posteo_choices, default='N')
	condicion = models.CharField(max_length=2, choices=condicion_choices, default='CO')
	cxp = models.CharField(max_length=1, choices=cxp_choices, default='E')
	suplidor = models.ForeignKey(Suplidor)
	borrado = models.BooleanField(default=False)
	borradoPor = models.ForeignKey(User, related_name='+', null=True, editable=False)
	borradoFecha = models.DateTimeField(null=True)

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
		total = 0.0
		for n in InventarioD.objects.filter(inventario_id=self.id).values('costo','cantidadTeorico'):
			total += float(n['costo']) * float(n['cantidadTeorico'])
		
		if total == None:
			total = 0

		return '$%s' % str(format(total,',.2f'))

	def __unicode__(self):
		return '%i' % (self.id)

# Detalle del Inventario
class InventarioD(models.Model):

	tipo_accion_choices = (('E','Entrada'),('S','Salida'),)

	inventario = models.ForeignKey(InventarioH, null=True)
	inventarioSalida = models.ForeignKey(InventarioHSalidas, null=True)

	producto = models.ForeignKey(Producto)
	almacen = models.ForeignKey(Almacen)
	cantidadTeorico = models.DecimalField(max_digits=12, decimal_places=2)
	cantidadFisico = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	costo = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
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

			exist.cantidadAnterior = exist.cantidad

			if self.tipoAccion == 'S':
				exist.cantidad = decimal.Decimal(exist.cantidad) - decimal.Decimal(self.cantidadTeorico)
				# raise Exception(decimal.Decimal(self.cantidadTeorico))
			else:
				exist.cantidad = decimal.Decimal(exist.cantidad) + decimal.Decimal(self.cantidadTeorico)

			exist.save()

		except Existencia.DoesNotExist:
			existencia = Existencia()
			existencia.producto = self.producto
			
			if self.tipoAccion == 'S':
				raise Exception('El producto ' + existencia.producto.descripcion + ' no tiene existencia.')
				#existencia.cantidad = - decimal.Decimal(self.cantidadTeorico)
			else:
				existencia.cantidad = decimal.Decimal(self.cantidadTeorico)
			
			existencia.almacen = self.almacen
			existencia.tipo_mov = self.tipoAccion
			existencia.save()

		# Guardar el movimiento del producto

		mov = Movimiento()
		mov.producto = self.producto
		mov.cantidad = decimal.Decimal(self.cantidadTeorico)
		mov.precio = self.producto.precio
		mov.costo = self.costo
		mov.almacen = self.almacen
		mov.tipo_mov = self.tipoAccion
		mov.documento = 'SINV' if self.tipoAccion == 'S' else 'EINV'
		mov.documentoNo = self.inventario.id if self.inventario != None else self.inventarioSalida.id
		mov.userLog = self.inventario.userLog if self.inventario != None else self.inventarioSalida.usuarioSalida
		mov.save()

		super(InventarioD, self).save(*args, **kwargs)


# Transferencia entre almacenes
class TransferenciasAlmacenes(models.Model):
	
	desdeAlmacen = models.ForeignKey(Almacen, related_name='+')
	hastaAlmacen = models.ForeignKey(Almacen, related_name='+')
	cantidad = models.DecimalField(max_digits=12, decimal_places=2)
	producto = models.ForeignKey(Producto)
	fechaTransf = models.DateField(auto_now_add=True)
	userLog = models.ForeignKey(User)

	def __unicode__(self):
		return 'desde almacen: %s hacia el almacen: %s' % (self.desdeAlmacen, self.hastaAlmacen)

	class Meta:
		ordering = ('fechaTransf',)
		verbose_name = 'Transferencia entre Almacenes'
		verbose_name_plural = 'Transferencias entre Almacenes'


# Movimiento de productos del inventario
class Movimiento(models.Model):

	tipo_mov_choices = (('E','Entrada'),('S','Salida'),)
	doc_choices = (('EINV', 'Entrada Inventario'), ('SINV', 'Salida Inventario'), ('AINV', 'Ajuste Inventario'), ('FACT', 'Facturacion'))

	producto = models.ForeignKey(Producto)
	cantidad = models.DecimalField(max_digits=12, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	costo = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	almacen = models.ForeignKey(Almacen)
	fechaMovimiento = models.DateField(auto_now_add=True)
	documento = models.CharField(max_length=4, choices=doc_choices)
	documentoNo = models.PositiveIntegerField()
	tipo_mov = models.CharField(max_length=1,
								choices=tipo_mov_choices,
								default=tipo_mov_choices[0][0],
								verbose_name="Tipo de Movimiento")
	
	userLog = models.ForeignKey(User, null=True, editable=False)
	datetime_server = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s - %s (%s) - Almacen: %s --> %s' % (self.producto,self.cantidad,self.tipo_mov,self.almacen, self.documento)

	@property
	def getUsuario(self):
		if self.userLog != None:
			return self.userLog.username
		else:
			return ''

	@property
	def getCodProd(self):
		return self.producto.codigo

	class Meta:
		ordering = ['producto']


#Existencia de cada producto en cada almacen
class Existencia(models.Model):
	
	producto = models.ForeignKey(Producto)
	cantidad = models.DecimalField(max_digits=12, decimal_places=2)
	cantidadAnterior = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	almacen = models.ForeignKey(Almacen)
	fecha = models.DateField(auto_now=True)

	def __unicode__(self):
		return '%s - %s' % (self.producto,self.cantidad)

	@property
	def getCodigo(self):
		return self.producto.codigo

	class Meta:
		ordering = ['producto']
		unique_together = ('producto','almacen')


#Ajuste de Inventario Cabecera
class AjusteInventarioH(models.Model):

	fecha = models.DateField()
	notaAjuste = models.CharField(max_length=200, blank=True, null=True)
	estatus = models.CharField(max_length=1, default='N') #N = En proceso, S = Procesado
	
	usuario = models.ForeignKey(User)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.id)

	class Meta:
		ordering = ('id',)
		verbose_name = 'Ajuste Inventario Cabecera'
		verbose_name_plural = 'Ajuste Inventario Cabecera'

#Ajuste de Inventario Detalle
class AjusteInventarioD(models.Model):

	ajusteInvH = models.ForeignKey(AjusteInventarioH)
	producto = models.ForeignKey(Producto)
	almacen = models.ForeignKey(Almacen)
	cantidadFisico = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
	cantidadTeorico = models.DecimalField(max_digits=12, decimal_places=2, blank=True)

	@property
	def diferencia(self):
		return self.cantidadFisico - self.cantidadTeorico

	def __unicode__(self):
		return '%s = %s' % (self.producto, (self.cantidadFisico - self.cantidadTeorico))

	class Meta:
		verbose_name = 'Ajuste Inventario Detalle'
		verbose_name_plural = 'Ajuste Inventario Detalle'

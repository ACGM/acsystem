# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from cuenta.models import Cuentas
from administracion.models import Localidad

import datetime


# Fondos para desembolsos
class Fondo(models.Model):

	estatus_choices = (('A','Activo'),('I','Inhactivo'),)

	descripcion = models.CharField(max_length=150)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Conceptos de Desembolsos
class ConceptoDesembolso(models.Model):

	descripcion = models.CharField(max_length=255)
	cuentaDebito = models.ForeignKey(Cuentas, related_name='+', verbose_name='Cuenta Debito')
	cuentaCredito = models.ForeignKey(Cuentas, related_name='+', verbose_name='Cuenta Credito')

	userLog = models.ForeignKey(User, null=True, editable=False)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Desembolso Cabecera
class DesembolsoH(models.Model):

	estatus_choices = (('A','Activo'),('N','Anulado'),)

	beneficiario = models.CharField(max_length=80)
	fecha = models.DateField(auto_now=True)
	fondo = models.ForeignKey(Fondo, null=True)
	localidad = models.ForeignKey(Localidad)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')
	impreso = models.PositiveIntegerField(default=0, editable=False)
	cheque = models.PositiveIntegerField(null=True, editable=False)

	
	userLog = models.ForeignKey(User, editable=False)
	datetimeServer = models.DateTimeField(auto_now_add=True)
	modificado = models.DateField(auto_now=True, editable=False)

	def __unicode__(self):
		return '%i' % (self.id)

	class Meta:
		verbose_name = "Desembolso Caja Chica"
		verbose_name_plural = "Desembolsos Caja Chica"
		ordering = ['-id',]

	@property
	def totalGeneral(self):
		total = 0
		for item in DesembolsoD.objects.filter(desembolso_id=self.id):
			total += item.monto

		if total == None:
			total = 0

		return '%s' % str(format(total,',.2f'))


# Desembolso Detalle
class DesembolsoD(models.Model):

	desembolso = models.ForeignKey(DesembolsoH)
	concepto = models.ForeignKey(ConceptoDesembolso)
	monto = models.DecimalField(max_digits=18, decimal_places=2)

	def __unicode__(self):
		return '%i - %s - %d' % (self.desembolso.id, self.concepto.descripcion, self.monto) 

	class Meta:
		verbose_name = "Desembolso Detalle"
		verbose_name_plural = "Desembolsos Detalle"
		ordering = ['-id',]
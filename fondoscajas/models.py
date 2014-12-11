# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from administracion.models import CuentaContable

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
	cuentaDebito = models.ForeignKey(CuentaContable, related_name='+')
	cuentaCredito = models.ForeignKey(CuentaContable, related_name='+')

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Desembolso Cabecera
class DesembolsoH(models.Model):

	estatus_choices = (('A','Activo'),('N','Anulado'),)

	beneficiario = models.TextField()
	monto = models.DecimalField(max_digits=12, decimal_places=2)
	fecha = models.DateField(auto_now=True)
	estatus = models.CharField(max_length=1, default='A')
	impreso = models.PositiveIntegerField(default=0)
	
	userLog = models.ForeignKey(User)
	datetimeServer = models.DateTimeField(auto_now_add=True)


# Desembolso Detalle
class DesembolsoD(models.Model):

	desembolso = models.ForeignKey(DesembolsoH)
	concepto = models.ForeignKey(ConceptoDesembolso)
	monto = models.DecimalField(max_digits=12, decimal_places=2)
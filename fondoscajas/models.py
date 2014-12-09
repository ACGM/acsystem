from django.db import models
from django.contrib.auth import User

from administracion.models import CuentaContable

import datetime


# Fondos para desembolsos
class Fondo(models.Model):

	estatus_choices = (('A','Activo'),('I','Inhactivo'),)

	descripcion = models.CharField(max_length=150)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')

	def __unicode__(self):
		return '%s' % (self.descripcion)


# Conceptos de Desembolsos
class ConceptoDesembolso(models.Model):

	descripcion = models.CharField(max_length=255)
	cuenta_debito = models.ForeignKey(CuentaContable)
	cuenta_credito = models.ForeignKey(CuentaContable)


# Desembolso Cabecera
class DesembolsoH(models.Model):

	estatus_choices = (('A','Activo'),('N','Anulado'),)

	beneficiario = models.TextField()
	monto = models.DecimalField(max_digits=12, decimal_places=2)
	fecha = models.DateField(default=datetime.now())
	estatus = models.CharField(max_length=1, default='A')
	impreso = models.PositiveIntegerField(default=0)
	user_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)


# Desembolso Detalle
class DesembolsoD(models.Model):

	desembolso = models.ForeignKey(DesembolsoH)
	concepto = models.ForeignKey()
	monto = models.DecimalField(max_digits=12, decimal_places=2)
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Cuentas(models.Model):

	# Catalogo de Cuentas Contables
	"""docstring for Cuentas"""
	
	#Origenes de cuentas
	origen_choices = (('D','Debito'),('C','Credito'),)

	#Campos Base
	codigo = models.PositiveIntegerField(verbose_name="Código Cuenta", null=False, default=False, blank=False)
	descripcion = models.CharField(max_length=100, verbose_name="Descripcion", blank=False, null=False)
	origen = models.CharField(max_length=1, choices=origen_choices, verbose_name="Origen de la cuenta")
	#Para Identificar si es una cuenta Control
	control =models.BooleanField(default=False)
	cuentaControl = models.PositiveIntegerField(default=False, verbose_name="Cuenta Control", null=True, blank=True)

	def __unicode__(self):
		return '%s-%s' % (self.codigo,self.descripcion)

	class Meta: 
		ordering = ['codigo']

class Auxiliares(models.Model):
  #auxiliares Contables

  codigo = models.PositiveIntegerField(verbose_name="Código Auxiliar", null=False, default=False, blank=False)
  descripcion = models.CharField(max_length=200,verbose_name="Descripcion", blank=False, null=False)
  cuenta = models.ForeignKey(Cuentas, verbose_name="Cuenta", null=False, blank=False)


class DiarioGeneral(models.Model):
	"""docstring for DiarioGeneral"""
	fecha = models.DateTimeField()
	cuenta = models.ForeignKey(Cuentas, verbose_name="Cuenta", null=True, blank=True)
	referencia = models.PositiveIntegerField(verbose_name="Ref", blank=False, null=False, default=False)
	auxiliar = models.ForeignKey(Auxiliares, verbose_name="Aux", null=True, blank=True)
	tipoDoc = models.CharField(max_length=3, default=False, blank=False, null=False, verbose_name="Tipo de Doc")
	debito = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Debito")
	Credito = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Credito")

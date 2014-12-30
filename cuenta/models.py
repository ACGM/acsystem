# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
class Cuentas(models.Model):

	# Catalogo de Cuentas Contables
	"""docstring for Cuentas"""
	
	#Origenes de cuentas
	origen_choices = (('D','Debito'),('C','Credito'),)

	#Campos Base
	codigo = models.PositiveIntegerField(verbose_name="Código Cuenta", null=False, blank=False, unique=True)
	descripcion = models.CharField(max_length=100, verbose_name="Descripcion", blank=False, null=False)
	origen = models.CharField(max_length=1, choices=origen_choices, verbose_name="Origen de la cuenta")
	#Para Identificar si es una cuenta Control
	control =models.BooleanField(default=False)
	cuentaControl = models.PositiveIntegerField(verbose_name="Cuenta Control", null=True, blank=True)

	def __unicode__(self):
		return '%s-%s' % (self.codigo,self.descripcion)

	class Meta: 
		ordering = ['codigo']

class Auxiliares(models.Model):
  #auxiliares Contables

  codigo = models.PositiveIntegerField(verbose_name="Código Auxiliar", null=False,blank=False, unique=True)
  descripcion = models.CharField(max_length=200,verbose_name="Descripcion", blank=False, null=False)
  cuenta = models.ForeignKey(Cuentas, verbose_name="Cuenta", null=False, blank=False)

  def __unicode__(self):
  	return '%s-%s' % (self.codigo,self.descripcion)

  class Meta: 
  	ordering = ['codigo']

class TipoDocumento(models.Model):
	tipoDoc=models.CharField(max_length=4, verbose_name='Tipo de Documento', blank=False, unique=True)
	descripcion= models.CharField(max_length=100, verbose_name='Descripcion', blank=False)


class DiarioGeneral(models.Model):
	estatus_choicer=(('P','Posteada'),('R','Registrada'),('C','Cancelada'))

	fecha = models.DateTimeField()
	cuenta = models.ForeignKey(Cuentas, verbose_name="Cuenta", null=True, blank=True)
	referencia = models.PositiveIntegerField(verbose_name="Ref", blank=False, null=False)
	auxiliar = models.ForeignKey(Auxiliares, verbose_name="Aux", null=True, blank=True)
	tipoDoc = models.ForeignKey(TipoDocumento)
	estatus =models.CharField(max_length=1, choices=estatus_choicer, default='R')
	debito = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Debito")
	credito = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Credito")

	def __unicode__(self): 
		return id

	class Meta:
		ordering=['fecha']


from django.db import models

# Create your models here.
class Cuentas(models.Model):

	# Catalogo de Cuentas Contables
	"""docstring for Cuentas"""
	
	#Origenes de cuentas
	origen_choices = (('D','Debito'),('o','Credito'),)

	#Campos Base
	codigo=models.PositiveIntegerField(verbose_name="Codigo Cuenta", null=false, default=false, blank=false)
	descripcion=models.CharField(max_length=255,verbose_name="Descripcion", blank=false, null=false)
	origen=models.CharField(max_length=1,choices=origen_choices,verbose_name="Origen de la cuenta")
	cuentaControl=models.PositiveIntegerField(default=false, verbose_name="Cuenta Control", null=true, blank=true)

	def __init__(self, arg):
		super(Cuentas, self).__init__()
		self.arg = arg


class Auxiliares(models.Model):
  #auxiliares Contables

  codigo=models.PositiveIntegerField(verbose_name="Codigo Auxiliar", null=false, default=false, blank=false)
  descripcion=models.CharField(max_length=200,verbose_name="Descripcion", blank=false, null=false)
  cuenta=models.ForeignKey(Cuentas, verbose_name="Cuenta", null=false, blank=false)


class DiarioGeneral(models.Model):
	"""docstring for DiarioGeneral"""
	fecha=models.DateTimeField()
	cuenta=models.ForeignKey(Cuentas, verbose_name="Cuenta", null=true, blank=true)
	auxiliar=models.ForeignKey(Auxiliares, verbose_name="Aux", null=true, blank=true)
	tipoDoc=CharField(max_length=3, default=false, blank=false, null=false verbose_name="Tipo de Doc")
	debito=DecimalField(max_digits=18, decimal_places=2, verbose_name="Debito")
	Credito=DecimalField(max_digits=18, decimal_places=2, verbose_name="Credito")


	def __init__(self, arg):
		super(DiarioGeneral, self).__init__()
		self.arg = arg
		
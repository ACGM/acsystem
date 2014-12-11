from django.db import models
from cuenta import Cuentas

# Create your models here.
class MayorGeneral(models.Model):
	"""docstring for MayorGeneral"""
	agno=models.PositiveIntegerField(max_digits=4, default=false, null=false, blank=false, verbose_name="Año")
	mes=models.PositiveIntegerField(max_digits=12, default=false, null=false, blank=false, verbose_name="Mes")
	dia=models.PositiveIntegerField(max_digits=31, default=false, null=false, blank=false, verbose_name="Dia")
	cuenta=models.ForeignKey(Cuentas, null=false, blank=false, default=false, verbose_name="Cuenta Contable")
	debito=models.DecimalFiels(max_digits=18, decimal_places=2, default=false, blank=false, null=false, verbose_name="Debito")
	credito=models.DecimalFiels(max_digits=18, decimal_places=2, default=false, blank=false, null=false, verbose_name="Credito")
	balance=models.DecimalFiels(max_digits=18, decimal_places=2, default=false, blank=false, null=false, verbose_name="Balance")

	def __init__(self, arg):
		super(MayorGeneral, self).__init__()
		self.arg = arg
		

class BalanzaComprobacion(object):
	"""docstring for BalanzaComprobacion"""
	agno=models.PositiveIntegerField(max_digits=4, default=false, null=false, blank=false, verbose_name="Año")
	mes=models.PositiveIntegerField(max_digits=12, default=false, null=false, blank=false, verbose_name="Mes")
	diaDesde=models.PositiveIntegerField(max_digits=31, default=false, null=false, blank=false, verbose_name="Desde")
	diaHasta=models.PositiveIntegerField(max_digits=31, default=false, null=false, blank=false, verbose_name="Hasta")
	cuenta=models.ForeignKey(Cuentas, null=false, blank=false), default=false, verbose_name="Cuenta Contable")
	debito=models.DecimalFiels(max_digits=18, decimal_places=2, default=false, blank=false, null=false, verbose_name="Debito")
	credito=models.DecimalFiels(max_digits=18, decimal_places=2, default=false, blank=false, null=false, verbose_name="Credito")


	def __init__(self, arg):
		super(BalanzaComprobacion, self).__init__()
		self.arg = arg

class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg

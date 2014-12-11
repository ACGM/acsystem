from django.db import models

# Create your models here.
class MayorGeneral(models.Model):
	"""docstring for MayorGeneral"""
	agno=models.PositiveIntegerField(max_digits=4, default=false, null=false, blank=false, verbose_name="Año")
	mes=models.PositiveIntegerField(max_digits=12, default=false, null=false, blank=false, verbose_name="Mes")
	dia=models.PositiveIntegerField(max_digits=31, default=false, null=false, blank=false, verbose_name="Dia")
	def __init__(self, arg):
		super(MayorGeneral, self).__init__()
		self.arg = arg
		
from django.db import models

from administracion.models import Socio, CoBeneficiario
from cuenta.models import Cuentas, Auxiliares, DiarioGeneral

#Maneja todas las transacciones de ahorro realizada en las quincenas
class MaestraAhorro(models.Model):

	fecha=models.DateTimeField()
	socio=models.ForeignKey(Socio, null=True, blank=True)
	beneficiario=models.ForeignKey(CoBeneficiario, null=True, blank=True)
	monto=models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Monto", null=False, blank=False)
	interes=models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Interes", null=False, blank=False)
	balance=models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Balance", null=False, blank=False)
	estatus=models.BooleanField(default=False)
	cuentas=models.ManyToManyField(DiarioGeneral,verbose_name="Cuentas", related_name='maestraAhorro_rel')


#Almacena el ahorro y disponible de cada Socio
class AhorroSocio(models.Model):
	socio=models.ForeignKey(Socio,unique=True, null=True, blank=True)
	beneficiario=models.ForeignKey(CoBeneficiario, null=True, blank=True)
	balance=models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, verbose_name="Balance Socio")
	disponible=models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, verbose_name="Disponible")
	cuentas=models.ManyToManyField(DiarioGeneral, verbose_name="Cuentas", related_name="ahorro_rel")

#Retiros de ahorro
class RetiroAhorro(models.Model):
	retiro_choicer=(('A','Retiro Ahorro'),('J','Retiro por Ajuste'),('O','Otros'))

	socio=models.ForeignKey(Socio, null=True, blank=True)
	beneficiario=models.ForeignKey(CoBeneficiario, null=True, blank=True)
	ahorro=models.ForeignKey(AhorroSocio)
	tipoRetiro= models.CharField(max_length=1, choices=retiro_choicer, verbose_name="Tipo de Retiro")
	monto=models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=0.00, verbose_name="Monto a Retirar")
	cuentas=models.ManyToManyField(DiarioGeneral, verbose_name="Cuentas", related_name='retiroAhorro_rel')






from django.db import models

from administracion.models import Socio
from prestamos.models import MaestraPrestamo
from ahorro.models import AhorroSocio
from cuenta.models import Cuentas, Auxiliares

#Registra todos los ingresos externos para un prestamo o el ahorro.
class RecibosIngreso(models.Model):
	socioIngreso=models.ForeignKey(Socio)
	prestamo=models.ForeignKey(MaestraPrestamo,null=True, blank=True)
	ahorro= models.ForeignKey(AhorroSocio, null=True, blank=True)
	montoPrestamo= models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="Rebajar a PRestamo")
	montoAhorro= models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="Ingreso a Ahorro")
#identifica si esta posteada o no
	estatus=models.BooleanField(default=False)

#Detalle de registros para prestamos
class DetalleRecibo(models.Model):
	recibo=models.ForeignKey(RecibosIngreso)
	montoCuota=models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Monto Cuota")
	montoDistribuir=models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Por Distribuir")

#Detalle de las cuentas contables o auxiliares a afectar
class DetalleCuentasRecibo(models.Model):
	referencia=models.ForeignKey(MaestraPrestamo, null=False, blank=False)
	cuenta=models.ForeignKey(Cuentas, null=True, blank=True, verbose_name="Cuenta Contable")
	auxiliar=models.ForeignKey(Auxiliares, null=True, blank=True, verbose_name="Aux")
	debito=models.DecimalField(max_digits=18, decimal_places=2, null=False, default=0.00, verbose_name="Debito")
	credito=models.DecimalField(max_digits=18, decimal_places=2, null=False, default=0.00, verbose_name="Credito")





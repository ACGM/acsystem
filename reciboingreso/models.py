from django.db import models

from administracion.models import Socio
from prestamos.models import MaestraPrestamo
from ahorro.models import AhorroSocio
from cuenta.models import DiarioGeneral

# Detalle de registros para prestamos
class DetalleRecibo(models.Model):
    cantCuotas = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="Cantidad de cuotas")
    montoCuota = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Monto Cuota")
    montoDistribuir = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Por Distribuir")


    def __unicode__(self):
        return '%i' % (self.id)

    class Meta:
        ordering = ['id']

# Registra todos los ingresos externos para un prestamo o el ahorro.
class RecibosIngreso(models.Model):
    estatus_choices = (('R', 'Registrado'), ('I', 'Inactivas'), ('P', 'Posteada'))

    socioIngreso = models.ForeignKey(Socio)
    prestamo = models.ForeignKey(MaestraPrestamo, null=True, blank=True)
    ahorro = models.ForeignKey(AhorroSocio, null=True, blank=True)
    montoPrestamo = models.DecimalField(max_digits=18, decimal_places=2, default=0.00,
                                        verbose_name="Rebajar a Prestamo")
    montoAhorro = models.DecimalField(max_digits=18, decimal_places=2, default=0.00, verbose_name="Ingreso a Ahorro")
    fecha = models.DateField()

    # identifica si esta posteada o no
    estatus = models.CharField(max_length=1, choices=estatus_choices, verbose_name="Estatus")
    # detallePrestamo = models.ForeignKey(DetalleRecibo, null=True)
    cuentas = models.ManyToManyField(DiarioGeneral, verbose_name="Cuentas", related_name="recibo_rel")

    def __unicode__(self):
        return '%i - %s' % (self.id, self.fecha)

    class Meta:
        ordering = ['id']







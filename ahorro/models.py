from django.db import models

from administracion.models import Socio
from cuenta.models import DiarioGeneral

# Manejo de intereces de ahorro
class InteresesAhorro(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name="Descripcion")
    porcentaje = models.DecimalField(max_digits=2, decimal_places=2, null=False, blank=False)

    def __unicode__(self):
        return '%i - %s' % (self.id, self.descripcion)

    class Meta:
        ordering = ['descripcion']


# Almacena el ahorro y disponible de cada Socio
class AhorroSocio(models.Model):
    socio = models.ForeignKey(Socio, unique=True)
    balance = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False,
                                  verbose_name="Balance Socio")
    disponible = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False,
                                     verbose_name="Disponible")

    def __unicode__(self):
        return '%s-%s' % (str(self.pk), self.socio.nombreCompleto)


# Retiros de ahorro
class RetiroAhorro(models.Model):
    estatus_choices = (('A', 'Activas'), ('I', 'Inactivas'), ('P', 'Posteada'))
    retiro_choicer = (('A', 'Retiro Ahorro'), ('J', 'Retiro por Ajuste'), ('O', 'Otros'))

    fecha = models.DateField()
    socio = models.ForeignKey(Socio)
    tipoRetiro = models.CharField(max_length=1, choices=retiro_choicer, verbose_name="Tipo de Retiro")
    estatus = models.CharField(max_length=1, choices=estatus_choices, verbose_name="Estatus", default="A")
    monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=0.00,
                                verbose_name="Monto a Retirar")

    def __unicode__(self):
        return '%i-%s' % (self.id, self.socio)


# Maneja todas las transacciones de ahorro realizada en las quincenas
class MaestraAhorro(models.Model):
    estatus_choices = (('A', 'Activas'), ('I', 'Inactivas'), ('P', 'Posteada'))

    fecha = models.DateField()
    ahorro = models.ForeignKey(AhorroSocio, null=False, blank=False)
    retiro = models.ForeignKey(RetiroAhorro, null=True, blank=True)
    monto = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Monto", null=False, blank=False)
    interes = models.ForeignKey(InteresesAhorro)
    balance = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Balance", null=False, blank=False)
    estatus = models.CharField(max_length=1, choices=estatus_choices, verbose_name="Estatus")
    cuentas = models.ManyToManyField(DiarioGeneral, verbose_name="Cuentas", related_name="ahorro_rel")

    def __unicode__(self):
        return '%i' % self.id

    class Meta:
        ordering = ['fecha']








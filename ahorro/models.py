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
    estatus_choices = (('A', 'Activas'), ('I', 'Inactivo'))

    socio = models.ForeignKey(Socio, unique=True)
    balance = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False,
                                  verbose_name="Balance Socio")
    disponible = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False,
                                     verbose_name="Disponible")
    estatus = models.CharField(max_length=1, choices=estatus_choices, verbose_name="Estatus")

    def __unicode__(self):
        return '%s-%s' % (str(self.pk), self.socio.nombreCompleto)

# Maneja todas las transacciones de ahorro realizada en las quincenas
class MaestraAhorro(models.Model):
    estatus_choices = (('A', 'Activas'), ('I', 'Inactivas'), ('P', 'Posteada'))
    tipo_choices = (('R', 'Retiro'), ('I', 'Ingresos'))

    fecha = models.DateField()
    ahorro = models.ForeignKey(AhorroSocio, null=False, blank=False)
    prestamo = models.PositiveIntegerField(null=True, blank=True, verbose_name="# Prestamo")
    monto = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Monto", null=False, blank=False)
    tipo = models.CharField(max_length=1, choices=tipo_choices, verbose_name="Tipo", default="I")
    estatus = models.CharField(max_length=1, choices=estatus_choices, verbose_name="Estatus")
    cuentas = models.ManyToManyField(DiarioGeneral, verbose_name="Cuentas", related_name="ahorro_rel")

    def __unicode__(self):
        return '%i' % self.id

    class Meta:
        ordering = ['fecha']


class ahorroGenerados(models.Model):
    tipo_choices = (('A', 'Ahorro'), ('I', 'Interes'))

    fecha = models.DateField()
    tipoRegistro = models.CharField(max_length=1, choices=tipo_choices, verbose_name="Tipo Registro")

    







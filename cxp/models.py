from django.db import models
from administracion.models import Suplidor, Socio
from cuenta.models import Cuentas, DiarioGeneral


# Registro de ordenes de compra a Socio
class OrdenCompra(models.Model):
    estatus_choices = (('A', 'Activas'), ('I', 'Inactivas'), ('P', 'Posteada'))

    suplidor = models.ForeignKey(Suplidor, null=False, blank=False, default=False, verbose_name="Suplidor")
    socio = models.ForeignKey(Socio, null=False, blank=False, default=False, verbose_name="Socio")
    orden = models.PositiveIntegerField(null=False, blank=False, verbose_name="# Orden")
    fecha = models.DateField(verbose_name="Fecha")
    monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, verbose_name="Monto")
    estatus = models.CharField(max_length=1, choices=estatus_choices, verbose_name="Estatus")
    detalleCuentas = models.ManyToManyField(DiarioGeneral, related_name="diario_ref", verbose_name='Detalle Cuentas')

    def __unicode__(self):
        return '%s-%s' % (str(self.orden), self.suplidor.nombre)

    class Meta:
        ordering = ['suplidor', 'fecha']


# Cuenta por pagar a suplidor de SuperCoop
class CxpSuperCoop(models.Model):
    estatus_choices = (('A', 'Activas'), ('I', 'Inactivas'), ('P', 'Posteada'))

    suplidor = models.ForeignKey(Suplidor, null=False, blank=False, default=False, verbose_name="Suplidor")
    factura = models.CharField(max_length=10, default=False, null=False, blank=False, verbose_name="# Factura")
    fecha = models.DateField(verbose_name="Fecha")
    concepto = models.CharField(max_length=255, null=False, blank=False, default=False, verbose_name="Concepto")
    monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False,
                                verbose_name="Monto")
    descuento = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False,
                                    verbose_name="Desc")
    estatus = models.CharField(max_length=1, choices=estatus_choices, verbose_name="Estatus")
    detalleCuentas = models.ManyToManyField(DiarioGeneral, related_name="diario_super_ref",
                                            verbose_name='Detalle Cuentas', null=True, blank=True)

    def __unicode__(self):
        return '%s-%s' %(str(self.factura), self.suplidor.nombre)

    class Meta:
        ordering = ['suplidor', 'fecha']

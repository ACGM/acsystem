from django.db import models
from administracion.models import Suplidor, Socio
from cuenta.models import Cuentas, Auxiliares, DiarioGeneral

# Detalle de articulos y precio del mismo de la Orden
class DetalleOrden(models.Model):
    articulo = models.CharField(max_length=200, default=False, blank=False, null=False, verbose_name="Articulo")
    monto = models.DecimalField(max_digits=18, decimal_places=2, blank=False, null=False, verbose_name="Precio")
    orden = models.PositiveIntegerField(verbose_name='Orden')
    def __unicode__(self):
        return self.articulo

    class Meta:
        ordering = ['articulo']


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
    suplidor = models.ForeignKey(Suplidor, null=False, blank=False, default=False, verbose_name="Suplidor")
    factura = models.CharField(max_length=10, default=False, null=False, blank=False, verbose_name="# Factura")
    fecha = models.DateField(verbose_name="Fecha")
    concepto = models.CharField(max_length=255, null=False, blank=False, default=False, verbose_name="Concepto")
    monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False,
                                verbose_name="Monto")
    descuento = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False,
                                    verbose_name="Desc")
    estatus = models.BooleanField(default=False)
    detalleCuentas = models.ManyToManyField(DiarioGeneral, related_name="diario_super_ref",
                                            verbose_name='Detalle Cuentas')

    def __unicode__(self):
        return '%s-%s' %(str(self.factura), self.suplidor.nombre)

    class Meta:
        ordering = ['suplidor', 'fecha']

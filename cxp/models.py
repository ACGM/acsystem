from django.db import models
from administracion.models import Suplidor, Socio
from cuenta.models import Cuentas, DiarioGeneral


# # Registro de ordenes de compra a Socio
# class OrdenCompra(models.Model):
#     estatus_choices = (('A', 'Activas'), ('I', 'Inactivas'), ('P', 'Posteada'))
#     estatusCh_choices =(('R', 'Registrado'),('N','No Emitida'), ('S', 'Disponible Solicitud'))

#     suplidor = models.ForeignKey(Suplidor, null=False, blank=False, default=False, verbose_name="Suplidor")
#     socio = models.ForeignKey(Socio, null=False, blank=False, default=False, verbose_name="Socio")
#     orden = models.PositiveIntegerField(null=False, blank=False, verbose_name="# Orden")
#     fecha = models.DateField(verbose_name="Fecha")
#     monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, verbose_name="Monto")
#     estatus = models.CharField(max_length=1, choices=estatus_choices, verbose_name="Estatus")
#     estatusCh = models.CharField(max_length=1, choices=estatusCh_choices, verbose_name="Estatus Solicitud", default='N')
#     detalleCuentas = models.ManyToManyField(DiarioGeneral, related_name="diario_ref", verbose_name='Detalle Cuentas')

#     def __unicode__(self):
#         return '%s-%s' % (str(self.orden), self.suplidor.nombre)

#     class Meta:
#         ordering = ['suplidor', 'fecha']


# # Cuenta por pagar a suplidor de SuperCoop
# class CxpSuperCoop(models.Model):
#     estatus_choices = (('A', 'Activas'), ('I', 'Inactivas'), ('P', 'Posteada'))
#     estatusCh_choices =(('R', 'Registrado'),('N','No Emitida'),('S', 'Disponible Solicitud'))

#     suplidor = models.ForeignKey(Suplidor, null=False, blank=False, default=False, verbose_name="Suplidor")
#     factura = models.CharField(max_length=10, default=False, null=False, blank=False, verbose_name="# Factura")
#     fecha = models.DateField(verbose_name="Fecha")
#     concepto = models.CharField(max_length=255, null=False, blank=False, default=False, verbose_name="Concepto")
#     monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False,
#                                 verbose_name="Monto")
#     descuento = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False,
#                                     verbose_name="Desc")
#     estatus = models.CharField(max_length=1, choices=estatus_choices, verbose_name="Estatus")
#     estatusCh = models.CharField(max_length=1, choices=estatusCh_choices, verbose_name="Estatus Solicitud", default='N')
#     detalleCuentas = models.ManyToManyField(DiarioGeneral, related_name="diario_super_ref",
#                                             verbose_name='Detalle Cuentas', null=True, blank=True)

#     def __unicode__(self):
#         return '%s-%s' %(str(self.factura), self.suplidor.nombre)

#     class Meta:
#         ordering = ['suplidor', 'fecha']


class OrdenDetalleFact(models.Model):
    idRegistro = models.PositiveIntegerField(null=False, blank=False, verbose_name="Registro")
    factura = models.CharField(max_length=15, default=False, null=False, blank=False, verbose_name="# Factura")
    fecha = models.DateField(verbose_name="Fecha")
    monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False,
                                verbose_name="Monto")

    def __unicode__(self):
        return '%s-%s' %(self.factura,str(self.fecha))

    class Meta:
        ordering = ['fecha', 'factura']

class OrdenGeneral(models.Model):
    estatus_choices = (('A', 'Activas'), ('N', 'Nula'), ('P', 'Posteada'))
    estatusCh_choices =(('N','No Emitida'),('S', 'Disponible Solicitud'))

    suplidor = models.ForeignKey(Suplidor, null=False, blank=False, default=False, verbose_name="Suplidor")
    fecha = models.DateField(verbose_name="Fecha")
    concepto = models.CharField(max_length=255, null=False, blank=False, default=False, verbose_name="Concepto")
    monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False,
                                verbose_name="Monto")
    descuento = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False,
                                    verbose_name="Desc")
    estatus = models.CharField(max_length=1, choices=estatus_choices, verbose_name="Estatus")
    chk = models.CharField(max_length=1, choices=estatusCh_choices, verbose_name="Chk Solicitado", default='N')
    detalle = models.ManyToManyField(OrdenDetalleFact, related_name="Orden_Detalle", verbose_name="Detalle", null=False, blank=False)
    cuentas = models.ManyToManyField(DiarioGeneral, related_name="diario_OG_ref",
                                            verbose_name='Cuentas', null=True, blank=True)

    def __unicode__(self):
        return '%s-%s' %(str(self.fecha), str(self.monto))

    class Meta:
        ordering = ['fecha','monto']

class cxpSuperDetalle(models.Model):
    idRegistro = models.PositiveIntegerField(null=False, blank=False, verbose_name="Registro")
    fecha = models.DateField(verbose_name='Fecha')
    monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False,
                                verbose_name="Monto")

class cxpSuperGeneral(models.Model):
    estatus_choices = (('A', 'Activas'), ('I', 'Inactivas'), ('P', 'Posteada'))
    estatusCh_choices =(('N','No Emitida'),('S', 'Disponible Solicitud'))

    suplidor = models.ForeignKey(Suplidor, null=False, blank=False, default=False, verbose_name="Suplidor")
    fecha = models.DateField(verbose_name='Fecha')
    concepto = models.CharField(max_length=255, null=False, blank=False, verbose_name="Concepto")
    monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False,
                                verbose_name="Monto")
    descuento = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=False,
                                    verbose_name="Desc")
    estatus = models.CharField(max_length=1, choices=estatus_choices, verbose_name="Estatus")
    chk = models.CharField(max_length=1, choices=estatusCh_choices, verbose_name="Chk Solicitado", default='N')
    detalle = models.ManyToManyField(cxpSuperDetalle, related_name="super_Detalle", verbose_name="Detalle", null=False, blank=False)
    cuentas = models.ManyToManyField(DiarioGeneral, related_name="diario_super_cuenta",
                                            verbose_name='Cuentas', null=True, blank=True)






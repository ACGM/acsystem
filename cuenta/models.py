# -*- coding: utf-8 -*-

from django.db import models

class CuentasControl(models.Model):
    codigoControl = models.PositiveIntegerField('Cuenta control', unique=True)
    descripcion = models.CharField(max_length=100, verbose_name="Descripcion", blank=False, null=False)

    class Meta:
        ordering = ['codigoControl', ]

    def __unicode__(self):
        return '%i-%s' % (self.codigoControl, self.descripcion)


# Create your models here.
class Cuentas(models.Model):
    # Catalogo de Cuentas Contables

    # Origenes de cuentas
    origen_choices = (('D', 'Debito'), ('C', 'Credito'),)
    tipo_choicer = (('G', 'General'), ('D', 'Detalle'))
    tipo_socio = (('N', 'Normal'), ('S', 'Socio'), ('E', 'Empleado'),)

    # Campos Base
    codigo = models.PositiveIntegerField(verbose_name="Código Cuenta", null=False, blank=False, unique=True)
    descripcion = models.CharField(max_length=100, verbose_name="Descripcion", blank=False, null=False)
    origen = models.CharField(max_length=1, choices=origen_choices, verbose_name="Origen de la cuenta")
    tipo = models.CharField(max_length=1, choices=tipo_choicer, verbose_name="Tipo Cuenta")
    #Para Identificar si es una cuenta Control
    control = models.BooleanField(default=False)
    cuentaControl = models.ForeignKey(CuentasControl, null=True, blank=True)
    tipoSocio = models.CharField(max_length=1, choices=tipo_socio, default='S')

    def __unicode__(self):
        return '%s-%s' % (str(self.codigo), self.descripcion)

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        ordering = ['codigo']

    def save(self, *args, **kwargs):
        if self.control:
            cuentaControl = CuentasControl()
            cuentaControl.codigoControl = self.codigo
            cuentaControl.descripcion = self.descripcion
            cuentaControl.save()

        super(Cuentas, self).save(*args, **kwargs)


# Auxiliares Contables
# class Auxiliar(models.Model):

#     codigo = models.CharField(verbose_name="Código Auxiliar", max_length=20, null=False, blank=False, unique=True)
#     socio = models.PositiveIntegerField(null=True, blank=True)
#     suplidor = models.PositiveIntegerField(null=True, blank=True)
#     cuenta = models.ForeignKey(Cuentas, verbose_name="Cuenta")

#     def __unicode__(self):
#         return '%s' % (self.codigo)

#     class Meta:
#         verbose_name = 'Auxiliar'
#         verbose_name_plural = 'Auxiliares'
#         ordering = ['codigo']


class DiarioGeneral(models.Model):
    estatus_choicer = (('P', 'Posteada'), ('R', 'Registrada'), ('C', 'Cancelada'))

    fecha = models.DateField()
    cuenta = models.ForeignKey(Cuentas, verbose_name="Cuenta", null=True, blank=True)
    referencia = models.CharField("Ref", max_length=30, blank=False, null=False)
    # auxiliar = models.ForeignKey(Auxiliar, verbose_name="Aux", null=True, blank=True)
    estatus = models.CharField(max_length=1, choices=estatus_choicer, default='R')
    debito = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Debito")
    credito = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Credito")

    def __unicode__(self):
        return '%i' % (self.id)


    class Meta:
        ordering = ['fecha']


# -*- coding: utf-8 -*-

from django.db import models

from cuenta.models import Cuentas

# Create your models here.
class MayorGeneral(models.Model):
    """docstring for MayorGeneral"""
    agno = models.PositiveIntegerField(max_length=4, default=False, null=False, blank=False, verbose_name="Agno")
    mes = models.PositiveIntegerField(max_length=12, default=False, null=False, blank=False, verbose_name="Mes")
    dia = models.PositiveIntegerField(max_length=31, default=False, null=False, blank=False, verbose_name="Dia")
    cuenta = models.ForeignKey(Cuentas, verbose_name="Cuenta Contable")
    debito = models.DecimalField(max_digits=18, decimal_places=2, default=False, blank=False, null=False,
                                 verbose_name="Debito")
    credito = models.DecimalField(max_digits=18, decimal_places=2, default=False, blank=False, null=False,
                                  verbose_name="Credito")
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=False, blank=False, null=False,
                                  verbose_name="Balance")


class BalanzaComprobacion(object):
    """docstring for BalanzaComprobacion"""
    agno = models.PositiveIntegerField(max_length=4, default=False, null=False, blank=False, verbose_name="Agno")
    mes = models.PositiveIntegerField(max_length=12, default=False, null=False, blank=False, verbose_name="Mes")
    diaDesde = models.PositiveIntegerField(max_length=31, default=False, null=False, blank=False, verbose_name="Desde")
    diaHasta = models.PositiveIntegerField(max_length=31, default=False, null=False, blank=False, verbose_name="Hasta")
    cuenta = models.ForeignKey(Cuentas, verbose_name="Cuenta Contable")
    debito = models.DecimalField(max_digits=18, decimal_places=2, default=False, blank=False, null=False,
                                 verbose_name="Debito")
    credito = models.DecimalField(max_digits=18, decimal_places=2, default=False, blank=False, null=False,
                                  verbose_name="Credito")

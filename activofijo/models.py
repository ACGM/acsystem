from django.db import models
from administracion.models import Suplidor, Localidad
from cuenta.models import DiarioGeneral


# Definicion de tipos de activos
class CategoriaActivo(models.Model):
    descripcion = models.CharField(max_length=100, default=None, unique=True, null=False,
                                   verbose_name='Categoria de Activo')

    def __unicode__(self):
        return '%i - %s' % (self.id, self.descripcion)

    class Meta:
        ordering = ['descripcion']


class Depresiacion(models.Model):
    activoId = models.PositiveIntegerField(null=False, verbose_name='Id Activo')
    fecha = models.DateField(null=False, verbose_name='Fecha')
    dMensual = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Depresiacion Mensual')
    dAcumulada = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Depresiacion Acumulada')
    dAgno = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Depresiacion en el Agno')
    vLibro = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Valor en Libro')
    cuentas = models.ManyToManyField(DiarioGeneral, verbose_name='Cuentas', related_name='depre_rel', null=True,
                                     blank=True)

    def __unicode__(self):
        return '%i - %s' % (self.id, str(self.fecha))

    class Meta:
        ordering = ['fecha']


class Activos(models.Model):
    estatus_choices = (('A', 'En Uso'), ('D', 'Depresiado'))

    descripcion = models.CharField(max_length=100, default=None, null=False, verbose_name='Descripcion')
    categoria = models.ForeignKey(CategoriaActivo)
    # Fecha Adquisicion
    fechaAdd = models.DateField(null=False, verbose_name='Fecha Adquisicion')
    # Fecha Depresiacion
    fechaDep = models.DateField(null=False, verbose_name='Fecha Depresiacion')
    # Agnos de Vida Util
    agnosVu = models.PositiveIntegerField(null=False, verbose_name='Agnos vida Util')
    costo = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Costo de adquisicion')
    porcentaje = models.PositiveIntegerField(null=False, blank=False ,verbose_name="%. Dep Anual")
    suplidor = models.ForeignKey(Suplidor, null=True, blank=True, verbose_name='Suplidor')
    factura = models.PositiveIntegerField(null=False, verbose_name='Factura')
    localidad = models.ForeignKey(Localidad, verbose_name='Localidad')
    estatus = models.CharField(max_length=1, choices=estatus_choices, verbose_name="Estatus")

    # relaciones Many To Many a Depresiaciones y Diario General
    depresiacion = models.ManyToManyField(Depresiacion, verbose_name='Depresiaciones', related_name='ActivoDep_rel',
                                          null=True, blank=True)
    cuentas = models.ManyToManyField(DiarioGeneral, verbose_name='Cuentas', related_name='ActivoCuentas_rel', null=True,
                                     blank=True)

    def __unicode__(self):
        return '%i - %s' % (self.id, self.descripcion)

    class Meta:
        ordering = ['descripcion']

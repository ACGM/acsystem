from django.db import models

from cuenta.models import DiarioGeneral

from administracion.models import Socio, Suplidor

class SolicitudCheque(models.Model):
    estatus_choicer = (('A', 'Aprobada'), ('R', 'Rechazada'), ('P', 'En Proceso'),('E', 'Emitido'))

    fecha = models.DateTimeField()
    socio = models.ForeignKey(Socio, null=True, blank=True)
    suplidor = models.ForeignKey(Suplidor, null=True, blank=True)
    concepto = models.CharField(max_length=150, null=False, blank=False)
    monto = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Monto', blank=False, null=False)
    prestamo = models.PositiveIntegerField() 
    estatus = models.CharField(max_length=1, choices=estatus_choicer, verbose_name='Estatus')

    def __unicode__(self):
        return '%i - %s' % (self.id, str(self.fecha))


class ConcCheques(models.Model):
    estatus_choicer = (
    ('p', 'Posteado'), ('R', 'Registrado'), ('C', 'Cancelado'), ('D', 'Devueltos'), ('T', 'Transito'))

    solicitud = models.ForeignKey(SolicitudCheque)
    chequeNo = models.PositiveIntegerField(null=False, blank=False, verbose_name='# Cheque')
    fecha = models.DateTimeField()
    estatus = models.CharField(max_length=1, choices=estatus_choicer, verbose_name='Estatus')
    cuentas = models.ManyToManyField(DiarioGeneral, related_name='Chk_Cuentas', verbose_name='Cuentas', null=True, blank=True)

    def __unicode__(self):
        return '%i-%s' % (self.chequeNo, self.id)


class NotaDCConciliacion(models.Model):
    tipo_choicer = (('D', 'Debito'), ('C', 'Credito'))
    estatus_choicer = (('P', 'Posteada'), ('R', 'Registrado'), ('N', 'Nula'), ('T', 'Transito'))

    concepto = models.CharField(max_length=150, null=False, blank=False, verbose_name='Concepto')
    fecha = models.DateField()
    tipo = models.CharField(max_length=1, choices=tipo_choicer, verbose_name='Tipo Nota')
    monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False)
    estatus = models.CharField(max_length=1, choices=estatus_choicer, default='R')
    cuentas = models.ManyToManyField(DiarioGeneral, related_name='NConci_rel', verbose_name='Cuentas', null=True, blank=True)

    def __unicode__(self):
        return '%i-%s' % (self.id, self.concepto)


class ConBanco(models.Model):
    tipo_choicer = (('P', 'Deposito'), ('H', 'Cheques'), ('B', 'Balance Segun Banco'),('C', 'Credito'),('D', 'Debito'))
    estatus_choicer = (('R', 'Registrado'), ('T', 'Transito'), ('C','Cerrado'))

    fecha = models.DateField()
    descripcion = models.CharField(max_length=150, null=False, blank=False, verbose_name='Descripcion')
    tipo = models.CharField(max_length=1, choices=tipo_choicer, verbose_name='Tipo Registro')
    monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=True)
    estatus = models.CharField(max_length=1, choices=estatus_choicer, default='R')

    def __unicode__(self):
        return '%i-%s' % (self.id, str(self.fecha))

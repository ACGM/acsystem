from django.db import models

from cuenta.models import DiarioGeneral

from administracion.models import Socio, Suplidor

class SolicitudCheque(models.Model):
    estatus_choicer = (('A', 'Aprobada'), ('R', 'Rechazada'), ('P', 'En Proceso'),('E', 'Emitido'))

    fecha = models.DateField()
    socio = models.ForeignKey(Socio, null=True, blank=True)
    suplidor = models.ForeignKey(Suplidor, null=True, blank=True)
    concepto = models.CharField(max_length=150, null=False, blank=False)
    monto = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Monto', blank=False, null=False)
    prestamo = models.PositiveIntegerField(null=True, blank=True)
    cxpOrden = models.PositiveIntegerField(null=True, blank=True)
    superOrden = models.PositiveIntegerField(null=True, blank=True)
    estatus = models.CharField(max_length=1, choices=estatus_choicer, verbose_name='Estatus')
    cuentas = models.ManyToManyField(DiarioGeneral, related_name='Sol_Cuentas', verbose_name='Cuentas', null=True, blank=True)


    def __unicode__(self):
        return '%i - %s' % (self.id, str(self.fecha))


class NumCheque(models.Model):
    chequeNo = models.PositiveIntegerField(null=False, blank=False, verbose_name='# Cheque')
    banco = models.CharField(max_length="50")


class ConcCheques(models.Model):
    estatus_choicer = (
    ('p', 'Posteado'), ('R', 'Registrado'), ('C', 'Cancelado'), ('D', 'Devueltos'), ('T', 'Transito'))

    solicitud = models.ForeignKey(SolicitudCheque, null=True, blank=True)
    chequeNo = models.PositiveIntegerField(null=False, blank=False, verbose_name='# Cheque')
    fecha = models.DateField(null=False, blank=False)
    estatus = models.CharField(max_length=1, choices=estatus_choicer, verbose_name='Estatus')
    beneficiario = models.CharField(null=True, max_length=120, blank=True)
    concepto = models.CharField(max_length=150, null=True, blank=True)
    monto = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Monto', blank=True, null=True)
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
    # tipo_choicer = (('P', 'Deposito'), ('H', 'Cheques'), ('B', 'Balance Segun Banco'),('C', 'Credito'),('D', 'Debito'))
    estatus_choicer = (('R', 'Registrado'), ('T', 'Transito'), ('C','Cerrado'))

    fecha = models.DateField()
    descripcion = models.CharField(max_length=150, null=False, blank=False, verbose_name='Descripcion')
    # tipo = models.CharField(max_length=1, choices=tipo_choicer, verbose_name='Tipo Registro')
    monto = models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False, default=0)
    estatus = models.CharField(max_length=1, choices=estatus_choicer, default='R')
    cuentas = models.ManyToManyField(DiarioGeneral, related_name='CCBanco', verbose_name='Cuentas', null=True, blank=True)


    def __unicode__(self):
        return '%i-%s' % (self.id, str(self.fecha))


class ConDeposito(models.Model):
    estatus_choicer = (('R', 'Registrado'),('T', 'Transito'), ('C', 'Cerrado'))

    fecha = models .DateField()
    descripcion = models.CharField(max_length=150, null=False, blank=False, verbose_name='Descripcion')
    monto = models.DecimalField(max_digits=18, decimal_places=2, null= False, blank=False, default=0)
    estatus = models.CharField(max_length=1, choices=estatus_choicer, default='R')
    cuentas = models.ManyToManyField(DiarioGeneral, related_name='CCDepositos', null=True, blank=True, verbose_name="Depositos_Cuenta")

    def __unicode__(self):
        return '%i-%s' % (self.id, str(self.fecha))

class ConPeriodo(models.Model):

    fechaInicio = models.DateField()
    fechaFin    = models.DateField()
    cuenta = models.CharField(max_length=15, blank=False, null=False, verbose_name="cuenta") 
    monto = models.DecimalField(max_digits=18,decimal_places=2 , blank= False, null=False)

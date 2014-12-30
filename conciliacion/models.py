from django.db import models

from cuenta.models import DiarioGeneral

from administracion.models import Socio, CoBeneficiario

class SolicitudCheque(models.Model):
	fecha=models.DateTimeField()
	socio=models.ForeignKey(Socio)
	beneficiario=models.ForeignKey(CoBeneficiario)
	concepto=models.CharField(max_length=150, null=False, blank=False)
	monto=models.DecimalField(max_digits=18, decimal_places=2, verbose_name='Monto', blank=False, null=False)
	cuentas=models.ManyToManyField(DiarioGeneral, related_name='Solicitud_rel', verbose_name='Cuentas')

	def __unicode__(self):
		return '%i - %s' % self.id,str(self.fecha)

class ConcCheques(models.Model):
	estatus_choicer=(('p','Posteado'),('R','Registrado'),('C','Cancelado'),('D','Devueltos'))

	solicitud=models.ForeignKey(SolicitudCheque)
	chequeNo=models.PositiveIntegerField(null=False, blank=False, verbose_name='# Cheque')
	fecha=models.DateTimeField()
	estatus=models.CharField(max_length=1, choices=estatus_choicer, verbose_name='Estatus')

	def __unicode__(self):
		return '%i-%s' % self.chequeNo,self.id

class NotaDCConciliacion(models.Model):
	tipo_choicer=(('D','Debito'),('C','Credito'))
	estatus_choicer=(('P','Posteada'),('R','Registrado'),('N','Nula'))

	concepto=models.CharField(max_length=150, null=False, blank=False, verbose_name='Concepto')
	fecha=models.DateTimeField()
	tipo=models.CharField(max_length=1, choices=tipo_choicer, verbose_name='Tipo Nota')
	monto=models.DecimalField(max_digits=18, decimal_places=2, null=False, blank=False)
	estatus=models.CharField(max_length=1, choices=estatus_choicer, default='R')
	cuentas=models.ManyToManyField(DiarioGeneral, related_name='NConci_rel', verbose_name='Cuentas')

	def __unicode__(self):
		return '%i-%s' % self.id,self.tipo

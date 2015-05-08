# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from administracion.models import Socio, Representante, Cobrador, CategoriaPrestamo, Suplidor, Banco, Localidad
from facturacion.models import Factura

import datetime


# Cheques
class Cheque(models.Model):

	estatus_choices = (('A','Aprobado'),('R','Rechazado'),)

	chequeNo = models.IntegerField()
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')


# Solicitud de Prestamos
class SolicitudPrestamo(models.Model):

	estatus_choices = (('P','En Proceso'),('A','Aprobado'),('R','Rechazado'),('C','Cancelado'))

	noSolicitud = models.PositiveIntegerField(unique=True)
	fechaSolicitud = models.DateField(auto_now=True)

	socio = models.ForeignKey(Socio)
	salarioSocio = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	representante = models.ForeignKey(Representante)
	cobrador = models.ForeignKey(Cobrador)
	autorizadoPor = models.ForeignKey(User)
	aprobadoRechazadoPor = models.ForeignKey(User, related_name='+', null=True, blank=True)

	montoSolicitado = models.DecimalField(max_digits=12, decimal_places=2)
	ahorrosCapitalizados = models.DecimalField(max_digits=12, decimal_places=2, default=0) #Guardar los ahorros capitalizados al momento de realizar esta solicitud
	deudasPrestamos = models.DecimalField(max_digits=12, decimal_places=2, default=0) #Guardar las deudas de prestamos al momento de realizar esta solicitud
	prestacionesLaborales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	valorGarantizado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	netoDesembolsar = models.DecimalField(max_digits=12, decimal_places=2)
	
	garante = models.ForeignKey(Socio, related_name='+', null=True, blank=True)

	observacion = models.TextField(max_length=100)
	categoriaPrestamo = models.ForeignKey(CategoriaPrestamo)
	fechaParaDescuento = models.DateField()
	unificarPrestamos = models.BooleanField(default=False)
	tasaInteresAnual = models.DecimalField(max_digits=6, decimal_places=2)
	tasaInteresMensual = models.DecimalField(max_digits=6, decimal_places=2)
	cantidadCuotas = models.IntegerField()
	valorCuotasCapital = models.DecimalField(max_digits=12, decimal_places=2)
	fechaAprobacion = models.DateField(null=True, blank=True)
	fechaRechazo = models.DateField(null=True, blank=True)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')
	prestamo = models.PositiveIntegerField(null=True)
	localidad = models.ForeignKey(Localidad, null=True)

	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)

	@property
	def codigoSocio(self):
		return self.socio.codigo

	def __unicode__(self):
		return '%s' % (self.noSolicitud)


# Solicitud de Orden de Despacho Cabecera
class SolicitudOrdenDespachoH(models.Model):

	cxp_choices = (('E','EN PROCESO'),('P','PROCESADA'))
	estatus_choices = (('P','En Proceso'),('A','Aprobado'),('R','Rechazado'),('C','Cancelado'))

	noSolicitud = models.IntegerField(unique=True)
	fechaSolicitud = models.DateField(auto_now=True)

	socio = models.ForeignKey(Socio)
	salarioSocio = models.DecimalField(max_digits=12, decimal_places=2)
	representante = models.ForeignKey(Representante)
	cobrador = models.ForeignKey(Cobrador)
	autorizadoPor = models.ForeignKey(User)
	localidad = models.ForeignKey(Localidad)

	suplidor = models.ForeignKey(Suplidor)

	montoSolicitado = models.DecimalField(max_digits=12, decimal_places=2)
	ahorrosCapitalizados = models.DecimalField(max_digits=12, decimal_places=2, default=0) #Guardar los ahorros capitalizados al momento de realizar esta solicitud
	deudasPrestamos = models.DecimalField(max_digits=12, decimal_places=2, default=0) #Guardar las deudas de prestamos al momento de realizar esta solicitud
	prestacionesLaborales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	valorGarantizado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	netoDesembolsar = models.DecimalField(max_digits=12, decimal_places=2)
	observacion = models.TextField()
	categoriaPrestamo = models.ForeignKey(CategoriaPrestamo)
	fechaParaDescuento = models.DateField()
	tasaInteresAnual = models.DecimalField(max_digits=6, decimal_places=2)
	tasaInteresMensual = models.DecimalField(max_digits=6, decimal_places=2)
	cantidadCuotas = models.IntegerField()
	valorCuotasCapital = models.DecimalField(max_digits=12, decimal_places=2)
	fechaAprobacion = models.DateField(null=True, blank=True)
	fechaRechazo = models.DateField(null=True, blank=True)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')
	prestamo = models.PositiveIntegerField(null=True, blank=True)
	fechaVencimiento = models.DateField(null=True, blank=True)
	factura = models.PositiveIntegerField(null=True)
	cxp = models.CharField(max_length=1, choices=cxp_choices, default='E')
	impresa = models.PositiveIntegerField(default=0)
	
	
	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)

	@property
	def codigoSocio(self):
		return self.socio.codigo

	def __unicode__(self):
		return '%s' % (str(self.noSolicitud))

# Solicitud de Orden de Despacho Detalle
class SolicitudOrdenDespachoD(models.Model):

	ordenDespacho = models.ForeignKey(SolicitudOrdenDespachoH)
	articulo = models.CharField(max_length=80, default='No especificado')
	cantidad = models.DecimalField(max_digits=12, decimal_places=2)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	descuento = models.DecimalField(max_digits=8, decimal_places=2, default=0)

	class Meta:
		unique_together = ('id','ordenDespacho')


#Maestra de Prestamos
class MaestraPrestamo(models.Model):

	estatus_choices = (('E','En proceso'), ('P','Posteado'), ('S','Saldado'), ('C', 'Cheque'), ('D','Desembolso'))
	tipoPrestamoNomina_choices = (('RE','Regular'), ('BO','Bonificacion'), ('RG','Regalia'), ('VA','Vacaciones'), ('RI', 'Rifa'))

	noPrestamo = models.PositiveIntegerField(unique=True)
	noSolicitudPrestamo = models.ForeignKey(SolicitudPrestamo, null=True, blank=True)
	noSolicitudOD = models.ForeignKey(SolicitudOrdenDespachoH, null=True, blank=True)
	factura = models.ForeignKey(Factura, null=True, blank=True)

	categoriaPrestamo = models.ForeignKey(CategoriaPrestamo)
	socio = models.ForeignKey(Socio)
	representante = models.ForeignKey(Representante)
	oficial = models.ForeignKey(User)
	localidad = models.ForeignKey(Localidad)

	montoInicial = models.DecimalField(max_digits=12, decimal_places=2)
	tasaInteresAnual = models.DecimalField(max_digits=12, decimal_places=2)
	tasaInteresMensual = models.DecimalField(max_digits=12, decimal_places=2)
	pagoPrestamoAnterior = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	cantidadCuotas = models.PositiveIntegerField()
	montoCuotaQ1 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	montoCuotaQ2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	fechaDesembolso = models.DateField(null=True, blank=True)
	usuarioDesembolso = models.ForeignKey(User, related_name='+', null=True)
	fechaEntrega = models.DateField(null=True, blank=True)
	chequeNo = models.ForeignKey(Cheque, null=True, blank=True)
	valorGarantizado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	balance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, default=0)
	fechaAprobacion = models.DateField(auto_now_add=True, null=True)
	quincenas = models.PositiveIntegerField(default=2)
	tipoPrestamoNomina = models.CharField(max_length=2, choices=tipoPrestamoNomina_choices, default='RE') # Bonificacion, Vacaciones, Regalia, Rifa
	archivoBanco = models.CharField(max_length=25, null=True, blank=True)

	estatus = models.CharField(max_length=1, choices=estatus_choices, default='E')

	posteadoFecha = models.DateField(null=True)

	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '{0:0>9}'.format(self.noPrestamo)

	@property
	def codigoSocio(self):
		return self.socio.codigo

	@property
	def cuotaInteresQ1(self):
		if self.montoCuotaQ1 != None:
			valor = self.balance * (self.tasaInteresMensual/self.quincenas/100)
		else:
			valor = 0
		return valor

	@property
	def cuotaInteresQ2(self):
		if self.montoCuotaQ2 != None:
			valor = self.balance * (self.tasaInteresMensual/self.quincenas/100)
		else:
			valor = 0
		return valor

	@property
	def cuotaMasInteresQ1(self):
		if self.montoCuotaQ1 != None:
			valor = self.cuotaInteresQ1 + self.montoCuotaQ1
		else:
			valor = 0
		return valor

	@property
	def cuotaMasInteresQ2(self):
		if self.montoCuotaQ2 != None:
			valor = self.cuotaInteresQ2 + self.montoCuotaQ2
		else:
			valor = 0
		return valor

	def save(self, *args, **kwargs):
		if (self.montoCuotaQ1 == 0 or self.montoCuotaQ1 == None) or (self.montoCuotaQ2 == 0 or self.montoCuotaQ2 == None):
			self.quincenas = 1
		else:
			self.quincenas = 2

		super(MaestraPrestamo, self).save(*args, **kwargs)


# Prestamos Unificados
class PrestamoUnificado(models.Model):

	estatus_choices = (('P','En Proceso'),('A','Aprobado'),('R','Rechazado'))

	prestamoPrincipal = models.ForeignKey(SolicitudPrestamo, related_name='+')
	prestamoUnificado = models.ForeignKey(MaestraPrestamo, related_name='+')
	capitalUnificado = models.DecimalField(max_digits=12, decimal_places=2)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')


# Cuotas de Pago de Prestamos
class PagoCuotasPrestamo(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),('R','Rechazado'),('N','Nota de Credito'),('D','Nota de Debito'))

	noPrestamo = models.ForeignKey(MaestraPrestamo)
	valorCapital = models.DecimalField(max_digits=8, decimal_places=2)
	valorInteres = models.DecimalField(max_digits=8, decimal_places=2, null=True)
	fechaPago = models.DateField(auto_now_add=True)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')


# Nota de Credito a Prestamo
class NotaDeCreditoPrestamo(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),('R','Rechazado'),)

	fecha = models.DateField(auto_now=True)
	aplicadoACuota = models.ForeignKey(PagoCuotasPrestamo)
	noPrestamo = models.ForeignKey(MaestraPrestamo)
	valorCapital = models.DecimalField(max_digits=18, decimal_places=2)
	valorInteres = models.DecimalField(max_digits=18, decimal_places=2, null=True)
	concepto = models.TextField()

	posteado = models.BooleanField(default=False)
	fechaPosteo = models.DateField(auto_now=True, null=True)

	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)


# Nota de Credito Especial
class NotaDeCreditoEspecial(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),('R','Rechazado'),)

	fecha = models.DateField(auto_now=True)
	ordenDespacho = models.ForeignKey(SolicitudOrdenDespachoH)
	totalMontoOrden = models.DecimalField(max_digits=18, decimal_places=2)
	montoConsumido = models.DecimalField(max_digits=18, decimal_places=2)
	nota = models.TextField()
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')
	
	posteado = models.BooleanField(default=False)
	fechaPosteo = models.DateField(auto_now=True, null=True)

	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)


# Nota de Debito a Prestamo
class NotaDeDebitoPrestamo(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),('R','Rechazado'),)
	posteo_choices = (('N','NO'),('S','SI'))

	fecha = models.DateField(auto_now=True)
	noPrestamo = models.ForeignKey(MaestraPrestamo)
	valorCapital = models.DecimalField(max_digits=12, decimal_places=2)
	valorInteres = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	concepto = models.TextField()
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')

	posteado = models.CharField(max_length=1, choices=posteo_choices, default='N')
	fechaPosteo = models.DateField(auto_now=True, null=True)

	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)


# Distribuccion de Excedentes -- Este proceso se corre una vez al agno
# Consiste en repartir un % de los interes retenidos por la cooperativa entre los socios, depositandolo directamente en los ahorros.
class DistribucionExcedente(models.Model):

	agno = models.CharField(max_length=4)
	fecha = models.DateField(auto_now_add=True)
	porcentaje = models.DecimalField(max_digits=6, decimal_places=2)
	noPrestamo = models.ForeignKey(MaestraPrestamo)
	fechaPosteo = models.DateField(auto_now=True, null=True)

	userLog = models.ForeignKey(User, editable=False)
	datetimeServer = models.DateTimeField(auto_now_add=True)

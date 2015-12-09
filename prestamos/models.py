# Model Prestamos

# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# from nominacoop.models import CuotasPrestamosEmpresa
from administracion.models import Socio, Representante, Cobrador, CategoriaPrestamo, Suplidor, Banco, Localidad
from facturacion.models import Factura

from datetime import timedelta

import datetime
import decimal


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
	interesBaseAhorroMensual = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
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

	@property
	def codigoCategoria(self):
		return '{0:0>4}'.format(self.categoriaPrestamo.id)

	@property
	def codigoRepresentante(self):
		return '{0:0>4}'.format(self.representante.id)

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

	@property
	def codigoSuplidor(self):
		return self.suplidor.id

	@property
	def direccionSuplidor(self):
		return self.suplidor.direccion

	@property
	def valorInteresOD(self):
		return self.netoDesembolsar * (self.tasaInteresAnual/100)

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
	tasaInteresPrestBaseAhorro = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	pagoPrestamoAnterior = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	cantidadCuotas = models.PositiveIntegerField()
	montoCuotaQ1 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	montoCuotaQ2 = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	fechaDesembolso = models.DateField(null=True, blank=True)
	usuarioDesembolso = models.ForeignKey(User, related_name='+', null=True)
	fechaEntrega = models.DateField(null=True, blank=True)
	chequeNo = models.PositiveIntegerField(null=True, blank=True)
	valorGarantizado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	valorAhorro = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	balance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, default=0)
	fechaAprobacion = models.DateField(auto_now_add=True, null=True)
	quincenas = models.PositiveIntegerField(default=2)
	tipoPrestamoNomina = models.CharField(max_length=2, choices=tipoPrestamoNomina_choices, default='RE') # Bonificacion, Vacaciones, Regalia, Rifa
	archivoBanco = models.CharField(max_length=25, null=True, blank=True)

	estatus = models.CharField(max_length=1, choices=estatus_choices, default='E')

	posteadoFecha = models.DateField(null=True)
	posteoUsr = models.ForeignKey(User, related_name='+', null=True, blank=True)

	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '{0:0>9}'.format(self.noPrestamo)


	@property
	def tieneAUnificar(self):
		tiene = 'N' #N = No, S = Si

		try:
			aUnificar = PrestamoUnificado.objects.filter(prestamoUnificado=self.noPrestamo)
			tiene = 'S'
		except:
			tiene = 'N'

		return tiene

	@property
	def documentoDescrp(self):
		return 'Orden de Despacho' if self.noSolicitudOD != None else 'Prestamo'

	@property
	def codigoSocio(self):
		return self.socio.codigo

	@property
	def tipoSocio(self):
		return self.socio.estatus

	@property
	def departamentoSocio(self):
		return self.socio.departamento.descripcion

	@property
	def centrocostoSocio(self):
		return self.socio.departamento.centroCosto

	@property
	def fechaVencimiento(self):
		dias = self.cantidadCuotas * 15
		f = self.fechaAprobacion + timedelta(days=dias)

		return f

	@property
	def getDescrpCatPrestamo(self):
		return self.categoriaPrestamo.descripcion
	
	@property
	def getCodigoSuplidor(self):
		codigo = 0
		if self.noSolicitudOD != None:
			codigo = self.noSolicitudOD.suplidor.id

		return codigo

	@property
	def getRNCSuplidor(self):
		rnc = ''
		if self.noSolicitudOD != None:
			rnc = self.noSolicitudOD.suplidor.cedulaRNC

		return rnc

	@property
	def getNombreSuplidor(self):
		nombre = ''
		if self.noSolicitudOD != None:
			nombre = self.noSolicitudOD.suplidor.nombre

		return nombre

	@property
	def getMontoSinInteres(self):
		montoOD = 0
		if self.noSolicitudOD != None:
			montoOD = self.noSolicitudOD.montoSolicitado

		return montoOD

	@property
	def getMontoInteres(self):
		montoInteresOD = 0
		if self.noSolicitudOD != None:
			montoInteresOD = self.montoInicial - self.noSolicitudOD.montoSolicitado

		return montoInteresOD

	@property
	def cuotaInteresQ1(self):
		if self.montoCuotaQ1 > 0:
			interesGarant = self.tasaInteresMensual/self.quincenas/100
			InteresGarantizado = self.valorGarantizado * (interesGarant) if self.valorGarantizado != None else 0
		else:
			InteresGarantizado = 0
		return InteresGarantizado

	@property
	def cuotaInteresQ2(self):
		if self.montoCuotaQ2 != None:
			interesGarant = self.tasaInteresMensual/self.quincenas/100
			InteresGarantizado = self.valorGarantizado * (interesGarant) if self.valorGarantizado != None else 0
		else:
			InteresGarantizado = 0
		return InteresGarantizado

	@property
	def cuotaInteresAhQ1(self):
		if self.montoCuotaQ1 > 0:
			intPrestBaseAhorroMens = InteresPrestamosBaseAhorros.objects.get(estatus='A').porcentajeAnual/12
			interesAhorro = decimal.Decimal(intPrestBaseAhorroMens/self.quincenas/100)
			InteresAhorroC = decimal.Decimal(self.valorAhorro * (interesAhorro)) if self.valorAhorro != None else 0
		else:
			InteresAhorroC = 0
		return InteresAhorroC

	@property
	def cuotaInteresAhQ2(self):
		if self.montoCuotaQ2 != None:
			intPrestBaseAhorroMens = InteresPrestamosBaseAhorros.objects.get(estatus='A').porcentajeAnual/12
			interesAhorro = decimal.Decimal(intPrestBaseAhorroMens/self.quincenas/100) 
			InteresAhorroC = decimal.Decimal(self.valorAhorro * (interesAhorro)) if self.valorAhorro != None else 0
		else:
			InteresAhorroC = 0
		return InteresAhorroC

	@property
	def cuotaMasInteresQ1(self):
		if self.montoCuotaQ1 != None:
			valor = self.cuotaInteresQ1 + self.cuotaInteresAhQ1 + self.montoCuotaQ1
		else:
			valor = 0
		return valor

	@property
	def cuotaMasInteresQ2(self):
		if self.montoCuotaQ2 != None:
			valor = self.cuotaInteresQ2 + self.cuotaInteresAhQ2 + self.montoCuotaQ2
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

	solicitudPrestamo = models.ForeignKey(SolicitudPrestamo, related_name='+')
	prestamoUnificado = models.ForeignKey(MaestraPrestamo, related_name='+')
	capitalUnificado = models.DecimalField(max_digits=12, decimal_places=2)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')


# Cuotas de Pago de Prestamos
class PagoCuotasPrestamo(models.Model):

	# estatus_choices = (('P','Pendiente'),('A','Aprobado'),('R','Rechazado'),)
	tipo_pago_choices = (('NC','Nota de Credito'),('ND','Nota de Debito'), ('NM', 'Nomina'), ('RI', 'Recibo Ingreso'), ('AH', 'Ahorros'))

	noPrestamo = models.ForeignKey(MaestraPrestamo)
	valorCapital = models.DecimalField(max_digits=8, decimal_places=2)
	valorInteres = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	valorInteresAh = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	fechaPago = models.DateField(auto_now_add=True)
	docRef = models.CharField(max_length=15, null=True, blank=True)
	tipoPago = models.CharField(max_length=2, choices=tipo_pago_choices, default='N')
	# estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')

	def __unicode__(self):
		return '%i' % self.id

# Nota de Credito a Prestamo
class NotaDeCreditoPrestamo(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),('R','Rechazado'),)
	posteo_choices = (('N','NO'),('S','SI'))

	fecha = models.DateField(auto_now=True)
	aplicadoACuota = models.ForeignKey(PagoCuotasPrestamo)
	noPrestamo = models.ForeignKey(MaestraPrestamo)
	valorCapital = models.DecimalField(max_digits=12, decimal_places=2)
	valorInteres = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	valorInteresAh = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	concepto = models.TextField()
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')

	posteado = models.CharField(max_length=1, choices=posteo_choices, default='N')
	posteadoUsr = models.ForeignKey(User, null=True, blank=True, related_name='+')
	fechaPosteo = models.DateField(auto_now=True, null=True)

	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%i' % self.id

	@property
	def getSocio(self):
		return self.noPrestamo.socio.nombreCompleto


# Nota de Credito Especial
class NotaDeCreditoEspecial(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),('R','Rechazado'),)
	posteo_choices = (('N','NO'),('S','SI'))

	fecha = models.DateField(auto_now=True)
	ordenDespacho = models.ForeignKey(SolicitudOrdenDespachoH)
	totalMontoOrden = models.DecimalField(max_digits=12, decimal_places=2)
	montoConsumido = models.DecimalField(max_digits=12, decimal_places=2)
	nota = models.TextField()
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')
	
	posteado = models.CharField(max_length=1, choices=posteo_choices, default='N')
	fechaPosteo = models.DateField(auto_now=True, null=True)

	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)

	@property
	def getSocio(self):
		return self.ordenDespacho.socio.nombreCompleto

	@property
	def getMontoAhorro(self):
		return 0

	class Meta:
		verbose_name = "Nota de Credito Especial"
		verbose_name_plural = "Notas de Credito Especiales"

# Nota de Debito a Prestamo
class NotaDeDebitoPrestamo(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),('R','Rechazado'),)
	posteo_choices = (('N','NO'),('S','SI'))

	fecha = models.DateField(auto_now=True)
	noPrestamo = models.ForeignKey(MaestraPrestamo)
	valorCapital = models.DecimalField(max_digits=12, decimal_places=2)
	valorInteres = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	valorInteresAh = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	concepto = models.TextField()
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')

	posteoUsr = models.ForeignKey(User, null=True, blank=True, related_name='+')
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


#Tabla para guardar el porcentaje de interes sobre beneficio de ahorro para prestamos
class InteresPrestamosBaseAhorros(models.Model):
    estatus_choices = (('A', 'Activo'), ('I', 'Inactivo'))

    porcentajeAnual = models.DecimalField("Porcentaje Anual", max_digits=4, decimal_places=2)
    estatus = models.CharField(max_length=6, choices=estatus_choices, default='A')

    def __unicode__(self):
    	return '%s' % self.porcentajeAnual

    class Meta:
    	verbose_name = 'Interes en Base Ahorro'
    	verbose_name_plural = 'Interes en Base Ahorro'

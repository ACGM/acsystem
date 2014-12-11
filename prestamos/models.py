# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from administracion.models import Socio, Representante, Cobrador, CategoriaPrestamo, Suplidor, Distrito, Banco
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
	descontar_choices = (('Q','Quincenal'),('M','Mensual'))
	quincena_choices = (('1','1ra. Quincena'),('2','2da. Quincena'))

	noSolicitud = models.IntegerField(unique=True)
	fechaSolicitud = models.DateField(auto_now=True)

	socio = models.ForeignKey(Socio)
	salarioSocio = models.DecimalField(max_digits=12, decimal_places=2)
	representante = models.ForeignKey(Representante)
	cobrador = models.ForeignKey(Cobrador)
	autorizadoPor = models.ForeignKey(User)

	montoSolicitado = models.DecimalField(max_digits=12, decimal_places=2)
	valorGarantizado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	netoDesembolsar = models.DecimalField(max_digits=12, decimal_places=2)
	observacion = models.TextField()
	categoriaPrestamo = models.ForeignKey(CategoriaPrestamo)
	fechaParaDescuento = models.DateField()
	unificarPrestamos = models.BooleanField(default=False)
	descontar = models.CharField(max_length=1, choices=descontar_choices, default='Q')
	quincena = models.IntegerField(choices=quincena_choices, default=1, null=True, blank=True)
	tasaInteresAnual = models.DecimalField(max_digits=6, decimal_places=2)
	tasaInteresMensual = models.DecimalField(max_digits=6, decimal_places=2)
	cantidadCuotas = models.IntegerField()
	valorCuotasCapital = models.DecimalField(max_digits=12, decimal_places=2)
	fechaAprobacion = models.DateField(null=True, blank=True)
	fechaRechazo = models.DateField(null=True, blank=True)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')

	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)


# Solicitud de Orden de Despacho Cabecera
class SolicitudOrdenDespachoH(models.Model):

	estatus_choices = (('P','En Proceso'),('A','Aprobado'),('R','Rechazado'),('C','Cancelado'))
	descontar_choices = (('Q','Quincenal'),('M','Mensual'))
	quincena_choices = (('1','1ra. Quincena'),('2','2da. Quincena'))

	noSolicitud = models.IntegerField(unique=True)
	fechaSolicitud = models.DateField(auto_now=True)

	socio = models.ForeignKey(Socio)
	salarioSocio = models.DecimalField(max_digits=12, decimal_places=2)
	representante = models.ForeignKey(Representante)
	cobrador = models.ForeignKey(Cobrador)
	autorizadoPor = models.ForeignKey(User)

	suplidor = models.ForeignKey(Suplidor)
	montoSolicitado = models.DecimalField(max_digits=12, decimal_places=2)
	valorGarantizdo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	netoDesembolsar = models.DecimalField(max_digits=12, decimal_places=2)
	observacion = models.TextField()
	categoriaPrestamo = models.ForeignKey(CategoriaPrestamo)
	fechaParaDescuento = models.DateField()
	unificarPrestamos = models.BooleanField(default=False)
	descontar = models.CharField(max_length=1, choices=descontar_choices, default='Q')
	quincena = models.IntegerField(choices=quincena_choices, default=1, null=True, blank=True)
	tasaInteresAnual = models.DecimalField(max_digits=6, decimal_places=2)
	tasaInteresMensual = models.DecimalField(max_digits=6, decimal_places=2)
	cantidadCuotas = models.IntegerField()
	valorCuotasCapital = models.DecimalField(max_digits=12, decimal_places=2)
	fechaAprobacion = models.DateField(null=True, blank=True)
	fechaRechazo = models.DateField(null=True, blank=True)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')
	
	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)


# Solicitud de Orden de Despacho Detalle
class SolicitudOrdenDespachoD(models.Model):

	ordenDespacho = models.ForeignKey(SolicitudOrdenDespachoH)
	#FALTA COMPLETAR AQUI -- VER DETALLE EN EL SISTEMA ACTUAL



#Maestra de Prestamos
class MaestraPrestamo(models.Model):

	tipoPago_choices = (('Q','Quincenal'),('M','Mensual'))
	quincena_choices = (('1','1ra. Quincena'),('2','2da. Quincena'))

	noPrestamo = models.PositiveIntegerField(unique=True)
	noSolicitudPrestamo = models.ForeignKey(SolicitudPrestamo, null=True, blank=True)
	noSolicitudOD = models.ForeignKey(SolicitudOrdenDespachoH, null=True, blank=True)
	factura = models.ForeignKey(Factura, null=True)

	categoriaPrestamo = models.ForeignKey(CategoriaPrestamo)
	socio = models.ForeignKey(Socio)
	representante = models.ForeignKey(Representante)
	oficial = models.ForeignKey(User)
	distrito = models.ForeignKey(Distrito)

	montoInicial = models.DecimalField(max_digits=12, decimal_places=2)
	tasaInteresAnual = models.DecimalField(max_digits=12, decimal_places=2)
	tasaInteresMensual = models.DecimalField(max_digits=12, decimal_places=2)
	pagoPrestamoAnterior = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	cantidadCuotas = models.PositiveIntegerField()
	montoCuotas = models.DecimalField(max_digits=12, decimal_places=2)
	fechaDesembolso = models.DateField()
	fechaEntrega = models.DateField()
	chequeNo = models.ForeignKey(Cheque)
	tipoPago = models.CharField(max_length=1, choices=tipoPago_choices, default='Q')
	quincena = models.PositiveIntegerField(choices=quincena_choices, default=1)	
	valorGarantizado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	balance = models.DecimalField(max_digits=12, decimal_places=2, blank=True)

	posteado = models.BooleanField(default=False)
	posteadoFecha = models.DateField(auto_now=True, null=True, blank=True)

	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)


# Prestamos Unificados
class PrestamoUnificado(models.Model):

	estatus_choices = (('P','En Proceso'),('A','Aprobado'),('R','Rechazado'))

	prestamoPrincipal = models.ForeignKey(SolicitudPrestamo, related_name='+')
	prestamoUnificado = models.ForeignKey(MaestraPrestamo, related_name='+')
	capitalUnificado = models.DecimalField(max_digits=12, decimal_places=2)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')


# Cuotas de Pago de Prestamos
class CuotasPrestamo(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),('R','Rechazado'),('N','Nota de Credito'),)

	noPrestamo = models.ForeignKey(MaestraPrestamo)
	valorCapital = models.DecimalField(max_digits=12, decimal_places=2)
	valorInteres = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	fechaPago = models.DateField(auto_now_add=True)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')


# Nota de Credito a Prestamo
class NotaDeCreditoPrestamo(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),('R','Rechazado'),)

	fecha = models.DateField(auto_now=True)
	aplicadoACuota = models.ForeignKey(CuotasPrestamo)
	noPrestamo = models.ForeignKey(MaestraPrestamo)
	valorCapital = models.DecimalField(max_digits=12, decimal_places=2)
	valorInteres = models.DecimalField(max_digits=12, decimal_places=2, null=True)
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
	totalMontoOrden = models.DecimalField(max_digits=12, decimal_places=2)
	montoConsumido = models.DecimalField(max_digits=12, decimal_places=2)
	nota = models.TextField()
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')
	
	posteado = models.BooleanField(default=False)
	fechaPosteo = models.DateField(auto_now=True, null=True)

	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)


# Nota de Debito a Prestamo
class NotaDeDebitoPrestamo(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),('R','Rechazado'),)

	fecha = models.DateField(auto_now=True)
	noPrestamo = models.ForeignKey(MaestraPrestamo)
	valorCapital = models.DecimalField(max_digits=12, decimal_places=2)
	valorInteres = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	concepto = models.TextField()
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')

	posteado = models.BooleanField(default=False)
	fechaPosteo = models.DateField(auto_now=True, null=True)

	userLog = models.ForeignKey(User, related_name='+')
	datetimeServer = models.DateTimeField(auto_now_add=True)


# Desembolsos Electronicos
class DesembolsoElectronico(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),('R','Rechazado'),)

	fecha = models.DateField(auto_now_add=True)
	noPrestamo = models.ForeignKey(MaestraPrestamo)
	monto = models.DecimalField(max_digits=12, decimal_places=2)
	banco = models.ForeignKey(Banco)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')

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

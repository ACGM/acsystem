# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from administracion.models import Empresa, CoBeneficiario, Socio
from prestamos.models import MaestraPrestamo, CuotasPrestamo


class DepartamentoCoop(models.Model):

	descripcion = models.CharField(max_length=150)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Cargos en la cooperativa para empleados
class CargoCoop(models.Model):

	descripcion = models.CharField(max_length=100)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Empleado Cooperativa
class EmpleadoCoop(models.Model):

	estado_civil_choices = (('S','Soltero(a)'),('C','Casado(a)'),('U','Union Libre'),)
	sexo_choices = (('M','Masculino'),('F','Femenino'),)
	tipo_empleado_choices = (('F','Fijo'),('T','Temporal'),)
	tipo_cobro_choices = (('Q','Quincenal'),('M','Mensual'),)
	tipo_pago_choices = (('E','Efectivo'),('C','Cheque'),('B','Banco'),)

	codigo = models.CharField(max_length=5)
	nombres = models.CharField(max_length=80)
	apellidos = models.CharField(max_length=100)
	cedula = models.CharField(max_length=20)
	direccion = models.TextField(null=True, blank=True)
	sector = models.CharField(max_length=100, null=True, blank=True)
	ciudad = models.CharField(max_length=80, null=True, blank=True)
	telefono = models.CharField(max_length=50, null=True, blank=True)
	fechaNac = models.DateField("Fecha de Nacimiento", null=True, blank=True)
	lugarNac = models.CharField("Lugar de Nacimiento", max_length=100, null=True, blank=True)
	estadoCivil = models.CharField("Estado Civil", max_length=1, choices=estado_civil_choices, default='S')
	sexo = models.CharField(max_length=1, choices=sexo_choices, default='M')
	dependencias = models.PositiveIntegerField(null=True, blank=True)
	fechaIngreso = models.DateField("Fecha de Ingreso", auto_now=True)
	empresa = models.ForeignKey(Empresa)
	departamento = models.ForeignKey(DepartamentoCoop)
	tipoContrato = models.CharField("Tipo de Contrato", max_length=1, choices=tipo_empleado_choices, default='F')
	cargo = models.ForeignKey(CargoCoop)
	tipoCobro = models.CharField("Tipo de Cobro", max_length=1, choices=tipo_empleado_choices, default='Q')
	tipoPago = models.CharField("Tipo de Pago", max_length=1, choices=tipo_pago_choices, default='B')
	sueldoActual = models.DecimalField("Sueldo Actual", max_digits=12, decimal_places=2)
	sueldoAnterior = models.DecimalField("Sueldo Anterior", max_digits=12, decimal_places=2, blank=True)
	activo = models.BooleanField(default=True)
	fechaSalida = models.DateField("Fecha de Salida", null=True, blank=True)


# Tipos de nominas
class TipoNomina(models.Model):

	descripcion = models.CharField(max_length=50)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Cabecera Nomina de Cooperativa
class NominaCoopH(models.Model):

	tipo_pago_choices = (('E','Efectivo'),('C','Cheque'),('B','Banco'),)
	estatus_choices = (('P','Procesada'),('E','En proceso'),)

	fechaNomina = models.DateField(auto_now=True)
	fechaPago = models.DateField(auto_now=True)
	empleados = models.IntegerField()
	valorNomina = models.DecimalField(max_digits=12, decimal_places=2)
	tipoNomina = models.ForeignKey(TipoNomina)
	tipoPago = models.CharField(max_length=1, choices=tipo_pago_choices, default='B')
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='E')
	nota = models.TextField(blank=True)

	posteada = models.BooleanField(default=False)
	fechaPosteo = models.DateField(auto_now=True, null=True)

	user_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)


# Detalle Nomina de Cooperativa
class NominaCoopD(models.Model):

	tipo_pago_choices = (('E','Efectivo'),('C','Cheque'),('B','Banco'),)
	estatus_choices = (('P','Procesada'),('E','En proceso'),)

	fecha = models.DateField(auto_now_add=True)
	fechaNomina = models.DateField(auto_now=True)
	userLog = models.ForeignKey(User)
	empleado = models.ForeignKey(EmpleadoCoop)
	salario = models.DecimalField(max_digits=12, decimal_places=2)
	isr = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	afp = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	ars = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	cafeteria = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	vacaciones = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	otrosIngresos = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	descAhorros = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) #Este actualizado a traves del proceso especial
	descPrestamos = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) #Este actualizado a traves del proceso especial
	tipoPago = models.CharField(max_length=1, choices=tipo_pago_choices, default='B')
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='E')


# Cuotas Prestamos para Nomina Empresa
class CuotasPrestamosEmpresa(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),)

	socio = models.ForeignKey(Socio)
	noPrestamo = models.ForeignKey(MaestraPrestamo)
	cuota = models.ForeignKey(CuotasPrestamo)
	valorCapital = models.DecimalField(max_digits=12, decimal_places=2)
	valorInteres = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	fecha = models.DateField(auto_now=True, null=True)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')


# Cuotas Ahorros para Nomina Empresa
class CuotasAhorrosEmpresa(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),)

	socio = models.ForeignKey(Socio)
	noPrestamo = models.ForeignKey(MaestraPrestamo)
	cuota = models.ForeignKey(CuotasPrestamo)
	valorAhorro = models.DecimalField(max_digits=12, decimal_places=2)
	fecha = models.DateField(auto_now=True, null=True)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')

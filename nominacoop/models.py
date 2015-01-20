# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

from administracion.models import Empresa, CoBeneficiario, Socio
from prestamos.models import MaestraPrestamo, CuotasPrestamo


class DepartamentoCoop(models.Model):

	descripcion = models.CharField(max_length=40)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'Departamento Cooperativa'
		verbose_name_plural = 'Departamentos Cooperativa'


# Cargos en la cooperativa para empleados
class CargoCoop(models.Model):

	descripcion = models.CharField(max_length=40)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'Cargo Cooperativa'
		verbose_name_plural = 'Cargos Cooperativa'


# Empleado Cooperativa
class EmpleadoCoop(models.Model):

	estado_civil_choices = (('S','Soltero(a)'),('C','Casado(a)'),('U','Union Libre'),)
	sexo_choices = (('M','Masculino'),('F','Femenino'),)
	tipo_empleado_choices = (('F','Fijo'),('T','Temporal'),)
	tipo_cobro_choices = (('Q','Quincenal'),('M','Mensual'),)
	tipo_pago_choices = (('E','Efectivo'),('C','Cheque'),('B','Banco'),)

	codigo = models.PositiveIntegerField(max_length=6)
	nombres = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=50)
	cedula = models.CharField(max_length=20)
	direccion = models.TextField(null=True, blank=True)
	sector = models.CharField(max_length=50, null=True, blank=True)
	ciudad = models.CharField(max_length=40, null=True, blank=True)
	telefono = models.CharField(max_length=40, null=True, blank=True)
	fechaNac = models.DateField("Fecha de Nacimiento", null=True, blank=True)
	lugarNac = models.CharField("Lugar de Nacimiento", max_length=50, null=True, blank=True)
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
	sueldoActual = models.DecimalField("Sueldo Actual", max_digits=18, decimal_places=2)
	sueldoAnterior = models.DecimalField("Sueldo Anterior", max_digits=18, decimal_places=2, blank=True)
	activo = models.BooleanField(default=True)
	fechaSalida = models.DateField("Fecha de Salida", null=True, blank=True)

	def __unicode__(self):
		return '%s %s' % (self.nombres, self.apellidos)

	class Meta:
		verbose_name = 'Empleado Cooperativa'
		verbose_name_plural = 'Empleados Cooperativa'
		ordering = ['codigo',]


# Tipos de nominas
class TipoNomina(models.Model):

	descripcion = models.CharField(max_length=20)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['id']
		verbose_name = 'Tipo de Nomina'
		verbose_name_plural = 'Tipos de Nominas'


# Cabecera Nomina de Cooperativa
class NominaCoopH(models.Model):

	tipo_pago_choices = (('E','Efectivo'),('C','Cheque'),('B','Banco'),)
	estatus_choices = (('P','Procesada'),('E','En proceso'),)
	quincena_choices = ((1,'1ra. Quincena'),(2,'2da. Quincena'),)

	fechaNomina = models.DateField()
	fechaPago = models.DateField(null=True)
	tipoNomina = models.ForeignKey(TipoNomina)
	tipoPago = models.CharField(max_length=1, choices=tipo_pago_choices, default='B')
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='E')
	quincena = models.PositiveIntegerField(choices=quincena_choices, default=1)
	nota = models.TextField(blank=True)

	posteada = models.CharField(max_length=1, default='N')
	fechaPosteo = models.DateField(auto_now=True, null=True)

	userLog = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.fechaNomina)

	@property
	def cntEmpleados(self):
		try:
			cnt = NominaCoopD.objects.filter(nomina=self.id).count()
			cnt = cnt if cnt != None else 0
		except NominaCoopD.DoesNotExist:
			cnt = 0

		return '%i' % cnt
	
	@property
	def valorNomina(self):
		valor = 0

		try:
			empleados = NominaCoopD.objects.filter(nomina=self.id)
			
			for empleado in empleados:
				valor += empleado.salario - (empleado.isr + empleado.afp + empleado.ars + \
						empleado.cafeteria + empleado.descAhorros + empleado.descPrestamos) \
						+ empleado.otrosIngresos + empleado.vacaciones
		except NominaCoopD.DoesNotExist:
			valor = 0

		return valor

	@property
	def sueldoMensual(self):
		try:
			totalSueldo = NominaCoopD.objects.values('salario').filter(nomina=self.id).annotate(total=Sum('salario'))[0]['total']
		except NominaCoopD.DoesNotExist:
			totalSueldo = 0

		return totalSueldo


	class Meta:
		ordering = ['-id']
		verbose_name = 'Nomina Cabecera'
		verbose_name_plural = 'Nominas Cabecera'
		unique_together = ('fechaNomina', 'tipoNomina')


# Detalle Nomina de Cooperativa
class NominaCoopD(models.Model):

	tipo_pago_choices = (('E','Efectivo'),('C','Cheque'),('B','Banco'),)
	estatus_choices = (('P','Procesada'),('E','En proceso'),)

	nomina = models.ForeignKey(NominaCoopH)
	empleado = models.ForeignKey(EmpleadoCoop)
	salario = models.DecimalField(max_digits=18, decimal_places=2)
	isr = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, default=0)
	afp = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, default=0)
	ars = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, default=0)
	cafeteria = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, default=0)
	vacaciones = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, default=0)
	otrosIngresos = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, default=0)
	descAhorros = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, default=0) #Este actualizado a traves del proceso especial
	descPrestamos = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True, default=0) #Este actualizado a traves del proceso especial
	tipoPago = models.CharField(max_length=1, choices=tipo_pago_choices, default='B')
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='E')

	def __unicode__(self):
		return '%s' % (self.nomina.fechaNomina)

	@property
	def getcodigo(self):
		return '%s' % (self.empleado.codigo)

	class Meta:
		unique_together = ('nomina', 'empleado')
		verbose_name = 'Nomina Detalles'
		verbose_name_plural = 'Nominas Detalles'


# Cuotas Prestamos para Nomina Empresa
class CuotasPrestamosEmpresa(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),)

	socio = models.ForeignKey(Socio)
	noPrestamo = models.ForeignKey(MaestraPrestamo)
	cuota = models.ForeignKey(CuotasPrestamo)
	valorCapital = models.DecimalField(max_digits=12, decimal_places=2)
	valorInteres = models.DecimalField(max_digits=12, decimal_places=2, null=True)
	nomina = models.DateField(null=True)
	fecha = models.DateField(auto_now=True, null=True)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')


# Cuotas Ahorros para Nomina Empresa
class CuotasAhorrosEmpresa(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),)

	socio = models.ForeignKey(Socio)
	valorAhorro = models.DecimalField(max_digits=12, decimal_places=2)
	fecha = models.DateField(auto_now=True, null=True)
	nomina = models.DateField(null=True)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')

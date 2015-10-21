# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

from administracion.models import Empresa, CoBeneficiario, Socio
from prestamos.models import MaestraPrestamo, PagoCuotasPrestamo


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

	#codigo = models.PositiveIntegerField(max_length=6)
	socio = models.ForeignKey(Socio)
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
	sueldoAnterior = models.DecimalField("Sueldo Anterior", max_digits=18, decimal_places=2, blank=True, null=True)
	activo = models.BooleanField(default=True)
	fechaSalida = models.DateField("Fecha de Salida", null=True, blank=True)

	def __unicode__(self):
		return '%s %s' % (self.nombres, self.apellidos)

	def codigoSocio(self):
		return '%s' % (self.socio.codigo)

	class Meta:
		verbose_name = 'Empleado Cooperativa'
		verbose_name_plural = 'Empleados Cooperativa'
		ordering = ['socio',]


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
	archivoBanco = models.CharField(max_length=25, null=True, blank=True)

	posteada = models.CharField(max_length=1, default='N') # N = No, S = Si
	fechaPosteo = models.DateField(null=True, blank=True)
	posteoUsr = models.ForeignKey(User, null=True, blank=True, related_name='+')

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
				salario = empleado.salario
				descuentos = empleado.isr + empleado.afp + empleado.ars + empleado.cafeteria + empleado.descAhorros + empleado.descPrestamos
				ingresos = empleado.otrosIngresos + empleado.vacaciones

				valor += (salario + ingresos - descuentos)

		except NominaCoopD.DoesNotExist:
			valor = 0

		return valor

	@property
	def sueldoMensual(self):
		try:
			totalSueldo = NominaCoopD.objects.values('salario').filter(nomina=self.id).aggregate(total=Sum('salario'))['total']
		except NominaCoopD.DoesNotExist:
			totalSueldo = 0
		return totalSueldo

	@property
	def ISR(self):
		try:
			totalISR = NominaCoopD.objects.values('isr').filter(nomina=self.id).aggregate(total=Sum('isr'))['total']
		except NominaCoopD.DoesNotExist:
			totalISR = 0
		return totalISR

	@property
	def AFP(self):
		try:
			totalAFP = NominaCoopD.objects.values('afp').filter(nomina=self.id).aggregate(total=Sum('afp'))['total']
		except NominaCoopD.DoesNotExist:
			totalAFP = 0
		return totalAFP

	@property
	def ARS(self):
		try:
			totalARS = NominaCoopD.objects.values('ars').filter(nomina=self.id).aggregate(total=Sum('ars'))['total']
		except NominaCoopD.DoesNotExist:
			totalARS = 0
		return totalARS

	@property
	def CAFETERIA(self):
		try:
			totalCAFETERIA = NominaCoopD.objects.values('cafeteria').filter(nomina=self.id).aggregate(total=Sum('cafeteria'))['total']
		except NominaCoopD.DoesNotExist:
			totalCAFETERIA = 0
		return totalCAFETERIA

	@property
	def VACACIONES(self):
		try:
			totalVACACIONES = NominaCoopD.objects.values('vacaciones').filter(nomina=self.id).aggregate(total=Sum('vacaciones'))['total']
		except NominaCoopD.DoesNotExist:
			totalVACACIONES = 0
		return totalVACACIONES

	@property
	def OTROSINGRESOS(self):
		try:
			totalOTROSINGRESOS = NominaCoopD.objects.values('otrosIngresos').filter(nomina=self.id).aggregate(total=Sum('otrosIngresos'))['total']
		except NominaCoopD.DoesNotExist:
			totalOTROSINGRESOS = 0
		return totalOTROSINGRESOS

	@property
	def DESCAHORROS(self):
		try:
			totalDESCAHORROS = NominaCoopD.objects.values('descAhorros').filter(nomina=self.id).aggregate(total=Sum('descAhorros'))['total']
		except NominaCoopD.DoesNotExist:
			totalDESCAHORROS = 0
		return totalDESCAHORROS

	@property
	def DESCPRESTAMOS(self):
		try:
			totalDESCPRESTAMOS = NominaCoopD.objects.values('descPrestamos').filter(nomina=self.id).aggregate(total=Sum('descPrestamos'))['total']
		except NominaCoopD.DoesNotExist:
			totalDESCPRESTAMOS = 0
		return totalDESCPRESTAMOS

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
	salario = models.DecimalField(max_digits=12, decimal_places=2)
	isr = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
	afp = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
	ars = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
	cafeteria = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
	vacaciones = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
	otrosIngresos = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
	horasExtras = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
	descAhorros = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0) #Este actualizado a traves del proceso especial
	descPrestamos = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0) #Este actualizado a traves del proceso especial
	tipoPago = models.CharField(max_length=1, choices=tipo_pago_choices, default='B')
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='E')

	def __unicode__(self):
		return '%s' % (self.nomina.fechaNomina)

	@property
	def getcodigo(self):
		return '%s' % (self.empleado.socio.codigo)

	@property
	def getCuentaBanco(self):
		return '%s' % (self.empleado.socio.cuentaBancaria)

	@property
	def pago(self):
		descuentos = self.descuentos #self.isr + self.afp + self.ars + self.cafeteria + self.descAhorros + self.descPrestamos
		ingresos = self.ingresos #self.vacaciones + self.otrosIngresos
		neto = ingresos - descuentos #self.salario + ingresos - descuentos

		return '$%s' % str(format(neto,',.2f'))

	@property
	def descuentos(self):
		return self.isr + self.afp + self.ars + self.cafeteria + self.descAhorros + self.descPrestamos

	@property
	def ingresos(self):
		return self.salario + self.vacaciones + self.otrosIngresos

	class Meta:
		unique_together = ('nomina', 'empleado')
		verbose_name = 'Nomina Detalles'
		verbose_name_plural = 'Nominas Detalles'


# Nominas Generadas para Prestamos y Ahorros
class NominaPrestamosAhorros(models.Model):

	nomina = models.DateField()
	tipo = models.CharField(max_length=2) # PR = Prestamos, AH = Ahorros, BP = Balance Prestamos, BA = Balance Ahorros
	estatus = models.CharField(max_length=2, default='PE') # PE = PENDIENTE, PO = PROCESADA
	infoTipo = models.CharField(max_length=4, null=True, blank=True)

	class Meta:
		verbose_name = 'Nomina Prestamos Ahorros'
		verbose_name_plural = 'Nomina Prestamos Ahorros'
		unique_together = ('nomina', 'infoTipo')


# Cuotas Prestamos para Nomina Empresa (el listado de montos a descontar a cada socio en cada quincena de nomina)
class CuotasPrestamosEmpresa(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),)

	socio = models.ForeignKey(Socio)
	noPrestamo = models.ForeignKey(MaestraPrestamo)
	valorCapital = models.DecimalField(max_digits=8, decimal_places=2)
	valorInteres = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	valorInteresAh = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	nomina = models.DateField(null=True)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')
	infoTipoPrestamo = models.CharField(max_length=4, default='0015')

	fecha = models.DateField(auto_now=True)
	userLog = models.ForeignKey(User)

	def save(self, *args, **kwargs):
		pago = PagoCuotasPrestamo()
		pago.noPrestamo = self.noPrestamo
		pago.valorCapital = self.valorCapital
		pago.valorInteres = self.valorInteres
		pago.valorInteresAh = self.valorInteresAh
		pago.docRef = '{0}'.format(self.nomina)
		pago.tipoPago = 'NM'
		pago.save()

		super(CuotasPrestamosEmpresa, self).save(*args, **kwargs)
		
	@property
	def codigoSocio(self):
		return '%s' % (self.socio.codigo)

	@property
	def montoTotal(self):
		return self.valorCapital + self.valorInteres + self.valorInteresAh

	class Meta:
		unique_together = ('noPrestamo', 'nomina')

# Cuotas Ahorros para Nomina Empresa
class CuotasAhorrosEmpresa(models.Model):

	estatus_choices = (('P','Pendiente'),('A','Aprobado'),)

	socio = models.ForeignKey(Socio)
	valorAhorro = models.DecimalField(max_digits=8, decimal_places=2)
	nomina = models.DateField()
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='P')

	fecha = models.DateField(auto_now=True)
	userLog = models.ForeignKey(User)
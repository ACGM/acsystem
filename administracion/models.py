# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

import datetime


# Localidades
class Localidad(models.Model):

	descripcion = models.CharField(max_length=150)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Distritos
class Distrito(models.Model):

	descripcion = models.CharField(max_length=150)
	localidad = models.ForeignKey(Localidad)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Departamentos
class Departamento(models.Model):

	centroCosto = models.CharField("Centro de Costo", max_length=10)
	descripcion = models.CharField(max_length=150)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Representantes
class Representatne(models.Model):

	nombre = models.CharField(max_length=150)

	def __unicode__(self):
		return '%s' % (self.nombre)


# Unidades de productos
class Unidad(models.Model):

	descripcion = models.CharField(max_length=20)
	nota = models.TextField()


# PRODUCTOS para registrarlos en la facturacion
class Producto(models.Model):
	
	codigo = models.CharField(max_length=10)
	descripcion = models.CharField(max_length=150)
	unidad = models.ForeignKey(Unidad)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	costo = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
	foto = models.ImageField(upload_to='productos', blank=True, null=True)

	userLog = models.ForeignKey(User)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Tipo de suplidores
class TipoSuplidor(models.Model):
	
	descripcion = models.CharField(max_length=100)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Suplidores/Proveedores registrados
class Suplidor(models.Model):
	
	tipoIdentificacion_choices = (('C','Cedula'),('R','RNC'))
	clase_choices = (('N','Normal'),('S','SuperCoop'))

	tipoIdentificacion = models.CharField(max_length=1, choices=tipoIdentificacion_choices, default='C')
	cedulaRNC = models.CharField(max_length=25)
	nombre = models.CharField(max_length=150)
	direccion = models.TextField(blank=True)
	sector = models.CharField(max_length=100, blank=True)
	ciudad = models.CharField(max_length=100, blank=True)
	contacto = models.CharField(max_length=150, blank=True)
	telefono = models.CharField(max_length=50, blank=True)
	fax = models.CharField(max_length=50, blank=True)
	intereses = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
	tipoSuplidor = models.ForeignKey(TipoSuplidor)
	clase = models.CharField(max_length=1, choices=clase_choices, default='N')

	userLog = models.ForeignKey(User)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s - %s' % (self.cedulaRNC, self.nombre)

	class Meta:
		ordering = ['nombre']


# Socios de la cooperativa
class Socio(models.Model):
	
	sexo_choices = (('M','Masculino'),('F','Femenino'),)
	estado_civil_choices = (('S','Soltero(a)'),('C','Casado(a)'),('U','Union Libre'),)
	estatus_choices = (('S','Socio'),('E','Empleado'),('I','Inactivo'),)

	codigo = models.IntegerField()
	nombres = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)
	direccion = models.TextField(blank=True)
	sector = models.CharField(max_length=150, blank=True)
	telefono = models.CharField(max_length=150, blank=True)
	celular = models.CharField(max_length=150, blank=True)
	ciudad = models.CharField(max_length=150, blank=True)
	cedula = models.CharField(max_length=20, blank=True)
	sexo = models.CharField(max_length=1, choices=sexo_choices, default='M')
	estadoCivil = models.CharField("Estado Civil", max_length=1, choices=estado_civil_choices, default='S')
	pasaporte = models.CharField("Pasaporte No.", max_length=20, blank=True)
	carnetNumero = models.IntegerField("Carnet Numero")
	fechaIngresoCoop = models.DateField("Fecha de Ingreso Coop.")
	fechaIngresoEmpresa = models.DateField("Fecha de Ingreso Empresa")
	correo = models.EmailField(blank=True)
	departamento = models.ForeignKey(Departamento)
	distrito = models.ForeignKey(Distrito)
	estatus = models.CharField(max_length=2, choices=estatus_choices, default='S')
	salario = models.DecimalField(max_digits=12, decimal_places=2)
	cuentaBancaria = models.CharField("Cuenta Bancaria", max_length=20, blank=True)
	foto = models.ImageField(upload_to='administracion', blank=True, null=True)
	nombreCompleto = models.CharField("Nombre Completo", max_length=200, editable=False)

	user_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%i - %s %s' % (self.codigo,self.nombres,self.apellidos)

	class Meta:
		ordering = ['codigo']


# Co-Beneficiarios del socio
class CoBeneficiario(models.Model):

	parentesco_choices = (('C','Conyugue'), ('H','Hijo(a)'), ('T','Tio(a)'),('A','Abuelo(a)'), ('O','Otro'))

	socio = models.ForeignKey(Socio)
	nombre = models.CharField(max_length=150)
	direccion = models.TextField()
	sector = models.CharField(max_length=150)
	ciudad = models.CharField(max_length=100)
	cedula = models.CharField(max_length=15)
	telefono = models.CharField(max_length=100)
	celular = models.CharField(max_length=100)
	parentesco = models.CharField(max_length=1, choices=parentesco_choices, default='O')

	def __unicode__(self):
		return '%s' % (self.nombre)

	class Meta:
		ordering = ['nombre']


# Categorias de Prestamos
class CategoriaPrestamo(models.Model):
	
	tipo_choices = (('OD','Orden de Despacho'),('PR','Prestamo'),('SC','SuperCoop'),)

	descripcion = models.CharField(max_length=150)
	montoDesde = models.DecimalField("Monto Desde", max_digits=12, decimal_places=2, blank=True)
	montoHasta = models.DecimalField("Monto Hasta", max_digits=12, decimal_places=2, blank=True)
	tipo = models.CharField(max_length=2, choices=tipo_choices)
	interesAnualSocio = models.DecimalField("Intereses Anual Socio", max_digits=6, decimal_places=2)
	interesAnualEmpleado = models.DecimalField("Intereses Anual Empleado", max_digits=6, decimal_places=2)
	interesAnualDirectivo = models.DecimalField("Intereses Anual Directivo", max_digits=6, decimal_places=2)

	userLog = models.ForeignKey(User)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Cuotas de montos segun Prestamos
class CuotaPrestamo(models.Model):
	
	montoDesde = models.DecimalField("Monto Desde", max_digits=12, decimal_places=2)
	montoHasta = models.DecimalField("Monto Hasta", max_digits=12, decimal_places=2)
	cantidadQuincenas = models.PositiveIntegerField("Cantidad de Quincenas")
	cantidadMeses = models.PositiveIntegerField("Cantidad de Meses")

	user_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-montoDesde']


# Cuotas de montos segun Ordenes de Despacho
class CuotaOrdenes(models.Model):

	montoDesde = models.DecimalField("Monto Desde", max_digits=12, decimal_places=2)
	montoHasta = models.DecimalField("Monto Hasta", max_digits=12, decimal_places=2)
	cantidadQuincenas = models.PositiveIntegerField("Cantidad de Quincenas")
	cantidadMeses = models.PositiveIntegerField("Cnatidad de Meses")

	userLog = models.ForeignKey(User)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-montoDesde']


# Opciones
class Opcion(models.Model):

	tipo_choices = (('P','Principal'),('S','Secundario'),)

	descripcion = models.CharField(max_length=80)
	tipo = models.CharField(max_length=1, choices=tipo_choices, default='P')

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Perfiles
class Perfil(models.Model):

	perfilCod = models.CharField("Codigo Perfil", max_length=10, unique=True)
	opcion = models.ForeignKey(Opcion)

	def __unicode__(self):
		return '%s - %s' % (self.perfilCod, self.opcion)

	class Meta:
		ordering = ['perfilCod']


# Autorizadores
class Autorizador(models.Model):

	usuario = models.ForeignKey(User)
	perfil = models.ForeignKey(Perfil)

	datetimeServer = models.DateTimeField(auto_now_add=True)


# Tipos de Notas de Credito Globales
class TipoNCGlobal(models.Model):

	tipo_choices = (('1','NCG'),('2','NCG2'),)

	tipo = models.CharField(max_length=1, choices=tipo_choices, default='')
	descripcion = models.CharField(max_length=150)
	cuenta = models.ForeignKey(CuentaContable)


# Bancos
class Banco(models.Model):

	codigo = models.CharField(max_length=25)
	nombre = models.CharField(max_length=100)

	def __unicode__(self):
		return '%s - %s' % (self.codigo,self.nombre)

	class Meta:
		ordering = ['nombre']


# Tipos de Documentos
class TipoDocumento(models.Model):

	codigo = models.CharField(max_length=4)
	descripcion = models.CharField(max_length=150)

	def __unicode__(self):
		return '%s - %s' % (self.codigo,self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Periodos (Fiscales)
class Periodo(models.Model):

	estatus_choices = (('A','Activo'), ('C','Cerrado',))
	mes_choices = (
					('01','Enero'),('02','Febrero'),
					('03','Marzo'),('04','Abril'),
					('05','Mayo'),('06','Junio'),
					('07','Julio'),('08','Agosto'),
					('09','Septiembre'),('10','Octubre'),
					('11','Noviembre'),('12','Diciembre'),
		)

	mes = models.CharField(max_length=2, choices=mes_choices, default='01')
	agno = models.CharField("Año", max_length=4)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')

	def __unicode__(self):
		return '%s%s' % (self.mes,self.agno)

	class Meta:
		ordering = ['-agno']


# Empresas
class Empresa(models.Model):

	nombre = models.CharField(max_length=100)

	def __unicode__(self):
		return '%s' % (self.nombre)


# Cargos
class Cargo(models.Model):

	descripcion = models.CharField(max_length=100)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Cobradores
class Cobrador(models.Model):

	codigo = models.ForeignKey(EmpleadoCoop)
	userLog = models.ForeignKey(User)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.user)

	class Meta:
		ordering = ['codigo']
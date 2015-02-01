# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from cuenta.models import Cuentas, Auxiliares

import datetime


# Localidades
class Localidad(models.Model):

	descripcion = models.CharField(max_length=150)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion',]
		verbose_name_plural = 'Config 2.6) Localidades'


# Distritos
class Distrito(models.Model):

	descripcion = models.CharField(max_length=150)
	localidad = models.ForeignKey(Localidad)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion',]
		verbose_name_plural = 'Config 2.5) Distritos'


# Departamentos
class Departamento(models.Model):

	centroCosto = models.CharField("Centro de Costo", max_length=10)
	descripcion = models.CharField(max_length=80)

	def __unicode__(self):
		return '%s: %s' % (self.centroCosto, self.descripcion)

	def save(self, *args, **kwargs):
		self.descripcion = self.descripcion.title()

		super(Departamento, self).save(*args, **kwargs)

	class Meta:
		ordering = ['descripcion',]
		verbose_name_plural = 'Config 1.4) Departamentos'


# Representantes
class Representante(models.Model):

	nombre = models.CharField(max_length=50)

	def __unicode__(self):
		return '%s' % (self.nombre)

	class Meta:
		verbose_name_plural = 'Config 2.3) Representantes'


# Unidades de productos
class Unidad(models.Model):

	descripcion = models.CharField(max_length=20)
	nota = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.descripcion

	class Meta:
		verbose_name = 'Unidad'
		verbose_name_plural = 'Config 4.2) Unidades'


# PRODUCTOS para registrarlos en la facturacion
class Producto(models.Model):
	
	codigo = models.CharField(max_length=10, editable=False)
	descripcion = models.CharField(max_length=50)
	unidad = models.ForeignKey(Unidad)
	precio = models.DecimalField(max_digits=12, decimal_places=2)
	costo = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
	foto = models.ImageField(upload_to='productos', blank=True, null=True)

	userLog = models.ForeignKey(User, editable=False)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	def save(self, *args, **kwargs):
		self.descripcion = self.descripcion.upper()

		sec = Producto.objects.all().count() + 1
		self.codigo = self.descripcion[:3].upper() + ('0000' + str(sec))[-4:]

		super(Producto, self).save(*args, **kwargs)

	class Meta:
		ordering = ['descripcion']
		verbose_name_plural = 'Config 4.1) Productos'


# Tipo de suplidores
class TipoSuplidor(models.Model):
	
	descripcion = models.CharField(max_length=100)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'Tipo de Suplidor'
		verbose_name_plural = 'Config 4.4) Tipos de Suplidores'


# Suplidores/Proveedores registrados
class Suplidor(models.Model):
	
	tipoIdentificacion_choices = (('C','Cedula'),('R','RNC'))
	clase_choices = (('N','Normal'),('S','SuperCoop'))
	estatus_choices = (('A','Activo'), ('I','Inactivo'))

	tipoIdentificacion = models.CharField(max_length=1, choices=tipoIdentificacion_choices, default='C')
	cedulaRNC = models.CharField(unique=True, max_length=25)
	nombre = models.CharField(max_length=60)
	direccion = models.TextField(blank=True)
	sector = models.CharField(max_length=40, blank=True)
	ciudad = models.CharField(max_length=40, blank=True)
	contacto = models.CharField(max_length=50, blank=True)
	telefono = models.CharField(max_length=50, blank=True)
	fax = models.CharField(max_length=50, blank=True)
	intereses = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
	tipoSuplidor = models.ForeignKey(TipoSuplidor)
	clase = models.CharField(max_length=1, choices=clase_choices, default='N')
	auxiliar = models.ForeignKey(Auxiliares, null=True)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')

	userLog = models.ForeignKey(User, editable=False)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.nombre)

	def save(self, *args, **kwargs):
		self.nombre = self.nombre.upper()

		super(Suplidor, self).save(*args, **kwargs)

	class Meta:
		ordering = ['nombre']
		verbose_name_plural = 'Config 4.3) Suplidores'


# Socios de la cooperativa
class Socio(models.Model):
	
	sexo_choices = (('M','Masculino'),('F','Femenino'),)
	estado_civil_choices = (('S','Soltero(a)'),('C','Casado(a)'),('U','Union Libre'),)
	estatus_choices = (('S','Socio'),('E','Empleado'),('I','Inactivo'),)

	codigo = models.PositiveIntegerField()
	nombres = models.CharField(max_length=40)
	apellidos = models.CharField(max_length=40)
	direccion = models.TextField(blank=True)
	sector = models.CharField(max_length=40, blank=True)
	telefono = models.CharField(max_length=40, blank=True)
	celular = models.CharField(max_length=40, blank=True)
	ciudad = models.CharField(max_length=40, blank=True)
	cedula = models.CharField(max_length=20, blank=True)
	sexo = models.CharField(max_length=1, choices=sexo_choices, default='M')
	estadoCivil = models.CharField("Estado Civil", max_length=1, choices=estado_civil_choices, default='S')
	pasaporte = models.CharField("Pasaporte No.", max_length=20, blank=True)
	# carnetNumero = models.PositiveIntegerField("Carnet Numero")
	fechaIngresoCoop = models.DateField("Fecha de Ingreso Coop.")
	fechaIngresoEmpresa = models.DateField("Fecha de Ingreso Empresa")
	correo = models.EmailField(blank=True)
	departamento = models.ForeignKey(Departamento)
	distrito = models.ForeignKey(Distrito)
	estatus = models.CharField(max_length=2, choices=estatus_choices, default='S')
	salario = models.DecimalField(max_digits=12, decimal_places=2, null=True, default=0)
	cuentaBancaria = models.CharField("Cuenta Bancaria", max_length=20, blank=True)
	foto = models.ImageField(upload_to='administracion', blank=True, null=True)
	nombreCompleto = models.CharField("Nombre Completo", max_length=80, editable=False)

	userLog = models.ForeignKey(User, editable=False)
	datetime_server = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.nombreCompleto)

	
	def save(self, *args, **kwargs):
		self.nombres = self.nombres.upper()
		self.apellidos = self.apellidos.upper()

		self.nombreCompleto = self.nombres.upper() + ' ' + self.apellidos.upper()

		super(Socio, self).save(*args, **kwargs)

	class Meta:
		ordering = ['codigo']
		verbose_name = 'Config 1) Socio'
		verbose_name_plural = 'Config 1.1) Socios'


# Co-Beneficiarios del socio
class CoBeneficiario(models.Model):

	parentesco_choices = (('C','Conyugue'), ('H','Hijo(a)'), ('T','Tio(a)'),('A','Abuelo(a)'), ('O','Otro'))

	socio = models.ForeignKey(Socio)
	nombre = models.CharField(max_length=100)
	direccion = models.TextField(null=True, blank=True)
	sector = models.CharField(max_length=40, null=True, blank=True)
	ciudad = models.CharField(max_length=40, null=True, blank=True)
	cedula = models.CharField(max_length=15, null=True, blank=True)
	telefono = models.CharField(max_length=40, null=True, blank=True)
	celular = models.CharField(max_length=40, null=True, blank=True)
	parentesco = models.CharField(max_length=1, choices=parentesco_choices, default='O')

	def __unicode__(self):
		return '%s' % (self.nombre)

	def save(self, *args, **kwargs):
		self.nombre = self.nombre.upper()

		super(CoBeneficiario, self).save(*args, **kwargs)

	class Meta:
		ordering = ['nombre']
		verbose_name = 'Config 1) Co-Beneficiario'
		verbose_name_plural = 'Config 1.2) Co-Beneficiarios'


# Categorias de Prestamos
class CategoriaPrestamo(models.Model):
	
	tipo_choices = (('OD','Orden de Despacho'),('PR','Prestamo'),('SC','SuperCoop'),)

	descripcion = models.CharField(max_length=70)
	montoDesde = models.DecimalField("Monto Desde", max_digits=18, decimal_places=2, blank=True)
	montoHasta = models.DecimalField("Monto Hasta", max_digits=18, decimal_places=2, blank=True)
	tipo = models.CharField(max_length=2, choices=tipo_choices)
	interesAnualSocio = models.DecimalField("Intereses Anual Socio", max_digits=6, decimal_places=2, null=True, blank=True)
	interesAnualEmpleado = models.DecimalField("Intereses Anual Empleado", max_digits=6, decimal_places=2, null=True, blank=True)
	interesAnualDirectivo = models.DecimalField("Intereses Anual Directivo", max_digits=6, decimal_places=2, null=True, blank=True)

	userLog = models.ForeignKey(User, editable=False)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	def save(self, *args, **kwargs):
		self.descripcion = self.descripcion.upper()

		super(CategoriaPrestamo, self).save(*args, **kwargs)

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'Categoria de Prestamo'
		verbose_name_plural = 'Config 6.1) Categorias de Prestamos'


# Cuotas de montos segun Prestamos
class CuotaPrestamo(models.Model):
	
	montoDesde = models.DecimalField("Monto Desde", max_digits=18, decimal_places=2)
	montoHasta = models.DecimalField("Monto Hasta", max_digits=18, decimal_places=2)
	cantidadQuincenas = models.PositiveIntegerField("Cantidad de Quincenas")

	userLog = models.ForeignKey(User, editable=False)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return 'Monto desde: %s Hasta %s -- %i Cuotas' % (self.montoDesde, self.montoHasta, self.cantidadQuincenas)

	class Meta:
		ordering = ['-montoDesde']
		verbose_name = 'Cuota de Prestamo'
		verbose_name_plural = 'Config 6.2) Cuotas de Prestamos'


# Cuotas de montos segun Ordenes de Despacho
class CuotaOrdenes(models.Model):

	montoDesde = models.DecimalField("Monto Desde", max_digits=18, decimal_places=2)
	montoHasta = models.DecimalField("Monto Hasta", max_digits=18, decimal_places=2)
	cantidadQuincenas = models.PositiveIntegerField("Cantidad de Quincenas")

	userLog = models.ForeignKey(User, editable=False)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-montoDesde']
		verbose_name = 'Cuota de Ordenes'
		verbose_name_plural = 'Config 6.3) Cuotas de Ordenes'


# Opciones
class Opcion(models.Model):

	tipo_choices = (('P','Principal'),('S','Secundario'),)

	descripcion = models.CharField(max_length=80)
	tipo = models.CharField(max_length=1, choices=tipo_choices, default='P')

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']
		verbose_name_plural = 'Config 3.3) Opciones'


# Perfiles
class Perfil(models.Model):

	perfilCod = models.CharField("Codigo Perfil", max_length=10, unique=True)
	opcion = models.ForeignKey(Opcion)

	def __unicode__(self):
		return '%s - %s' % (self.perfilCod, self.opcion)

	class Meta:
		ordering = ['perfilCod']
		verbose_name_plural = 'Config 3.4) Perfiles'


# Autorizadores
class Autorizador(models.Model):

	usuario = models.ForeignKey(User)
	perfil = models.ForeignKey(Perfil)

	datetimeServer = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['usuario']
		verbose_name_plural = 'Config 3.1) Autorizadores'


# Tipos de Notas de Credito Globales
class TipoNCGlobal(models.Model):

	tipo_choices = (('1','NCG'),('2','NCG2'),)

	tipo = models.CharField(max_length=1, choices=tipo_choices, default='')
	descripcion = models.CharField(max_length=150)
	cuenta = models.ForeignKey(Cuentas)


# Bancos
class Banco(models.Model):

	codigo = models.CharField(max_length=25)
	nombre = models.CharField(max_length=100)

	def __unicode__(self):
		return '%s - %s' % (self.codigo,self.nombre)

	def save(self, *args, **kwargs):
		self.nombre = self.nombre.upper()

		super(Banco, self).save(*args, **kwargs)

	class Meta:
		ordering = ['nombre']
		verbose_name_plural = 'Config 2.1) Bancos'


# Tipos de Documentos
class TipoDocumento(models.Model):

	codigo = models.CharField(max_length=4)
	descripcion = models.CharField(max_length=50)

	def __unicode__(self):
		return '%s - %s' % (self.codigo,self.descripcion)

	class Meta:
		ordering = ['descripcion']
		verbose_name_plural = 'Config 7.1) Tipos de Documentos'


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
	agno = models.CharField("Agno", max_length=4)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')

	def __unicode__(self):
		return '%s%s' % (self.mes,self.agno)

	class Meta:
		ordering = ['-agno']
		verbose_name_plural = 'Config 7.3) Periodos'


# Empresas
class Empresa(models.Model):

	nombre = models.CharField(max_length=100)
	rnc = models.CharField(max_length=15, blank=True, null=True)
	bancoAsign = models.CharField(max_length=5, blank=True, null=True)

	def __unicode__(self):
		return '%s' % (self.nombre)

	class Meta:
		verbose_name_plural = 'Config 2.2) Empresas'


# Cobradores
class Cobrador(models.Model):

	usuario = models.CharField(max_length=10)
	userLog = models.ForeignKey(User, unique=True)
	datetimeServer = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.usuario)

	class Meta:
		ordering = ['usuario']
		verbose_name_plural = 'Config 3.2) Cobradores'


# Asociacion de Documentos con Cuentas
class DocumentoCuentas(models.Model):

	accion_choices = (('D','Debito'),('C','Credito'))

	documento = models.ForeignKey(TipoDocumento)
	cuenta = models.ForeignKey(Cuentas)
	accion = models.CharField(max_length=1, choices=accion_choices)

	def __unicode__(self):
		return '%s - %s (%s)' % (self.documento, self.cuenta, self.accion)

	class Meta:
		ordering = ['documento','cuenta']
		verbose_name = 'Documento relacionado a Cuentas'
		verbose_name_plural = 'Config 7.2) Documentos relacionados a Cuentas'
	

# Cuotas de Ahorros de Socios
class CuotaAhorroSocio(models.Model):

	socio = models.ForeignKey(Socio, unique=True)
	cuotaAhorroQ1 = models.DecimalField("Cuota Ahorro Q1", max_digits=12, decimal_places=2, null=True, blank=True)
	cuotaAhorroQ2 = models.DecimalField("Cuota Ahorro Q2", max_digits=12, decimal_places=2, null=True, blank=True)

	userLog = models.ForeignKey(User, editable=False)
	fechaInicioAhorro = models.DateField(auto_now_add=True, default=datetime.datetime.now())
	fechaModificacion = models.DateField(auto_now=True, default=datetime.datetime.now())

	class Meta:
		ordering = ['socio']
		verbose_name = 'Config 1) Cuota Ahorro Socio'
		verbose_name_plural = 'Config 1.3) Cuotas Ahorros Socios'


# Archivos para Banco
class ArchivoBancoNomina(models.Model):

	bancoAsign = models.CharField(max_length=5) # Numero Asignado a la Empresa de cinco posiciones
	tipoServicio = models.CharField(max_length=2) #T ipo de Servicio de dos posiciones
	envio = models.CharField(max_length=4) # MMDD mes y dia en que se envia el archivo
	secuencia = models.PositiveIntegerField() # Secuencia del header de siete posiciones

	datetimeServer = models.DateTimeField(auto_now_add=True)
	
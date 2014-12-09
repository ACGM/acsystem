from django.db import models
from django.contrib.auth import User

import datetime


# Catalogo de Cuentas
class CuentaContable(models.Model):

	tipo_cuenta_choices = (('G','General'),('D','Detalle'),)
	origen_choices = (('D','Debito'),('C','Credito'),)

	codigo = models.CharField(max_length=15)
	descripcion = models.CharField(max_length=150)
	tipoCuenta = models.CharField(max_length=1, choices=tipo_cuenta_choices, default='G')
	origen = models.CharField(max_length=1, choices=origen_choices)
	cuentaControl = models.BooleanField(default=False)

	user_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s - %s' % (self.codigo, self.descripcion)

	class Meta:
		ordering = ['codigo']


# PRODUCTOS para registrarlos en la facturacion
class Producto(models.Model):
	
	unidades_choices = (('UN','Unidad'),('CA','Caja'),)

	codigo = models.CharField(max_length=10)
	descripcion = models.CharField(max_length=150)
	unidad = models.CharField(max_length=2, 
								choices=unidades_choices, 
								default=unidades_choices[0][0])
	precio = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
	costo = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
	foto = models.ImageField(upload_to='productos', blank=True)

	user_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)

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

	user_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.nombre)

	class Meta:
		ordering = ['nombre']


# Auxiliares
class Auxiliar(models.Model):

	estatus_choices = (('A','Activo'),('I','Inactivo'))

	codigo = models.CharField(max_length=10)
	cuenta = models.ForeignKey(CuentaContable)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')


# Socios de la cooperativa
class Socio(model.Model):
	
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
	estado_civil = models.CharField(max_length=1, choices=estado_civil_choices, default='S')
	pasaporte = models.CharField(max_length=20, blank=True)
	carnet_numero = models.IntegerField()
	fecha_ingreso_coop = models.DateField()
	fecha_ingreso_empresa = models.DateField()
	correo = models.EmailField(blank=True)
	departamento = models.ForeignKey(Departamento)
	distrito = models.ForeignKey(Distrito)
	estatus = models.CharField(max_length=2, choices=estatus_choices, default='S')
	salario = models.DecimalField(max_length=12, decimal_places=2)
	cuenta_bancaria = models.CharField(max_length=20, blank=True)
	foto = models.ImageField(upload_to='administracion')


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


# Categorias de Prestamos
class CategoriaPrestamo(models.Model):
	
	tipo_choices = (('OD','Orden de Despacho'),('PR','Prestamo'),('SC','SuperCoop'),)

	descripcion = models.CharField(max_length=150)
	monto_desde = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
	monto_hasta = models.DecimalField(max_length=12, decimal_places=2, blank=True)
	tipo = models.CharField(max_length=2, choices=tipo_choices)
	interes_anual_socio = models.DecimalField(max_digits=6, decimal_places=2)
	interes_anual_empleado = models.DecimalField(max_digits=6, decimal_places=2)
	interes_anual_directivo = models.DecimalField(max_digits=6, decimal_places=2)

	user_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return '%s' % (self.descripcion)

	class Meta:
		ordering = ['descripcion']


# Cuentas Contables
class CuentaContable(models.Model):
	
	pass


# Localidades
class Localidad(models.Model):

	descripcion = models.CharField(max_length=150)

	def __unicode__(self):
		return '%s' % (self.descripcion)


# Distritos
class Distrito(models.Model):

	descripcion = models.CharField(max_length=150)
	localidad = models.ForeignKey(Localidad)


# Cobradores
class Cobrador(models.Model):

	codigo = models.ForeignKey(Empleado)
	user = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)

# Departamentos
class Departamento(models.Model):

	centro_costo = models.CharField(max_length=10)
	descripcion = models.CharField(max_length=150)


# Representantes
class Representatne(models.Model):

	nombre = models.CharField(max_length=150)

	def __unicode__(self):
		return '%s' % (self.nombre)


# Cuotas de montos segun Prestamos
class CuotaPrestamo(models.Model):
	
	monto_desde = models.DecimalField(max_digits=12, decimal_places=2)
	monto_hasta = models.DecimalField(max_digits=12, decimal_places=2)
	cantidad_quincenas = models.PositiveIntegerField()
	cantidad_meses = models.PositiveIntegerField()

	user_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)


# Cuotas de montos segun Ordenes de Despacho
class CuotaPrestamo(models.Model):

	monto_desde = models.DecimalField(max_digits=12, decimal_places=2)
	monto_hasta = models.DecimalField(max_digits=12, decimal_places=2)
	cantidad_quincenas = models.PositiveIntegerField()
	cantidad_meses = models.PositiveIntegerField()

	user_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)


# Opciones
class Opcion(models.Model):

	tipo_choices = (('P','Principal'),('S','Secundario'),)

	descripcion = models.CharField(max_length=80)
	tipo = models.CharField(max_length=1, choices=tipo_choices, default='P')


# Perfiles
class Perfil(models.Model):

	opcion = models.CharField(max_length=50)
	perfil_cod = models.CharField(max_length=10)


# Autorizadores
class Autorizador(models.Model):

	user = models.ForeignKey(User)
	perfil = models.ForeignKey(Perfil)

	user_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)


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


# Tipos de Documentos
class TipoDocumento(models.Model):

	codigo = models.CharField(max_length=4)
	descripcion = models.CharField(max_length=150)


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
	agno = models.CharField(max_length=4)
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')


# RECURSOS HUMANOS DE LA COOPERATIVA

# Empresas
class Empresa(models.Model):

	nombre = models.CharField(max_length=100)


# Cargos
class Cargo(models.Model):

	descripcion = models.CharField(max_length=100)


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
	direccion = models.TextField(blank=True)
	sector = models.CharField(max_length=100, blank=True)
	ciudad = models.CharField(max_length=80, blank=True)
	telefono = models.CharField(max_length=50, blank=True)
	fechaNac = models.DateField(blank=True)
	lugarNac = models.CharField(max_length=100, blank=True)
	estadoCivil = models.CharField(max_length=1, choices=estado_civil_choices, default='S')
	sexo = modelf.CharField(max_length=1, choices=sexo_choices, default='M')
	dependencias = models.PositiveIntegerField(blank=True)
	fechaIngreso = models.DateField(default=datetime.now())
	empresa = models.ForeignKey(Empresa)
	departamento = models.ForeignKey(Departamento)
	tipoContrato = models.CharField(max_length=1, choices=tipo_empleado_choices, default='F')
	cargo = models.ForeignKey(Cargo)
	tipoCobro = models.CharField(max_length=1, choices=tipo_empleado_choices, default='Q')
	tipoPago = models.CharField(max_length=1, choices=tipo_pago_choices, default='B')
	sueldoActual = models.DecimalField(max_digits=12, decimal_places=2)
	sueldoAnterior = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
	activo = models.BooleanField(default=True)
	fechaSalida = models.DateField(blank=True)


# Tipos de nominas
class TipoNomina(models.Model):

	descripcion = models.CharField(max_length=50)


# Cabecera Nomina de Cooperativa
class NominaCoopH(models.Model):

	tipo_pago_choices = (('E','Efectivo'),('C','Cheque'),('B','Banco'),)
	estatus_choices = (('P','Procesada'),('E','En proceso'),)

	fechaNomina = models.DateField(default=datetime.now())
	fechaPago = models.DateField(default=datetime.now())
	empleados = models.IntegerField()
	valorNomina = models.DecimalField(max_digits=12, decimal_places=2)
	tipoNomina = models.ForeignKey(TipoNomina)
	tipoPago = models.CharField(max_length=1, choices=tipo_pago_choices, default='B')
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='E')
	nota = models.TextField(blank=True)

	user_log = models.ForeignKey(User)
	datetime_server = models.DateTimeField(auto_now_add=True)


# Detalle Nomina de Cooperativa
class NominaCoopD(models.Model):

	tipo_pago_choices = (('E','Efectivo'),('C','Cheque'),('B','Banco'),)
	estatus_choices = (('P','Procesada'),('E','En proceso'),)

	fecha = models.DateField(auto_now_add)
	fechaNomina = models.DateField(default=datetime.now())
	userLog = models.ForeignKey(User)
	empleado = models.ForeignKey(Empleado)
	salario = models.DecimalField(max_digits=12, decimal_places=2)
	afp = models.DecimalField(max_digits=12, decimal_places=2)
	ars = models.DecimalField(max_digits=12, decimal_places=2)
	cafeteria = models.DecimalField(max_digits=12, decimal_places=2)
	vacaciones = models.DecimalField(max_digits=12, decimal_places=2)
	otrosIngresos = models.DecimalField(max_digits=12, decimal_places=2)
	descAhorros = models.DecimalField(max_digits=12, decimal_places=2)
	descPrestamos = models.DecimalField(max_digits=12, decimal_places=2)
	tipoPago = models.CharField(max_length=1, choices=tipo_pago_choices, default='B')
	estatus = models.CharField(max_length=1, choices=estatus_choices, default='E')
	
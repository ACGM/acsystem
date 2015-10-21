# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from cuenta.models import Cuentas

import datetime

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# Localidades
class Localidad(models.Model):
    descripcion = models.CharField(max_length=10)
    descripcionLarga = models.CharField(max_length=150, blank=True)

    def __unicode__(self):
        return '%s' % (self.descripcion)

    class Meta:
        ordering = ['descripcion', ]
        verbose_name_plural = 'Config 2.6) Localidades'


# Departamentos
class Departamento(models.Model):
    centroCosto = models.CharField("Centro de Costo", max_length=10)
    descripcion = models.CharField(max_length=80)

    def __unicode__(self):
        return '%s: %s' % (self.centroCosto, self.descripcion)

    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()

        super(Departamento, self).save(*args, **kwargs)

    class Meta:
        ordering = ['descripcion', ]
        verbose_name_plural = 'Config 1.4) Departamentos'


# Representantes
class Representante(models.Model):
    estatus_choices = (('A', 'Activo'), ('I', 'Inactivo'))

    nombre = models.CharField(max_length=50)
    estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')

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
        verbose_name_plural = 'Config 4.3) Unidades'


# CATEGORIA para productos
class CategoriaProducto(models.Model):
    descripcion = models.CharField(max_length=25)

    def __unicode__(self):
        return '%s' % (self.descripcion)

    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()

        super(CategoriaProducto, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Config 4.2) Categorias de Productos'
        ordering = ('descripcion',)


# PRODUCTOS para registrarlos en la facturacion
class Producto(models.Model):
    codigo = models.CharField(max_length=10, editable=False, unique=True)
    descripcion = models.CharField(max_length=50)
    unidad = models.ForeignKey(Unidad)
    categoria = models.ForeignKey(CategoriaProducto, null=True)
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

        try:
            p = Producto.objects.get(id=self.id)
        except Producto.DoesNotExist:
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
        verbose_name_plural = 'Config 4.5) Tipos de Suplidores'


# Suplidores/Proveedores registrados
class Suplidor(models.Model):
    tipoIdentificacion_choices = (('CE', 'Cedula'), ('RN', 'RNC'))
    clase_choices = (('N', 'Normal'), ('S', 'SuperCoop'))
    estatus_choices = (('A', 'Activo'), ('I', 'Inactivo'))
    sexo_choices = (('M', 'Masculino'), ('F', 'Femenino'),)

    tipoIdentificacion = models.CharField("Tipo de Identificacion", max_length=2, choices=tipoIdentificacion_choices,
                                          default='C', blank=True, null=True)
    cedulaRNC = models.CharField("Cedula o RNC", unique=True, max_length=25, blank=True, null=True)
    nombre = models.CharField(max_length=60)
    sexo = models.CharField(max_length=1, choices=sexo_choices, default='M', null=True, blank=True)
    direccion = models.TextField(blank=True)
    sector = models.CharField(max_length=40, blank=True, null=True)
    ciudad = models.CharField(max_length=40, blank=True, null=True)
    contacto = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    correo = models.CharField(max_length=40, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    intereses = models.DecimalField("Intereses %", max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    tipoSuplidor = models.ForeignKey(TipoSuplidor, null=True, blank=True)
    clase = models.CharField(max_length=1, choices=clase_choices, default='N')
    # auxiliar = models.ForeignKey(Auxiliares, null=True, blank=True)
    tipoCuentaBancaria = models.CharField("Tipo Cuenta Bancaria", max_length=2, null=True, blank=True)
    cuentaBancaria = models.CharField("Cuenta Bancaria", max_length=20, null=True, blank=True)
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
        verbose_name_plural = 'Config 4.4) Suplidores'


# Socios de la cooperativa
class Socio(models.Model):
    sexo_choices = (('M', 'Masculino'), ('F', 'Femenino'),)
    estado_civil_choices = (('S', 'Soltero(a)'), ('C', 'Casado(a)'), ('U', 'Union Libre'),)
    estatus_choices = (('S', 'Socio'), ('E', 'Empleado'), ('I', 'Inactivo'),)

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
    fechaIngresoCoop = models.DateField("Fecha de Ingreso Coop.")
    fechaIngresoEmpresa = models.DateField("Fecha de Ingreso Empresa")
    correo = models.EmailField(blank=True)
    departamento = models.ForeignKey(Departamento)
    localidad = models.ForeignKey(Localidad)
    estatus = models.CharField(max_length=2, choices=estatus_choices, default='S')
    salario = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
    cuentaBancaria = models.CharField("Cuenta Bancaria", max_length=20, blank=True, null=True)
    tipoCuentaBancaria = models.CharField("Tipo Cuenta Bancaria", max_length=1, default='1', blank=True, null=True)
    foto = models.FileField(upload_to='administracion', blank=True, null=True)
    nombreCompleto = models.CharField("Nombre Completo", max_length=80, editable=False)

    cuotaAhorroQ1 = models.DecimalField("Cuota Ahorro Q1", max_digits=12, decimal_places=2, default=0)
    cuotaAhorroQ2 = models.DecimalField("Cuota Ahorro Q2", max_digits=12, decimal_places=2, default=0)

    userLog = models.ForeignKey(User, editable=False)
    datetime_server = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s' % (self.nombreCompleto)

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()

        self.nombreCompleto = self.nombres.upper() + ' ' + self.apellidos.upper()

        super(Socio, self).save(*args, **kwargs)

        #Preparar la tabla AhorroSocio con Balance en Cero cuando es la primera vez.
        if self.id == None:
            from ahorro.models import AhorroSocio
            ah = AhorroSocio()
            ah.socio = self
            ah.balance = 0
            ah.disponible = 0
            ah.estatus = 'A'
            ah.save()

    class Meta:
        ordering = ['codigo']
        verbose_name = 'Socio'
        verbose_name_plural = 'Config 1.1) Socios'


# Co-Beneficiarios del socio
class CoBeneficiario(models.Model):
    parentesco_choices = (('C', 'Conyugue'), ('H', 'Hijo(a)'), ('T', 'Tio(a)'), ('A', 'Abuelo(a)'), ('O', 'Otro'))

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
        verbose_name = 'Co-Beneficiario'
        verbose_name_plural = 'Co-Beneficiarios'


# Categorias de Prestamos
class CategoriaPrestamo(models.Model):
    tipo_choices = (('OD', 'Orden de Despacho'), ('PR', 'Prestamo'), ('SC', 'SuperCoop'))

    descripcion = models.CharField(max_length=70)
    montoDesde = models.DecimalField("Monto Desde", max_digits=18, decimal_places=2, blank=True, null=True)
    montoHasta = models.DecimalField("Monto Hasta", max_digits=18, decimal_places=2, blank=True, null=True)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    interesAnualSocio = models.DecimalField("Intereses Anual Socio %", max_digits=6, decimal_places=2, null=True, blank=True)
	# interesAnualEmpleado = models.DecimalField("Intereses Anual Empleado %", max_digits=6, decimal_places=2, null=True, blank=True)
	# interesAnualDirectivo = models.DecimalField("Intereses Anual Directivo %", max_digits=6, decimal_places=2, null=True, blank=True)

    userLog = models.ForeignKey(User, editable=False)
    datetimeServer = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s' % (self.descripcion)

    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()

        super(CategoriaPrestamo, self).save(*args, **kwargs)

    class Meta:
        ordering = ['descripcion']
        verbose_name = 'Categoria de Prestamo/Orden'
        verbose_name_plural = 'Config 6.1) Categorias de Prestamos/Ordenes'


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


# Perfiles
class Perfil(models.Model):
    perfilCod = models.CharField("Codigo Perfil", max_length=15, unique=True)

    def __unicode__(self):
        return '%s' % (self.perfilCod)

    class Meta:
        ordering = ['perfilCod']
        verbose_name_plural = 'Config 3.4) Perfiles'


# Opciones
class Opcion(models.Model):
    tipo_choices = (('P', 'Principal'), ('S', 'Secundario'),)
    valor_choices = (('true', 'Deshabilitado'), ('false', 'Habilitado'),)

    descripcion = models.CharField(max_length=80)
    valor = models.CharField(max_length=5, choices=valor_choices, default='true')
    tipo = models.CharField(max_length=1, choices=tipo_choices, default='S')
    perfil = models.ForeignKey(Perfil)

    def __unicode__(self):
        return '%s' % (self.descripcion)

    class Meta:
        ordering = ['descripcion']
        verbose_name_plural = 'Config 3.3) Opciones'


# Autorizadores
class Autorizador(models.Model):
    usuario = models.ForeignKey(User, unique=True)
    perfil = models.ForeignKey(Perfil)
    clave = models.CharField(max_length=4)

    datetimeServer = models.DateTimeField(auto_now_add=True)

    @property
    def userName(self):
        return '%s' % self.usuario.username

    class Meta:
        ordering = ['usuario']
        verbose_name_plural = 'Config 3.1) Autorizadores'


# Tipos de Notas de Credito Globales
class TipoNCGlobal(models.Model):
    tipo_choices = (('1', 'NCG'), ('2', 'NCG2'),)

    tipo = models.CharField(max_length=1, choices=tipo_choices, default='')
    descripcion = models.CharField(max_length=150)
    cuenta = models.ForeignKey(Cuentas)


# Bancos
class Banco(models.Model):
    estatus_choices = (('A', 'Activo'), ('I', 'Inactivo'))

    codigo = models.CharField(max_length=25)
    nombre = models.CharField(max_length=100)
    digitoVerificador = models.CharField(max_length=1, default='8')
    codigoOperacion = models.CharField(max_length=2, default='22')
    estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')

    def __unicode__(self):
        return '%s - %s' % (self.codigo, self.nombre)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()

        super(Banco, self).save(*args, **kwargs)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = 'Config 2.1) Bancos'


# Periodos (Fiscales)
class Periodo(models.Model):
    estatus_choices = (('A', 'Activo'), ('C', 'Cerrado',))
    mes_choices = (
        ('01', 'Enero'), ('02', 'Febrero'),
        ('03', 'Marzo'), ('04', 'Abril'),
        ('05', 'Mayo'), ('06', 'Junio'),
        ('07', 'Julio'), ('08', 'Agosto'),
        ('09', 'Septiembre'), ('10', 'Octubre'),
        ('11', 'Noviembre'), ('12', 'Diciembre'),
    )

    mes = models.CharField(max_length=2, choices=mes_choices, default='01')
    agno = models.CharField("Agno", max_length=4)
    estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')

    def __unicode__(self):
        return '%s%s' % (self.mes, self.agno)

    class Meta:
        ordering = ['-agno']
        verbose_name_plural = 'Config 7.3) Periodos'


# Empresas
class Empresa(models.Model):
    estatus_choices = (('A', 'Activo'), ('I', 'Inactivo',))

    nombre = models.CharField(max_length=50)
    rnc = models.CharField(max_length=15, blank=True, null=True)
    cuentaBanco = models.CharField(max_length=1, null=True)
    bancoAsign = models.CharField(max_length=5, blank=True, null=True)
    correoHeader = models.CharField(max_length=40, blank=True, null=True)
    estatus = models.CharField(max_length=1, choices=estatus_choices, default='A')
    telefono = models.CharField(max_length=20, null=True, blank=True)

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


# UserExtra contiene datos agregados al usuario registrado,
# como la Localidad, perfil, entre otros.
class UserExtra(models.Model):
    usuario = models.ForeignKey(User)
    localidad = models.ForeignKey(Localidad)
    perfil = models.ForeignKey(Perfil)

    def __unicode__(self):
        return '%s - %s' % (self.usuario.username, self.localidad.descripcion)

    class Meta:
        ordering = ('usuario',)
        unique_together = ('usuario', 'localidad', 'perfil')


# Tipos de Documentos
class TipoDocumento(models.Model):
    codigo = models.CharField(max_length=4)
    descripcion = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s - %s' % (self.codigo, self.descripcion)

    def save(self, *args, **kwargs):
        self.codigo = self.codigo.upper()
        self.descripcion = self.descripcion.upper()

        super(TipoDocumento, self).save(*args, **kwargs)

    class Meta:
        ordering = ['descripcion']
        verbose_name_plural = 'Config 7.1) Tipos de Documentos'


# Asociacion de Documentos con Cuentas
class DocumentoCuentas(models.Model):
    accion_choices = (('D', 'Debito'), ('C', 'Credito'))

    documento = models.ForeignKey(TipoDocumento)
    cuenta = models.ForeignKey(Cuentas)
    accion = models.CharField(max_length=1, choices=accion_choices)

    def __unicode__(self):
        return '%s - %s (%s)' % (self.documento, self.cuenta, self.accion)

    @property
    def getCodigo(self):
        return self.documento.codigo

    @property
    def getCuentaCodigo(self):
        return self.cuenta.codigo

    @property
    def getCuentaDescrp(self):
        return self.cuenta.descripcion

    @property
    def getTipoSocio(self):
        return self.cuenta.tipoSocio

    class Meta:
        ordering = ['documento', 'cuenta']
        unique_together = ('documento', 'cuenta', 'accion')
        verbose_name = 'Documento relacionado a Cuentas'
        verbose_name_plural = 'Config 7.2) Documentos relacionados a Cuentas'


# Archivos para Banco
class ArchivoBanco(models.Model):
    bancoAsign = models.CharField("Numero Asignado a Empresa (desde el Banco)",
                                  max_length=5)  # Numero Asignado a la Empresa de cinco posiciones
    tipoServicio = models.CharField("Tipo Servicio (dos posiciones)",
                                    max_length=2)  # Tipo de Servicio de dos posiciones
    envio = models.CharField("Envio (MMDD)", max_length=4)  # MMDD mes y dia en que se envia el archivo
    secuencia = models.PositiveIntegerField("Secuencia (7 posiciones)",
                                            default=0)  # Secuencia del header de siete posiciones
    archivoNombre = models.CharField(max_length=25, null=True, blank=True)

    datetimeServer = models.DateTimeField(auto_now_add=True)
    userLog = models.ForeignKey(User, editable=False)

    def save(self, *args, **kwargs):
        self.archivoNombre = 'PE{0}{1}{2}{3}E.TXT'.format('{:0>5}'.format(self.bancoAsign), self.tipoServicio,
                                                          self.envio, '{:0>7}'.format(self.secuencia))

        super(ArchivoBanco, self).save(*args, **kwargs)


# Cabecera Contenido Archivo de Banco
class ArchivoBancoHeader(models.Model):
    tipoRegistro = models.CharField(max_length=1)  # = H
    idCompania = models.CharField(max_length=15)
    nombreCompania = models.CharField(max_length=35)
    secuencia = models.CharField(max_length=7)  # Secuencia del archivo generado
    tipoServicio = models.CharField(
        max_length=2)  # 01 = Nomina Automatica  --- 02 = Pago a Suplidores .... 06 = Transferencia a Cta.
    fechaEfectiva = models.CharField(max_length=8)  # YYYYMMDD (Fecha Futura cuando se aplican los Pagos)
    cantidadDB = models.CharField(max_length=11)  # Cantidad de Debitos
    montoTotalDB = models.CharField(max_length=13)  # Monto Total de Debitos
    cantidadCR = models.CharField(max_length=11)  # Cantidad Total de Creditos
    montoTotalCR = models.CharField(max_length=13)  # Monto Total de Creditos
    numeroAfiliacion = models.CharField(max_length=15, blank=True)  # Afiliacion a CARDNET
    fecha = models.CharField(max_length=8)  # YYYYMMDD (Fecha de envio del archivo)
    hora = models.CharField(max_length=4)  # HHMM del envio
    correo = models.CharField(max_length=40)  # Correo para recibir info del banco
    estatus = models.CharField(max_length=1, blank=True)  # Dejar vacio para el banco
    cuentaEmpresa = models.CharField(max_length=1)  # Numero de cuenta que empresa usara para DB/CR (1-9)
    filler = models.CharField(max_length=107, blank=True)  # Llenar con espacio en Blanco
    lineaFormateadaH = models.CharField(max_length=292, blank=True)  # Aqui ira la linea formateada para el TXT

    def save(self, *args, **kwargs):
        montoDB = str(self.montoTotalDB).replace('.', '').replace(',', '')[:13]
        montoCR = str(self.montoTotalCR).replace('.', '').replace(',', '')[:13]

        self.tipoRegistro = 'H'
        self.idCompania = '{:<15}'.format(self.idCompania)
        self.nombreCompania = '{:<35}'.format(self.nombreCompania)
        self.secuencia = '{:0>7}'.format(self.secuencia)
        self.tipoServicio = self.tipoServicio
        self.fechaEfectiva = self.fechaEfectiva
        self.cantidadDB = '{:0>11}'.format(self.cantidadDB)
        self.montoTotalDB = '{:0>13}'.format(int(montoDB))
        self.cantidadCR = '{:0>11}'.format(self.cantidadCR)
        self.montoTotalCR = '{:0>13}'.format(int(montoCR))
        self.numeroAfiliacion = '{:0>15}'.format(self.numeroAfiliacion)
        self.fecha = self.fecha
        self.hora = self.hora
        self.correo = '{:<40}'.format(self.correo)
        self.estatus = '{:<1}'.format(self.estatus)
        self.cuentaEmpresa = self.cuentaEmpresa
        self.filler = '{:<107}'.format(self.filler)
        self.lineaFormateadaH = self.tipoRegistro + \
                                self.idCompania + \
                                self.nombreCompania + \
                                self.secuencia + \
                                self.tipoServicio + \
                                self.fechaEfectiva + \
                                self.cantidadDB + \
                                self.montoTotalDB + \
                                self.cantidadCR + \
                                self.montoTotalCR + \
                                self.numeroAfiliacion + \
                                self.fecha + \
                                self.hora + \
                                self.correo + \
                                self.estatus + \
                                self.cuentaEmpresa + \
                                self.filler

        super(ArchivoBancoHeader, self).save(*args, **kwargs)


# Detalle Contenido Archivo de Banco -- Registro N
class ArchivoBancoDetailN(models.Model):
    tipoRegistro = models.CharField(max_length=1, blank=True, default='N')
    idCompania = models.CharField(max_length=15)
    secuencia = models.CharField(max_length=7)  # Secuencia del Header
    secuenciaTrans = models.CharField(max_length=7)  # Numero que identifica la transaccion en el archivo
    cuentaDestino = models.CharField(max_length=20)  # Justificada a la izquierda - del suplidor
    tipoCuentaDestino = models.CharField(max_length=1)
    monedaDestino = models.CharField(max_length=3, default='214')
    codBancoDestino = models.CharField(max_length=8, default='10101070')
    digiVerBancoDestino = models.CharField(max_length=1, default='8')
    codigoOperacion = models.CharField(max_length=2, default='22')
    montoTransaccion = models.CharField(max_length=13)
    tipoIdentificacion = models.CharField(max_length=2, default='CE')  # Debe ser llenado para el BANCO POPULAR
    identificacion = models.CharField(max_length=15)  # Debe ser llenado para el BANCO POPULAR
    nombre = models.CharField(max_length=35, default='')  # Nombre del Beneficiario o Cliente
    numeroReferencia = models.CharField(max_length=12, blank=True, default='')
    descrpEstadoDestino = models.CharField(max_length=40, blank=True, default='')
    fechaVencimiento = models.CharField(max_length=4, blank=True, default='')  # solo para Codigo de Operacion 57
    formaContacto = models.CharField(max_length=1, default=' ')
    emailBenef = models.CharField(max_length=40, blank=True, default='')  # requerido si el campo formaContacto = 1
    faxTelefonoBenef = models.CharField(max_length=12, blank=True,
                                        default='')  # Requerido si el campo formaContacto = 2 ó 3
    filler = models.CharField(max_length=2, default='00')
    numeroAut = models.CharField(max_length=15, blank=True, default='')  # Uso del banco
    codRetornoRemoto = models.CharField(max_length=3, default='   ')  # Uso del banco
    codRazonRemoto = models.CharField(max_length=3, default='   ')  # Uso del banco
    codRazonInterno = models.CharField(max_length=3, default='   ')  # Uso del banco
    procTransaccion = models.CharField(max_length=1, default=' ')  # Uso del banco
    estatusTransaccion = models.CharField(max_length=2, default=' ')  # Uso del banco
    filler2 = models.CharField(max_length=52, blank=True, default='')
    lineaFormateadaN = models.CharField(max_length=320, blank=True, )

    def save(self, *args, **kwargs):
        montoT = str(self.montoTransaccion).replace('.', '').replace(',', '')[:13]

        self.tipoRegistro = 'N'
        self.idCompania = '{:<15}'.format(self.idCompania)
        self.secuencia = '{:0>7}'.format(self.secuencia)
        self.secuenciaTrans = '{:0>7}'.format(self.secuenciaTrans)
        self.cuentaDestino = '{:>20}'.format(self.cuentaDestino)
        self.tipoCuentaDestino = self.tipoCuentaDestino
        self.monedaDestino = self.monedaDestino
        self.codBancoDestino = self.codBancoDestino
        self.digiVerBancoDestino = self.digiVerBancoDestino
        self.codigoOperacion = self.codigoOperacion
        self.montoTransaccion = '{:0>13}'.format(int(montoT))
        self.tipoIdentificacion = self.tipoIdentificacion
        self.identificacion = '{:<15}'.format(self.identificacion)
        self.nombre = '{:<35}'.format(self.nombre)
        self.numeroReferencia = '{:<12}'.format(self.numeroReferencia)
        self.descrpEstadoDestino = '{:<40}'.format(self.descrpEstadoDestino)
        self.fechaVencimiento = '{:<4}'.format(self.fechaVencimiento)
        self.formaContacto = self.formaContacto
        self.emailBenef = '{:<40}'.format(self.emailBenef)
        self.faxTelefonoBenef = '{:>0}'.format(self.faxTelefonoBenef)
        self.filler = self.filler
        self.numeroAut = '{:<}'.format(self.numeroAut)
        self.codRetornoRemoto = self.codRetornoRemoto
        self.codRazonRemoto = self.codRazonRemoto
        self.codRazonInterno = self.codRazonInterno
        self.procTransaccion = self.procTransaccion
        self.estatusTransaccion = self.estatusTransaccion
        self.filler2 = '{:<52}'.format(self.filler2)
        self.lineaFormateadaN = self.tipoRegistro + \
                                self.idCompania + \
                                self.secuencia + \
                                self.secuenciaTrans + \
                                self.cuentaDestino + \
                                self.tipoCuentaDestino + \
                                self.monedaDestino + \
                                self.codBancoDestino + \
                                self.digiVerBancoDestino + \
                                self.codigoOperacion + \
                                self.montoTransaccion + \
                                self.tipoIdentificacion + \
                                self.identificacion + \
                                self.nombre + \
                                self.numeroReferencia + \
                                self.descrpEstadoDestino + \
                                self.fechaVencimiento + \
                                self.formaContacto + \
                                self.emailBenef + \
                                self.faxTelefonoBenef + \
                                self.filler + \
                                self.numeroAut + \
                                self.codRetornoRemoto + \
                                self.codRazonRemoto + \
                                self.codRazonInterno + \
                                self.procTransaccion + \
                                self.estatusTransaccion + \
                                self.filler2

        super(ArchivoBancoDetailN, self).save(*args, **kwargs)


# Detalle Contenido Archivo de Banco -- Registro R
class ArchivoBancoDetailR(models.Model):
    tipoRegistro = models.CharField(max_length=1, default='R')
    idCompania = models.CharField(max_length=15)
    secuencia = models.CharField(max_length=7)  # Secuencia del Header
    secuenciaTrans = models.CharField(max_length=7)  # Secuencia de la Transaccion N
    numeroCtaDestino = models.CharField(max_length=20)  # Justificada a la izquierda Suplidor
    numeroDocumento = models.CharField(max_length=15)  # Numero del Documento
    tipoDocumento = models.CharField(max_length=2)  # 00 Facturas --- 01 Nota de Creditos --- 02 Nota de Debitos
    fechaDocumento = models.CharField(max_length=8)  # Fecha del Documento YYYYMMDD
    montoDocumento = models.CharField(max_length=13)  # Monto del Documento (Bruto)
    montoDescuento = models.CharField(max_length=11)  # Monto Descuento
    montoImpuesto = models.CharField(max_length=11)  # Monto Impuesto
    netoDocumento = models.CharField(max_length=13)  # Monto Neto del Documento
    descripcion = models.CharField(max_length=50)  # Descripcion del Documento
    filler = models.CharField(max_length=146, blank=True)
    lineaFormateadaR = models.CharField(max_length=319)

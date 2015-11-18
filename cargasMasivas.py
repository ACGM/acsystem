#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, csv

#CARGA DE CUOTAS DE ORDENES
f = open('CuotasOrdenes.csv', 'r')
for line in f:
	line = line.split(',')
	c = CuotaOrdenes()
	c.montoDesde = line[0]
	c.montoHasta = line[1]
	c.cantidadQuincenas = line[2]
	c.userLog = User.objects.get(username='coop')
	c.save()
f.close()

#CARGA DE CUOTAS DE PRESTAMOS
f = open('CuotasPrestamos.csv', 'r')
for line in f:
	line = line.split(',')
	c = CuotaPrestamo()
	c.montoDesde = line[0]
	c.montoHasta = line[1]
	c.cantidadQuincenas = line[2]
	c.userLog = User.objects.get(username='coop')
	c.save()
f.close()

#CARGA DE CATEGORIAS DE PRODUCTOS
f = open('CategoriaProductos.csv', 'r')
for line in f:
	catP = CategoriaProducto()
	descripcion = line.decode('latin-1').encode('utf-8')
	catP.descripcion = descripcion.strip()
	catP.save()
f.close()

#CARGA DE PRODUCTOS
f = open('Productos.csv', 'r')
for line in f:
	line = line.split(',')
	producto = Producto()
	categoria = line[2].decode('latin-1').encode('utf-8')
	producto.descripcion = line[0].decode('latin-1')
	producto.unidad = Unidad.objects.get(id=1)
	producto.categoria = CategoriaProducto.objects.get(descripcion=categoria.strip())
	producto.precio = line[3]
	producto.costo = line[4]
	producto.userLog = User.objects.get(username='coop')
	producto.save()
f.close()

#CARGA DE DEPARTAMENTOS
f = open('Departamentos.csv', 'r')
for line in f:
	line = line.split(',')
	depto = Departamento()
	depto.centroCosto = line[0]
	depto.descripcion = line[1].decode('latin-1').strip()
	depto.save()
f.close()

#CARGA DE CUENTAS CONTROL
f = open('ctactrlOf.csv', 'r')
for line in f:
	line = line.split(',')
	cc = CuentasControl()
	cc.codigoControl = line[0]
	cc.descripcion = line[1].decode('latin-1').strip()
	cc.save()
f.close()

#CARGA DE CUENTAS (CATALOGO)
	# if line[2] != '': cuenta.cuentaControl = CuentasControl.objects.get(codigoControl=line[2].decode('latin-1').strip())
# f = open('CatalogoCuentas.csv', 'r')
f = open('cuentasOf.csv', 'r')
for line in f:
	line = line.split(',')
	cuenta = Cuentas()
	cuenta.codigo = line[0]
	cuenta.descripcion = line[1].decode('latin-1').strip()
	cuenta.origen = line[2].decode('latin-1').strip()
	cuenta.tipo = line[3].decode('latin-1').strip()
	cuenta.control = True if line[4].strip() == '1' else False
	cuenta.tipoSocio = line[5]
	cuenta.nivel = line[6].strip()
	cuenta.cuentaControl = None if line[8].strip() == 'x' else CuentasControl.objects.get(id=int(line[8].strip()))
	# print CuentasControl.objects.get(id=line[8].strip()) if line[8].strip != 'x' else None
	cuenta.save()
f.close()

#CARGA DE CATEGORIAS DE ORDENES
f = open('CategoriasOrdenes.csv', 'r')
for line in f:
	line = line.split(',')
	categPrest = CategoriaPrestamo()
	categPrest.descripcion = line[0].decode('latin-1').strip()
	categPrest.montoDesde = 1
	categPrest.montoHasta = 500000
	categPrest.tipo = 'OD'
	categPrest.interesAnualSocio = 18
	categPrest.userLog = User.objects.get(username='coop')
	categPrest.save()
f.close()

#CARGA DE CATEGORIAS DE PRESTAMOS
f = open('CategoriasPrestamos.csv', 'r')
for line in f:
	line = line.split(',')
	categPrest = CategoriaPrestamo()
	categPrest.descripcion = line[0].decode('latin-1').strip()
	categPrest.montoDesde = 1
	categPrest.montoHasta = 500000
	categPrest.tipo = 'PR'
	categPrest.interesAnualSocio = 5
	categPrest.userLog = User.objects.get(username='coop')
	categPrest.save()
f.close()

#CARGA DE SUPLIDORES (Ordenes Despacho)
f = open('SuplidoresOD.csv', 'r')
for line in f:
	line = line.split('|')
	suplidor = Suplidor()
	suplidor.nombre = line[1].decode('latin-1').strip()
	suplidor.contacto = line[2].decode('latin-1').strip()
	suplidor.telefono = line[3].decode('latin-1').strip()
	suplidor.fax = line[4].decode('latin-1').strip()
	suplidor.clase = 'N'
	suplidor.userLog = User.objects.get(username='coop')
	suplidor.save()
f.close()

#CARGA DE SUPLIDORES (Supercoop)
f = open('SuplidoresSuperCoop.csv', 'r')
for line in f:
	line = line.split('|')
	suplidor = Suplidor()
	suplidor.nombre = line[1].decode('latin-1').strip()
	suplidor.contacto = line[2].decode('latin-1').strip()
	suplidor.clase = 'S'
	# suplidor.telefono = line[2].decode('latin-1').strip()
	# suplidor.contacto = line[3].decode('latin-1').strip()
	suplidor.userLog = User.objects.get(username='coop')
	suplidor.save()
f.close()

import decimal
f = open('Balanza.csv','r')
for line in f:
	line = line.split(',')
	balance = BalanceCuenta()
	balance.agno = 2015
	balance.mes =10
	balance.cuenta = Cuentas.objects.get(codigo=line[0])
	balance.Balance = decimal.Decimal(line[1])
	balance.save()
f.close()

import decimal
import datetime
f = open('diario.csv','r')
for line in f:
	line = line.split(',')
	diario = DiarioGeneral()
	diario.fecha = datetime.now()
	diario.cuenta = Cuentas.objects.get(codigo=line[0])
	diario.referencia = line[1]
	diario.estatus ='P'
	diario.debito = decimal.Decimal(line[2])
	diario.credito = decimal.Decimal(line[3])
	diario.save()

f.close()


#CARGA DE SOCIOS
f = open('Socios.csv', 'r')
for line in f:
	line = line.split(',')
	socio = Socio()
	depto = Departamento.objects.get(centroCosto=line[7].strip()) 
	socio.codigo = line[0].decode('latin-1')
	socio.nombres = line[1].decode('latin-1')
	socio.apellidos = line[2].decode('latin-1')
	socio.sexo = 'M' if line[3].decode('latin-1') == '1' else 'F'
	socio.estadoCivil = 'S' if line[4] == 'Soltero' else 'Casado'
	socio.fechaIngresoCoop = line[5].decode('latin-1').replace('.','-')
	socio.fechaIngresoEmpresa = line[6].decode('latin-1').replace('.','-')
	socio.departamento = depto
	socio.localidad = Localidad.objects.get(descripcion=line[8].strip())
	socio.estatus = 'S' if line[9] == 'Socio' else 'E'
	socio.cuotaAhorroQ1 = line[10]
	socio.cuotaAhorroQ2 = line[11]
	socio.cuentaBancaria = line[12]
	socio.tipoCuentaBancaria = line[13]
	socio.salario = line[14]
	socio.direccion = line[15].decode('lation-1').strip()
	socio.telefono = line[16].strip()
	socio.correo = line[17].strip()
	socio.userLog = User.objects.get(username='coop')
	socio.save()

f.close


#Asignar atributo para cuentas que son CONTROL
for cc in CuentasControl.objects.all():
	try:
		c = Cuentas.objects.get(codigo=cc.codigoControl)
		c.control = True
		c.cuentaControl = cc
		c.save()
	except cc.DoesNotExist:
		pass


#Carga TIPOS DE DOCUMENTOS
f = open('tiposdocs.csv', 'r')
for line in f:
	line = line.split(',')
	td = TipoDocumento()
	td.codigo = line[0].decode('latin-1').strip()
	td.descripcion = line[1].decode('latin-1').strip()
	td.save()
f.close()


#Carga ACTIVOS
f = open('activos.csv', 'r')
for line in f:
	line = line.split(',')
	a = Activos()
	a.descripcion = line[1].decode('latin-1').strip()
	a.categoria = CategoriaActivo.objects.get(id=line[2].strip())
	a.fechaAdd = line[3].strip()
	a.fechaDep = line[4].strip()
	a.agnosVu = line[5].strip()
	a.costo = line[6].strip()
	a.localidad = Localidad.objects.get(id=line[7].strip())
	a.factura = line[9].strip()
	a.estatus = line[10].strip()
	a.porcentaje = line[11].strip()
	a.save()
f.close()



#Carga DEPRESIACION DE ACTIVOS
f = open('depresiacion.csv', 'r')
for line in f:
	line = line.split(',')
	d = Depresiacion()
	d.activoId = line[0].strip()
	d.fecha = line[5].strip()
	d.dMensual = line[1].strip()
	d.dAcumulada = line[2].strip()
	d.dAgno = line[3].strip()
	d.vLibro = line[4].strip()
	d.save()
f.close()


#Documentos RELACIONADOS con cuentas
f = open('doccta.csv', 'r')
for line in f:
	line = line.split('-')
	drc = DocumentoCuentas()
	drc.documento = TipoDocumento.objects.get(codigo=line[0].decode('latin-1').strip())
	drc.cuenta = Cuentas.objects.get(codigo=line[1].decode('latin-1').strip())
	drc.accion = line[2].decode('latin-1').strip()
	drc.save()
f.close()

import decimal
import datetime
#Prestamos a la fecha
f = open('prestamoslimpio.csv', 'r')
for line in f:
	line = line.split(',')
	p = SolicitudPrestamo()
	p.noSolicitud = SolicitudPrestamo.objects.latest('noSolicitud').noSolicitud +1
	p.socio = Socio.objects.get(codigo=line[0].strip())
	p.montoSolicitado = decimal.Decimal(line[1].strip().replace(',',''))
	p.netoDesembolsar = decimal.Decimal(line[1].strip().replace(',',''))
	p.categoriaPrestamo = CategoriaPrestamo.objects.get(descripcion=line[2].decode('latin-1').strip())
	p.tasaInteresAnual = line[3].strip()
	p.tasaInteresMensual = line[4].strip()
	p.cantidadCuotas = line[5].strip()
	p.valorCuotasCapital = line[6].strip()
	p.localidad = Localidad.objects.get(descripcion=line[7].strip())
	p.representante = Representante.objects.get(estatus='A')
	p.cobrador = Cobrador.objects.get(usuario='coop')
	p.autorizadoPor = User.objects.get(username='coop')
	p.userLog = User.objects.get(username='coop')
	p.fechaParaDescuento = datetime.datetime.now()
	p.save()
f.close()
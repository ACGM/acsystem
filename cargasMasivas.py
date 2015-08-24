#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, csv

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
f = open('CuentasControl.csv', 'r')
for line in f:
	line = line.split(',')
	cc = CuentasControl()
	cc.codigoControl = line[0]
	cc.descripcion = line[1].decode('latin-1').strip()
	cc.save()
f.close()

#CARGA DE CUENTAS (CATALOGO)
f = open('CatalogoCuentas.csv', 'r')
for line in f:
	line = line.split(',')
	cuenta = Cuentas()
	cuenta.codigo = line[0]
	cuenta.descripcion = line[1].decode('latin-1').strip()
	if line[2] != '': cuenta.cuentaControl = CuentasControl.objects.get(codigoControl=line[2].decode('latin-1').strip())
	cuenta.origen = line[3].decode('latin-1').strip()
	cuenta.tipo = line[4].decode('latin-1').strip()
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
	line = line.split(',')
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
	line = line.split(',')
	suplidor = Suplidor()
	suplidor.nombre = line[1].decode('latin-1').strip()
	suplidor.contacto = line[2].decode('latin-1').strip()
	suplidor.clase = 'S'
	# suplidor.telefono = line[2].decode('latin-1').strip()
	# suplidor.contacto = line[3].decode('latin-1').strip()
	suplidor.userLog = User.objects.get(username='coop')
	suplidor.save()
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
	socio.sexo = 'M' if line[3].decode('latin-1') == 1 else 'F'
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
	socio.userLog = User.objects.get(username='coop')
	socio.save()

f.close
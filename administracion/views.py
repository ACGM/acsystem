# VIEWS de Administracion

from django.conf import settings
from django.core.files import File
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponse

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from prestamos.models import MaestraPrestamo

from .serializers import ProductoSerializer, SuplidorTipoSerializer, SuplidorSerializer, \
						SocioSerializer, DepartamentoSerializer, CoBeneficiarioSerializer, \
						ListadoCategoriaPrestamoSerializer, CantidadCuotasPrestamosSerializer, \
						AutorizadoresSerializer, EmpresasSerializer, RepresentantesSerializer, \
						CategoriasProductosSerializer, CantidadCuotasODSerializer, DocumentoCuentasSerializer


from .models import Producto, Suplidor, TipoSuplidor, Socio, Departamento, CoBeneficiario, \
					CategoriaPrestamo, CuotaPrestamo, CuotaOrdenes, Autorizador, Empresa, \
					CategoriaProducto, Representante, Banco, ArchivoBanco, ArchivoBancoHeader, \
					ArchivoBancoDetailN, DocumentoCuentas

import json
import datetime

# Productos Busqueda (GENERICO)
def productosSearch(request):
	return render(request, 'productos_search.html')


# Productos Busqueda (GENERICO) - con Precio
def productosSearch2(request):
	return render(request, 'productos_search2.html')


class ProductoViewSet(viewsets.ModelViewSet):
	queryset = Producto.objects.all().order_by('descripcion')
	serializer_class = ProductoSerializer


class CategoriaProductoViewSet(viewsets.ModelViewSet):
	queryset = CategoriaProducto.objects.all().order_by('descripcion')
	serializer_class = CategoriasProductosSerializer


class SuplidorTipoViewSet(viewsets.ModelViewSet):
	queryset = TipoSuplidor.objects.all()
	serializer_class = SuplidorTipoSerializer


class SuplidorViewSet(viewsets.ModelViewSet):
	queryset = Suplidor.objects.all().order_by('nombre')
	serializer_class = SuplidorSerializer


class SocioViewSet(viewsets.ModelViewSet):
	queryset = Socio.objects.all().order_by('nombreCompleto')
	serializer_class = SocioSerializer


class DepartamentoViewSet(viewsets.ModelViewSet):
	queryset = Departamento.objects.all()
	serializer_class = DepartamentoSerializer


class CoBeneficiarioViewSet(viewsets.ModelViewSet):
	queryset = CoBeneficiario.objects.all()
	serializer_class = CoBeneficiarioSerializer


# Categorias de Prestamos
class ListadoCategoriasPrestamosViewSet(viewsets.ModelViewSet):

	queryset = CategoriaPrestamo.objects.all()
	serializer_class = ListadoCategoriaPrestamoSerializer


# Autorizadores
class AutorizadoresViewSet(viewsets.ModelViewSet):

	queryset = Autorizador.objects.all()
	serializer_class = AutorizadoresSerializer


# Empresas
class EmpresasViewSet(viewsets.ModelViewSet):

	queryset = Empresa.objects.all()
	serializer_class = EmpresasSerializer


# Representantes
class RepresentantesViewSet(viewsets.ModelViewSet):

	queryset = Representante.objects.all()
	serializer_class = RepresentantesSerializer


# Consultar un socio en especifico
class SocioByCodigoView(APIView):

	serializer_class = SocioSerializer

	def get(self, request, codigo):
		
		socio = Socio.objects.filter(codigo=codigo)

		response = self.serializer_class(socio, many=True)
		return Response(response.data)


# Documentos Relacionados a Cuentas
class DocumentoCuentasView(APIView):

	serializer_class = DocumentoCuentasSerializer

	def get(self, request, doc=None):
		
		docCuentas = DocumentoCuentas.objects.filter(documento__codigo=doc)

		response = self.serializer_class(docCuentas, many=True)
		return Response(response.data)


# Categoria de Prestamo por Descripcion
class CategoriaPrestamoByDescrpView(APIView):

	serializer_class = ListadoCategoriaPrestamoSerializer

	def get(self, request, descrp=None,):
		
		categorias = CategoriaPrestamo.objects.filter(descripcion__contains=descrp)

		response = self.serializer_class(categorias, many=True)
		return Response(response.data)


# Cantidad de Cuotas (parametro: Monto)
class CantidadCuotasPrestamosView(APIView):

	serializer_class = CantidadCuotasPrestamosSerializer

	def get(self, request, monto=None):
		
		monto = CuotaPrestamo.objects.filter(montoDesde__lte=monto, montoHasta__gte=monto)

		response = self.serializer_class(monto, many=True)
		return Response(response.data)


# Cantidad de Cuotas (parametro: Monto)
class CantidadCuotasODView(APIView):

	serializer_class = CantidadCuotasODSerializer

	def get(self, request, monto=None):
		
		monto = CuotaOrdenes.objects.filter(montoDesde__lte=monto, montoHasta__gte=monto)

		response = self.serializer_class(monto, many=True)
		return Response(response.data)


# Suplidor por Nombre
class SuplidorByNombreView(APIView):

	serializer_class = SuplidorSerializer

	def get(self, request, nombre=None):
		if nombre != None:
			suplidores = Suplidor.objects.filter(nombre__contains=nombre, estatus='A').order_by('nombre')
		else:
			suplidores = Suplidor.objects.filter(estatus='A')

		response = self.serializer_class(suplidores, many=True)
		return Response(response.data)


# Producto por Descripcion
class ProductoByDescrpView(APIView):

	serializer_class = ProductoSerializer

	def get(self, request, descrp=None):
		if descrp != None:
			productos = Producto.objects.filter(descripcion__contains=descrp).order_by('descripcion')
		else:
			productos = Producto.objects.all()

		response = self.serializer_class(productos, many=True)
		return Response(response.data)


#Generar Archivo para Banco
class GenerarArchivoBancoView(View):

	def post(self, request, *args, **kwargs):

		try:
			nombreArchivoFinal = ''
			contenidoArchivoFinal = ''

			data = json.loads(request.body)

			headerArchivo = data['CABECERA']
			registrosN = data['DETALLE']

			# Banco
			banco = Banco.objects.get(estatus='A')
			# Empresa
			empresa = Empresa.objects.get(estatus='A')
			# Archivo Banco
			archivoB = ArchivoBanco()
			archivoB.bancoAsign = empresa.bancoAsign
			archivoB.tipoServicio = headerArchivo['tipoServicio']
			archivoB.envio = '{:0>2}'.format(str(datetime.datetime.now().month)) + \
							'{:0>2}'.format(str(datetime.datetime.now().day))
			archivoB.secuencia = ArchivoBanco.objects.latest('secuencia').secuencia + 1
			archivoB.userLog = User.objects.get(username=request.user.username)
			archivoB.save()

			nombreArchivoFinal = archivoB.archivoNombre #El nombre del archivo que sera creado (.txt)
			pathFile = open(settings.ARCHIVOS_BANCO + nombreArchivoFinal, 'wb+')
			sysFile = File(pathFile)

			# Preparar cabecera de archivo de Banco
			aCabecera = ArchivoBancoHeader()
			aCabecera.idCompania = empresa.bancoAsign
			aCabecera.nombreCompania = empresa.nombre
			aCabecera.secuencia = archivoB.secuencia
			aCabecera.tipoServicio = headerArchivo['tipoServicio']
			aCabecera.fechaEfectiva = headerArchivo['fechaEfectiva']
			aCabecera.cantidadDB = headerArchivo['cantidadDB']
			aCabecera.montoTotalDB = headerArchivo['montoTotalDB']
			aCabecera.cantidadCR = headerArchivo['cantidadCR']
			aCabecera.montoTotalCR = headerArchivo['montoTotalCR']
			aCabecera.numeroAfiliacion = headerArchivo['numeroAfiliacion']
			aCabecera.fecha = headerArchivo['fechaEnvio']
			aCabecera.hora = headerArchivo['horaEnvio']
			aCabecera.correo = empresa.correoHeader
			aCabecera.cuentaEmpresa = empresa.cuentaBanco
			aCabecera.save()

			sysFile.write(aCabecera.lineaFormateadaH) # Escribir la linea de header en el archivo .TXT

			# Preparar el detalle del archivo de Banco
			icount = 0
			for linea in registrosN:
				if linea['socioCodigo'] != None:
					socio = Socio.objects.get(codigo=linea['socioCodigo']) #Consultar Socio para buscar detalles bancarios sobre el.
				else:
					suplidor = Suplidor.objects.get(id=linea['SuplidorId']) #Consultar Suplidor para buscar detalles bancarios sobre el.

				icount += 1
				registro = ArchivoBancoDetailN()
				registro.idCompania = aCabecera.idCompania
				registro.secuencia = aCabecera.secuencia
				registro.secuenciaTrans = icount
				registro.cuentaDestino = linea['cuentaDestino']
				registro.tipoCuentaDestino = socio.tipoCuentaBancaria if linea['socioCodigo'] != None else suplidor.tipoCuentaBancaria
				registro.monedaDestino = linea['monedaDestino']
				registro.codBancoDestino = banco.codigo
				registro.digiVerBancoDestino = banco.digitoVerificador
				registro.codigoOperacion = banco.codigoOperacion
				registro.montoTransaccion = linea['montoTransaccion']
				registro.tipoIdentificacion = 'CE' if linea['socioCodigo'] != None else suplidor.tipoIdentificacion
				registro.identificacion = socio.cedula if linea['socioCodigo'] != None else suplidor.identificacion
				registro.nombre = socio.nombreCompleto if linea['socioCodigo'] != None else '{0} {1}'.format(suplidor.nombres, suplidor.apellidos)
				registro.numeroReferencia = linea['numeroReferencia'] if linea.has_key('numeroReferencia') else ''
				registro.descrpEstadoDestino = linea['descrpEstadoDestino'] if linea.has_key('descrpEstadoDestino') else ''
				registro.fechaVencimiento = linea['fechaVencimiento'] if linea.has_key('fechaVencimiento') else ''
				registro.formaContacto = linea['formaContacto'] if linea.has_key('formaContacto') else ''
				registro.emailBenef = linea['emailBenef'] if linea.has_key('emailBenef') else ''
				registro.faxTelefonoBenef = linea['faxTelefonoBenef'] if linea.has_key('faxTelefonoBenef') else ''
				registro.save()

				sysFile.write(registro.lineaFormateadaN) # Escribir registro N en el archivo .TXT

				#Estas lineas son exclusiva para desembolso de prestamos (actualizacion en la MaestraPrestamo)
				if linea.has_key('prestamoNo'):
					m = MaestraPrestamo.objects.get(noPrestamo=linea['prestamoNo'])
					m.fechaDesembolso = datetime.date.today()
					m.usuarioDesembolso = request.user
					m.save()

			sysFile.close()


			# PENDIENTE -- Implementacion de Registros R -> para pago a Suplidores

			return HttpResponse(nombreArchivoFinal)

		except Exception as e:
			return HttpResponse(e)

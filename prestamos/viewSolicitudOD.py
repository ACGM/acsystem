# VIEWS de Solicitud de Prestamo

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, JsonResponse
from django.db import transaction

from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SolicitudesPrestamosSerializer, SolicitudesOrdenesDespachoSerializer

from .models import SolicitudOrdenDespachoH, SolicitudOrdenDespachoD, MaestraPrestamo
from administracion.models import CategoriaPrestamo, Cobrador, Representante, Socio, Autorizador, UserExtra, Suplidor
from facturacion.models import Factura

from acgm.views import LoginRequiredMixin

import json
import math
import decimal
import datetime


#Vista para Solicitud de Ordenes de Despacho
class SolicitudOrdenDespachoView(LoginRequiredMixin, TemplateView):

	template_name = 'solicitudordendespacho.html'

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			solicitante = data['solicitante']
			solicitud = data['solicitud']
			fechaSolicitud = data['fechaSolicitud']
			fechaDescuento = data['fechaDescuento']

			solicitudNo = solicitud['solicitudNo']

			socio = Socio.objects.get(codigo=solicitante['codigoEmpleado'])
			cobrador = Cobrador.objects.get(userLog=User.objects.get(username=solicitante['cobrador']))
			
			try:
				representante = Representante.objects.get(id=solicitante['representanteCodigo'])
			except Representante.DoesNotExist:
				representante = Representante.objects.get(estatus='A')

			categoriaPrest = CategoriaPrestamo.objects.get(id=solicitud['categoriaPrestamoId'])

			if solicitud['idSuplidor'] == -1:
				suplidor = Suplidor.objects.get(nombre='SUPERCOOP')
			else:
				suplidor = Suplidor.objects.get(id=solicitud['idSuplidor'])

			if solicitudNo > 0:
				SolOrdenDespacho = SolicitudOrdenDespachoH.objects.get(noSolicitud=solicitudNo)
			else:
				try:
					SolOrdenDespacho = SolicitudOrdenDespachoH()
					SolOrdenDespacho.noSolicitud = SolicitudOrdenDespachoH.objects.latest('noSolicitud').noSolicitud + 1
				except SolOrdenDespacho.DoesNotExist:
					SolOrdenDespacho.noSolicitud = 1

			SolOrdenDespacho.socio = socio
			SolOrdenDespacho.fechaSolicitud = fechaSolicitud
			SolOrdenDespacho.salarioSocio = socio.salario
			# SolOrdenDespacho.salarioSocio = decimal.Decimal(solicitante['salario'].replace(',','')) if solicitante['salario'] != None else 0
			SolOrdenDespacho.representante = representante
			SolOrdenDespacho.autorizadoPor = User.objects.get(username=request.user.username)
			SolOrdenDespacho.cobrador = cobrador

			SolOrdenDespacho.montoSolicitado = decimal.Decimal(solicitud['montoSolicitado'].replace(',',''))

			SolOrdenDespacho.ahorrosCapitalizados = decimal.Decimal(solicitud['ahorrosCapitalizados'].replace(',','')) if solicitud['ahorrosCapitalizados'] != None else 0
			SolOrdenDespacho.deudasPrestamos = decimal.Decimal(solicitud['deudasPrestamos'].replace(',','')) if solicitud['deudasPrestamos'] != None else 0
			SolOrdenDespacho.prestacionesLaborales = decimal.Decimal(solicitud['prestacionesLaborales'].replace(',','')) if solicitud['prestacionesLaborales'] != None else 0
			SolOrdenDespacho.valorGarantizado = decimal.Decimal(solicitud['valorGarantizado'].replace(',','')) if solicitud['valorGarantizado'] != None else 0
			SolOrdenDespacho.netoDesembolsar = decimal.Decimal(solicitud['netoDesembolsar'].replace(',',''))
			SolOrdenDespacho.observacion = solicitud['nota']
			SolOrdenDespacho.categoriaPrestamo = categoriaPrest
			SolOrdenDespacho.suplidor = suplidor
			SolOrdenDespacho.fechaParaDescuento = fechaDescuento
			SolOrdenDespacho.factura = solicitud['factura'] if solicitud.has_key('factura') else 0

			SolOrdenDespacho.tasaInteresAnual = decimal.Decimal(solicitud['tasaInteresAnual']) if solicitud['tasaInteresAnual'] > 0 else 0
			SolOrdenDespacho.tasaInteresMensual = decimal.Decimal(solicitud['tasaInteresMensual'])
			SolOrdenDespacho.cantidadCuotas = solicitud['cantidadCuotas']
			SolOrdenDespacho.valorCuotasCapital = decimal.Decimal(solicitud['valorCuotas'].replace(',',''))

			SolOrdenDespacho.localidad = UserExtra.objects.get(usuario__username=request.user.username).localidad
			SolOrdenDespacho.userLog = User.objects.get(username=request.user.username)

			SolOrdenDespacho.save()

			if SolOrdenDespacho.factura > 0:
				SolOrdenDespacho.cxp = 'P'
				SolOrdenDespacho.save()
				
				fact = Factura.objects.get(noFactura=SolOrdenDespacho.factura)
				fact.ordenCompra = SolOrdenDespacho.noSolicitud
				fact.save()

			return HttpResponse(SolOrdenDespacho.noSolicitud)

		except Exception as e:
			return HttpResponse(e)


#Vista para guardar Detalle de solicitud de Orden de Despacho
class SolicitudOrdenDespachoDetalleView(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			articulos = data['articulos']
			solicitudNo = data['solicitudNo']
			solHeader = SolicitudOrdenDespachoH.objects.get(noSolicitud=solicitudNo)

			try:
				SolicitudOrdenDespachoD.objects.filter(ordenDespacho=solHeader).delete()
			except SolicitudOrdenDespachoD.DoesNotExist:
				pass

			for item in articulos:
				detalle = SolicitudOrdenDespachoD()
				detalle.ordenDespacho = solHeader
				detalle.articulo = item['articulo']
				detalle.cantidad = item['cantidad']
				detalle.precio = item['precio']
				detalle.descuento = item['descuento']
				detalle.save()

			return HttpResponse(1)

		except Exception as e:
			return HttpResponse(e)


# Aprobar/Rechazar solicitudes de Ordenes de Despacho
class AprobarRechazarSolicitudesODView(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):

		with transaction.atomic():

			try:
				data = json.loads(request.body)

				solicitudes = data['solicitudes']
				accion = data['accion']

				for solicitud in solicitudes:
					oSolicitud = SolicitudOrdenDespachoH.objects.get(noSolicitud=solicitud['noSolicitud'])
					
					#Si la Orden de Despacho no tiene detalle digitado no puede ser aprobada
					try:
						SolicitudOrdenDespachoD.objects.filter(ordenDespacho=oSolicitud)
					except SolicitudOrdenDespachoD.DoesNotExist:
						raise Exception('La Solicitud No. ' + '{:0>8}'.format(oSolicitud.noSolicitud) + ' no tiene detalle digitado.')

					oSolicitud.estatus = accion
					oSolicitud.fechaAprobacion = datetime.datetime.now() if accion == 'A' else None
					oSolicitud.fechaRechazo = datetime.datetime.now() if accion == 'R' or accion == 'C' else None
					oSolicitud.aprobadoRechazadoPor = request.user
					oSolicitud.save()

					#Crear prestamo en la maestra de prestamos si es APROBADO
					if oSolicitud.estatus == 'A':

						try:
							maestra = MaestraPrestamo()
							maestra.noPrestamo = MaestraPrestamo.objects.latest('noPrestamo').noPrestamo + 1
						except MaestraPrestamo.DoesNotExist:
							maestra.noPrestamo = 1

						maestra.noSolicitudOD = oSolicitud
						maestra.categoriaPrestamo = oSolicitud.categoriaPrestamo
						maestra.socio = oSolicitud.socio
						maestra.representante = oSolicitud.representante
						maestra.oficial = User.objects.get(username=oSolicitud.cobrador.userLog.username)
						maestra.localidad = oSolicitud.localidad
						maestra.montoInicial = oSolicitud.netoDesembolsar
						maestra.tasaInteresAnual = oSolicitud.tasaInteresAnual
						maestra.tasaInteresMensual = oSolicitud.tasaInteresMensual
						maestra.pagoPrestamoAnterior = 0
						maestra.cantidadCuotas = oSolicitud.cantidadCuotas
						maestra.montoCuotaQ1 = oSolicitud.valorCuotasCapital
						maestra.montoCuotaQ2 = oSolicitud.valorCuotasCapital
						maestra.valorGarantizado = oSolicitud.valorGarantizado
						maestra.balance = oSolicitud.netoDesembolsar
						maestra.userLog = request.user

						maestra.save()

						#Guardar No. de Prestamo en la Solicitud
						oSolicitud.prestamo = maestra.noPrestamo
						oSolicitud.save()

				return HttpResponse(1)

			except Exception as e:
				return HttpResponse(e)


# Listado de Solicitudes de Ordenes de Despacho Por Codigo de Socio
class SolicitudesODAPIViewByCodigoNombre(APIView):

	serializer_class = SolicitudesOrdenesDespachoSerializer

	def get(self, request, codigo=None, nombre=None):
		if codigo != None:
			solicitudes = SolicitudOrdenDespachoH.objects.filter(socio__codigo=codigo).order_by('-noSolicitud')
		else:
			solicitudes = SolicitudOrdenDespachoH.objects.filter(socio__nombreCompleto__contains=nombre).order_by('-noSolicitud')

		response = self.serializer_class(solicitudes, many=True)
		return Response(response.data)


# Listado de Solicitudes de Ordenes de Despacho
class SolicitudesODAPIView(APIView):

	serializer_class = SolicitudesOrdenesDespachoSerializer

	def get(self, request, solicitud=None):
		if solicitud != None:
			solicitudes = SolicitudOrdenDespachoH.objects.filter(noSolicitud=solicitud)
		else:
			solicitudes = SolicitudOrdenDespachoH.objects.all().order_by('-noSolicitud')

		response = self.serializer_class(solicitudes, many=True)
		return Response(response.data)


# Desglose de Solicitud de Orden de Despacho
class SolicitudODById(LoginRequiredMixin, DetailView):

	queryset = SolicitudOrdenDespachoH.objects.all()

	def get(self, request, *args, **kwargs):
		NoSolicitud = self.request.GET.get('nosolicitud')

		self.object_list = self.get_queryset().filter(noSolicitud=NoSolicitud)

		format = self.request.GET.get('format')
		if format == 'json':
			return self.json_to_response()

		context = self.get_context_data()
		return self.render_to_response(context)

	def json_to_response(self):
		data = list()

		for solicitud in self.object_list:
			data.append({
				'noSolicitud': solicitud.noSolicitud,
				'fechaSolicitud': solicitud.fechaSolicitud,
				'socioCodigo': solicitud.socio.codigo,
				'socioNombre': solicitud.socio.nombreCompleto,
				'socioCedula': solicitud.socio.cedula,
				'socioSalario': solicitud.salarioSocio if solicitud.salarioSocio != None else 0,
				'representanteCodigo': solicitud.representante.id,
				'representanteNombre': solicitud.representante.nombre,
				'cobrador': solicitud.cobrador.userLog.username,
				'autorizadoPor': solicitud.autorizadoPor.username if solicitud.autorizadoPor != None else '',
				'montoSolicitado': solicitud.montoSolicitado,
				'ahorrosCapitalizados': solicitud.ahorrosCapitalizados,
				'deudasPrestamos': solicitud.deudasPrestamos,
				'prestacionesLaborales': solicitud.prestacionesLaborales,
				'valorGarantizado': solicitud.valorGarantizado,
				'netoDesembolsar': solicitud.netoDesembolsar,
				'observacion': solicitud.observacion,
				'categoriaPrestamoId': solicitud.categoriaPrestamo.id,
				'categoriaPrestamoDescrp': solicitud.categoriaPrestamo.descripcion,
				'idSuplidor': solicitud.suplidor.id,
				'suplidorNombre': solicitud.suplidor.nombre,
				'fechaParaDescuento': solicitud.fechaParaDescuento,
				'tasaInteresAnual': solicitud.tasaInteresAnual,
				'tasaInteresMensual': solicitud.tasaInteresMensual,
				'cantidadCuotas': solicitud.cantidadCuotas,
				'valorCuotasCapital': solicitud.valorCuotasCapital,
				'fechaAprobacion': solicitud.fechaAprobacion if solicitud.fechaAprobacion != None else '',
				'fechaRechazo': solicitud.fechaRechazo if solicitud.fechaRechazo != None else '',
				'estatus': solicitud.estatus,
				'prestamo': solicitud.prestamo,
				'userLog': solicitud.userLog.username,
				'datetimeServer': solicitud.datetimeServer,
				'articulos': [ 
					{	'articulo': detalle.articulo,
						'cantidad': detalle.cantidad,
						'precio': detalle.precio,
						'descuento': detalle.descuento,
					} 
					for detalle in SolicitudOrdenDespachoD.objects.filter(ordenDespacho=solicitud)],
				})

		return JsonResponse(data, safe=False)


#Imprimir Orden de Despacho
class ImprimirODView(LoginRequiredMixin, TemplateView):

	template_name = 'print_ordendespacho.html'

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)
			od = data['noSolicitud']

			orden = SolicitudOrdenDespachoH.objects.get(noSolicitud=od)
			orden.impresa = orden.impresa + 1
			orden.save()

			return HttpResponse(orden.impresa)

		except Exception as e:
			return HttpResponse(e)	
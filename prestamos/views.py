from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, JsonResponse

from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SolicitudesPrestamosSerializer

from .models import SolicitudPrestamo, PrestamoUnificado, MaestraPrestamo
from administracion.models import CategoriaPrestamo, Cobrador, Representante, Socio

import json
import math
import decimal
import datetime

#Vista para Maestra de Prestamos
class MaestraPrestamosView(TemplateView):

	template_name = 'maestraprestamos.html'


#Vista para Desembolso Electronico de Prestamos
class DesembolsoPrestamosView(TemplateView):

	template_name = 'desembolsoelectronico.html'


#Vista para Solicitud de Prestamo  -- El POST guarda la Solicitud de Prestamo
class SolicitudPrestamoView(TemplateView):

	template_name = 'solicitudprestamo.html'

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
			representante = Representante.objects.get(id=solicitante['representanteCodigo'])
			# auxiliar = Auxiliar.objects.get()
			categoriaPrest = CategoriaPrestamo.objects.get(id=solicitud['categoriaPrestamoId'])

			if solicitudNo > 0:
				SolPrestamo = SolicitudPrestamo.objects.get(noSolicitud=solicitudNo)
			else:
				try:
					SolPrestamo = SolicitudPrestamo()
					SolPrestamo.noSolicitud = SolicitudPrestamo.objects.latest('noSolicitud').noSolicitud + 1
				except SolPrestamo.DoesNotExist:
					SolPrestamo.noSolicitud = 1

			SolPrestamo.socio = socio
			SolPrestamo.fechaSolicitud = fechaSolicitud
			SolPrestamo.salarioSocio = decimal.Decimal(solicitante['salario'].replace(',','')) if solicitante['salario'] != None else 0
			SolPrestamo.representante = representante
			SolPrestamo.cobrador = cobrador

			SolPrestamo.montoSolicitado = decimal.Decimal(solicitud['montoSolicitado'].replace(',',''))
			SolPrestamo.ahorrosCapitalizados = decimal.Decimal(solicitud['ahorrosCapitalizados'].replace(',','')) if solicitud['ahorrosCapitalizados'] != None else 0
			SolPrestamo.deudasPrestamos = decimal.Decimal(solicitud['deudasPrestamos'].replace(',','')) if solicitud['deudasPrestamos'] != None else 0
			SolPrestamo.prestacionesLaborales = decimal.Decimal(solicitud['prestacionesLaborales'].replace(',','')) if solicitud['prestacionesLaborales'] != None else 0
			SolPrestamo.valorGarantizado = decimal.Decimal(solicitud['valorGarantizado'].replace(',','')) if solicitud['valorGarantizado'] != None else 0
			SolPrestamo.netoDesembolsar = decimal.Decimal(solicitud['netoDesembolsar'].replace(',',''))
			SolPrestamo.observacion = solicitud['nota']
			SolPrestamo.categoriaPrestamo = categoriaPrest
			SolPrestamo.fechaParaDescuento = fechaDescuento

			SolPrestamo.tasaInteresAnual = decimal.Decimal(solicitud['tasaInteresAnual'])
			SolPrestamo.tasaInteresMensual = decimal.Decimal(solicitud['tasaInteresMensual'])
			SolPrestamo.cantidadCuotas = solicitud['cantidadCuotas']
			SolPrestamo.valorCuotasCapital = decimal.Decimal(solicitud['valorCuotas'].replace(',',''))

			SolPrestamo.userLog = User.objects.get(username=request.user.username)

			SolPrestamo.save()

			return HttpResponse(SolPrestamo.noSolicitud)

		except Exception as e:
			return HttpResponse(e)


#Vista para Solicitud de Ordenes de Despacho
class SolicitudOrdenDespachoView(TemplateView):

	template_name = 'solicitudordendespacho.html'


#Vista para Notas de Debito
class NotaDeDebitoView(TemplateView):

	template_name = 'notasdebito.html'


#Vista para Notas de Credito
class NotaDeCreditoView(TemplateView):

	template_name = 'notascredito.html'


#Vista para Notas de Credito Especiales
class NotaDeCreditoEspView(TemplateView):

	template_name = 'notacreditoespecial.html'


# Listado de Solicitudes de Prestamos
class SolicitudesPrestamosAPIView(APIView):

	serializer_class = SolicitudesPrestamosSerializer

	def get(self, request, solicitud=None):
		if solicitud != None:
			solicitudes = SolicitudPrestamo.objects.filter(noSolicitud=solicitud)
		else:
			solicitudes = SolicitudPrestamo.objects.all().order_by('-noSolicitud')

		response = self.serializer_class(solicitudes, many=True)
		return Response(response.data)


# Listado de Solicitudes de Prestamos Por Codigo de Socio
class SolicitudesPrestamosAPIViewByCodigoNombre(APIView):

	serializer_class = SolicitudesPrestamosSerializer

	def get(self, request, codigo=None, nombre=None):
		if codigo != None:
			solicitudes = SolicitudPrestamo.objects.filter(socio__codigo=codigo).order_by('-noSolicitud')
		else:
			solicitudes = SolicitudPrestamo.objects.filter(socio__nombreCompleto__contains=nombre).order_by('-noSolicitud')

		response = self.serializer_class(solicitudes, many=True)
		return Response(response.data)


# Desglose de Solicitud de Prestamo
class SolicitudPrestamoById(DetailView):

	queryset = SolicitudPrestamo.objects.all()

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
				'PrestamosUnificados': [ 
					{	'prestamoUnificado': pu.prestamoUnificado.noPrestamo,
						'capitalUnificado': pu.capitalUnificado,
						'estatus': pu.estatus,
					} 
					for pu in PrestamoUnificado.objects.filter(prestamoPrincipal__noSolicitud=solicitud.noSolicitud)],
				})

		return JsonResponse(data, safe=False)


# Aprobar/Rechazar solicitudes de prestamos
class AprobarRechazarSolicitudesPrestamosView(View):

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			solicitudes = data['solicitudes']
			accion = data['accion']

			for solicitud in solicitudes:
				oSolicitud = SolicitudPrestamo.objects.get(noSolicitud=solicitud['noSolicitud'])
				oSolicitud.estatus = accion
				oSolicitud.fechaAprobacion = datetime.datetime.now() if accion == 'A' else None
				oSolicitud.fechaRechazo = datetime.datetime.now() if accion == 'R' or accion == 'C' else None
				oSolicitud.autorizadoPor = request.user
				oSolicitud.save()

				#Crear prestamo en la maestra de prestamos
				maestra = MaestraPrestamo()

				maestra.noPrestamo = MaestraPrestamo.objects.get_o_create('noPrestamo').latest().noPrestamo
				maestra.noSolicitudPrestamo = oSolicitud

				maestra.categoriaPrestamo = oSolicitud.categoriaPrestamo
				maestra.socio = oSolicitud.socio
				maestra.representante = oSolicitud.representante
				maestra.oficial = oSolicitud.cobrador
				# maestra.distrito = oSolicitud.distrito
				maestra.montoInicial = oSolicitud.netoDesembolsar
				maestra.tasaInteresAnual = oSolicitud.tasaInteresAnual
				maestra.tasaInteresMensual = oSolicitud.tasaInteresMensual
				maestra.pagoPrestamoAnterior = 0
				maestra.cantidadCuotas = oSolicitud.cantidadCuotas
				maestra.montoCuotaQ1 = oSolicitud.valorCuotasCapital
				maestra.montoCuotaQ2 = oSolicitud.valorCuotasCapital
				maestra.fechaDesembolso = oSolicitud.fechaParaDescuento
				maestra.fechaEntrega = datetime.datetime.now()
				# maestra.chequeNo
				maestra.valorGarantizado = oSolicitud.valorGarantizado
				maestra.userLog = request.user





			return HttpResponse(1)

		except Exception as e:
			return HttpResponse(e)

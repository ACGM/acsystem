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
			representante = Representante.objects.get(id=solicitante['representanteCodigo'])
			categoriaPrest = CategoriaPrestamo.objects.get(id=solicitud['categoriaPrestamoId'])
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
			SolOrdenDespacho.salarioSocio = decimal.Decimal(solicitante['salario'].replace(',','')) if solicitante['salario'] != None else 0
			SolOrdenDespacho.representante = representante
			SolOrdenDespacho.autorizadoPor = User.objects.get(username=solicitante['autorizadoPor'])
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

			SolOrdenDespacho.tasaInteresAnual = decimal.Decimal(solicitud['tasaInteresAnual'])
			SolOrdenDespacho.tasaInteresMensual = decimal.Decimal(solicitud['tasaInteresMensual'])
			SolOrdenDespacho.cantidadCuotas = solicitud['cantidadCuotas']
			SolOrdenDespacho.valorCuotasCapital = decimal.Decimal(solicitud['valorCuotas'].replace(',',''))

			SolOrdenDespacho.localidad = UserExtra.objects.get(usuario__username=request.user.username).localidad

			SolOrdenDespacho.userLog = User.objects.get(username=request.user.username)

			SolOrdenDespacho.save()

			return HttpResponse(SolOrdenDespacho.noSolicitud)

		except Exception as e:
			return HttpResponse(e)


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


	
# VIEWS de Prestamo

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, JsonResponse
from django.db import transaction

from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SolicitudesPrestamosSerializer

from .models import SolicitudPrestamo, PrestamoUnificado, MaestraPrestamo
from administracion.models import CategoriaPrestamo, Cobrador, Representante, Socio, Autorizador, UserExtra, Banco, DocumentoCuentas

from acgm.views import LoginRequiredMixin

import json
import math
import decimal
import datetime


#Vista para Desembolso Electronico de Prestamos
class DesembolsoPrestamosView(LoginRequiredMixin, TemplateView):

	template_name = 'desembolsoelectronico.html'


#Vista para Notas de Debito
class NotaDeDebitoView(LoginRequiredMixin, TemplateView):

	template_name = 'notasdebito.html'


#Vista para Notas de Credito
class NotaDeCreditoView(LoginRequiredMixin, TemplateView):

	template_name = 'notascredito.html'


#Vista para Notas de Credito Especiales
class NotaDeCreditoEspView(LoginRequiredMixin, TemplateView):

	template_name = 'notacreditoespecial.html'


#Imprimir Solicitud de Prestamo
class ImprimirSolicitudPView(LoginRequiredMixin, TemplateView):

	template_name = 'print_solicitudprestamo.html'


#Imprimir Solicitud de Prestamo
class ImprimirRecibidoConformeView(LoginRequiredMixin, TemplateView):

	template_name = 'print_recibidoconforme.html'


#Reporte de Solicitudes de Prestamos Emitidas
class rptSolPrestamosEmitidas(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_solprestamos.html'


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


# Listado de Solicitudes de Prestamos Por Rango de Fecha
class SolicitudesPrestamosAPIViewByRangoFecha(APIView):

	serializer_class = SolicitudesPrestamosSerializer

	def get(self, request, fechaInicio, fechaFin):
		
		solicitudes = SolicitudPrestamo.objects.filter(fechaSolicitud__range=(fechaInicio, fechaFin)).order_by('-fechaSolicitud')

		response = self.serializer_class(solicitudes, many=True)
		return Response(response.data)


#Vista para Solicitud de Prestamo  -- El POST guarda la Solicitud de Prestamo
class SolicitudPrestamoView(LoginRequiredMixin, TemplateView):

	template_name = 'solicitudprestamo.html'

	def post(self, request, *args, **kwargs):

		try:

			data = json.loads(request.body)

			solicitante = data['solicitante']
			solicitud = data['solicitud']
			fechaSolicitud = data['fechaSolicitud']
			fechaDescuento = data['fechaDescuento']
			prestamosUnificados = data['prestamosUnificados']

			solicitudNo = solicitud['solicitudNo']

			socio = Socio.objects.get(codigo=solicitante['codigoEmpleado'])
			cobrador = Cobrador.objects.get(userLog=User.objects.get(username=solicitante['cobrador']))
			representante = Representante.objects.get(id=solicitante['representanteCodigo'])
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
			SolPrestamo.autorizadoPor = User.objects.get(username=solicitante['autorizadoPor'])
			SolPrestamo.cobrador = cobrador

			SolPrestamo.montoSolicitado = decimal.Decimal(solicitud['montoSolicitado'].replace(',',''))
			SolPrestamo.ahorrosCapitalizados = decimal.Decimal(solicitud['ahorrosCapitalizados'].replace(',','')) if solicitud['ahorrosCapitalizados'] != None else 0
			SolPrestamo.deudasPrestamos = decimal.Decimal(solicitud['deudasPrestamos'].replace(',','')) if solicitud['deudasPrestamos'] > 0 else 0
			SolPrestamo.prestacionesLaborales = decimal.Decimal(solicitud['prestacionesLaborales'].replace(',','')) if solicitud['prestacionesLaborales'] != None else 0
			SolPrestamo.valorGarantizado = decimal.Decimal(solicitud['valorGarantizado'].replace(',','')) if solicitud['valorGarantizado'] != None else 0
			SolPrestamo.netoDesembolsar = decimal.Decimal(solicitud['netoDesembolsar'].replace(',',''))
			SolPrestamo.observacion = solicitud['nota']
			SolPrestamo.categoriaPrestamo = categoriaPrest
			SolPrestamo.fechaParaDescuento = fechaDescuento
			SolPrestamo.garante = Socio.objects.get(codigo=solicitud['garante']) if solicitud.has_key('garante') else None

			SolPrestamo.tasaInteresAnual = decimal.Decimal(solicitud['tasaInteresAnual'])
			SolPrestamo.tasaInteresMensual = decimal.Decimal(solicitud['tasaInteresMensual'])
			SolPrestamo.cantidadCuotas = solicitud['cantidadCuotas']
			SolPrestamo.valorCuotasCapital = decimal.Decimal(solicitud['valorCuotas'].replace(',',''))

			SolPrestamo.localidad = UserExtra.objects.get(usuario__username=request.user.username).localidad

			SolPrestamo.userLog = User.objects.get(username=request.user.username)

			SolPrestamo.save()

			#Guardar los prestamos a Unificar
			montoPrestamosUnificados = 0

			for pu in prestamosUnificados:
				prestamoUnif = PrestamoUnificado()
				prestamoUnif.solicitudPrestamo = SolPrestamo
				prestamoUnif.prestamoUnificado =  MaestraPrestamo.objects.get(noPrestamo=pu['noPrestamo'])
				prestamoUnif.capitalUnificado = pu['balance']
				prestamoUnif.save()

				montoPrestamosUnificados += decimal.Decimal(prestamoUnif.capitalUnificado)
			#Fin Prestamos a Unificar

			SolPrestamo.netoDesembolsar -= montoPrestamosUnificados
			SolPrestamo.save() 

			return HttpResponse(SolPrestamo.noSolicitud)

		except Exception as e:
			return HttpResponse(e)
		

# Verificar Autorizador
class validarAutorizadorView(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):

		data = json.loads(request.body)

		autorizador = data['autorizador']
		pin = data['pin']

		try:
			usuario = User.objects.get(username=autorizador)

			AU = Autorizador.objects.get(usuario=usuario, clave=pin)

			return HttpResponse(1)

		except Exception as e:
			return HttpResponse(e)


# Desglose de Solicitud de Prestamo
class SolicitudPrestamoById(LoginRequiredMixin, DetailView):

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
				'garante': solicitud.garante.codigo if solicitud.garante != None else '',
				'prestamo': solicitud.prestamo,
				'userLog': solicitud.userLog.username,
				'datetimeServer': solicitud.datetimeServer,
				'PrestamosUnificados': [ 
					{	'noPrestamo': pu.prestamoUnificado.noPrestamo,
						'balance': pu.capitalUnificado,
						'estatus': pu.estatus,
					} 
					for pu in PrestamoUnificado.objects.filter(solicitudPrestamo__noSolicitud=solicitud.noSolicitud)],
				})

		return JsonResponse(data, safe=False)


# Aprobar/Rechazar solicitudes de prestamos
class AprobarRechazarSolicitudesPrestamosView(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):

		with transaction.atomic():

			try:

				data = json.loads(request.body)

				solicitudes = data['solicitudes']
				accion = data['accion']

				for solicitud in solicitudes:
					oSolicitud = SolicitudPrestamo.objects.get(noSolicitud=solicitud['noSolicitud'])
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

						maestra.noSolicitudPrestamo = oSolicitud
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

						#Para cuando existe(n) Prestamo(s) Unificado(s)
						

				return HttpResponse(1)

			except Exception as e:
				return HttpResponse(e)


# Marcar como Desembolso Electronico o Cheque
class MarcarPrestamoComoDCView(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			prestamos = data['prestamos']
			accion = data['accion']
			
			# Marcar cada prestamo con D - Para Desembolsos Electronicos o C - Para Cheques
			for prestamo in prestamos:
				p = MaestraPrestamo.objects.get(noPrestamo=prestamo['noPrestamo'])
				p.estatus = accion
				p.save()

			return HttpResponse(1)

		except Exception as e:
			return HttpResponse(e)


# Guardar relacion del archivo de Deposito Banco con el prestamo
def relacionArchivoBancoConDesembolsoElectronico(request):
	
	data = json.loads(request.body)

	for prestamo in data['prestamos']:
		MaestraPrestamo.objects.filter(noPrestamo=prestamo['noPrestamo']).update(archivoBanco=data['archivoBanco'])

	return HttpResponse(1)


# Prestamos para Desembolso Electronico
class PrestamosDesembolsoElectronico(LoginRequiredMixin, DetailView):

	queryset = MaestraPrestamo.objects.filter(estatus='E', noSolicitudPrestamo__gt=0).order_by('-noPrestamo')

	def get(self, request, *args, **kwargs):

		self.object_list = self.get_queryset()
		return self.json_to_response()

	def json_to_response(self):
		data = list()

		banco = Banco.objects.get(estatus='A')

		for prestamo in self.object_list:
			maestra = MaestraPrestamo.objects.get(noPrestamo=prestamo.noPrestamo)
			doc = DocumentoCuentas.objects.filter(documento__codigo='DESE').order_by('accion')

			data.append({
				'noPrestamo': prestamo.noPrestamo,
				'cuotas': maestra.cantidadCuotas,
				'tasaInteresMensual': maestra.tasaInteresMensual,
				'estatus': prestamo.estatus,
				'socioCodigo': prestamo.socio.codigo,
				'socioNombre': prestamo.socio.nombreCompleto,
				'socioCedula': prestamo.socio.cedula,
				'socioCuentaBancaria': prestamo.socio.cuentaBancaria,
				'socioTipoCuentaBancaria': prestamo.socio.tipoCuentaBancaria,
				'bancoCodigo': banco.codigo,
				'bancoNombre': banco.nombre,
				'netoDesembolsar': prestamo.montoInicial,
				'fechaDesembolso': prestamo.fechaDesembolso,
				'cuentaDesembolsoCodigo': doc[0].cuenta.codigo,
				'cuentaDesembolsoDescrp': doc[0].cuenta.descripcion,
				'cuentaDesembolsoAuxiliar': doc[1].cuenta.codigo,
				'archivoBanco': prestamo.archivoBanco,
				})

		return JsonResponse(data, safe=False)


# Marcar como posteados los Prestamos y Ordenes de Despacho
class PostearPrestamosODView(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			prestamos = data['prestamos']
			
			# Marcar cada prestamo/OD con P - Posteado
			for prestamo in prestamos:
				p = MaestraPrestamo.objects.get(noPrestamo=prestamo['noPrestamo'])
				p.estatus = 'P'
				p.save()

			return HttpResponse(1)

		except Exception as e:
			return HttpResponse(e)


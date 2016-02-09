# VIEWS de Prestamo

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.db.models import Sum, Count

from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SolicitudesPrestamosSerializer, PagoCuotasPrestamoSerializer, MaestraPrestamosListadoSerializer, \
							InteresPrestamoBaseAhorroSerializer

from .models import SolicitudPrestamo, PrestamoUnificado, MaestraPrestamo, PagoCuotasPrestamo, InteresPrestamosBaseAhorros, \
					NotaDeDebitoPrestamo, NotaDeCreditoPrestamo

from administracion.models import CategoriaPrestamo, Cobrador, Representante, Socio, Autorizador, UserExtra, Banco, DocumentoCuentas
from conciliacion.views import prestSolicitud

from acgm.views import LoginRequiredMixin

import json
import math
import decimal
import datetime


# Prestamos Busqueda (GENERICO)
def prestamosSearch(request):
	return render(request, 'prestamos_search.html')


# Pago Cuotas Busqueda (GENERICO)
def pagoCuotasSearch(request):
	return render(request, 'pago_cuotas_search.html')


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


#Vista para Distribucion de Intereses
class DistribucionInteresesView(LoginRequiredMixin, TemplateView):

	template_name = 'distribucion_intereses.html'


#Vista para Tabla de Amortizacion
class TablaAmortizacionView(LoginRequiredMixin, TemplateView):

	template_name = 'tabla_amortizacion.html'


#Vista para Estado de Cuenta
class EstadoCuentaView(LoginRequiredMixin, TemplateView):

	template_name = 'estado_cuenta.html'


#Vista para Resumen Estado de Socios
class ResumenEstadoSociosView(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_resumen_estado_socios.html'


#Imprimir Solicitud de Prestamo
class ImprimirSolicitudPView(LoginRequiredMixin, TemplateView):

	template_name = 'print_solicitudprestamo.html'


#Imprimir Solicitud de Prestamo
class ImprimirRecibidoConformeView(LoginRequiredMixin, TemplateView):

	template_name = 'print_recibidoconforme.html'


#Reporte de Solicitudes de Prestamos Emitidas
class rptSolPrestamosEmitidas(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_solprestamos.html'


#Reporte de Prestamos
class rptPrestamos(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_prestamos.html'


# Listado de Ajustes de inventario
class InteresPrestamosBaseAhorroView(viewsets.ModelViewSet):

	queryset = InteresPrestamosBaseAhorros.objects.all()
	serializer_class = InteresPrestamoBaseAhorroSerializer


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


# Listado de Pagos de Cuotas de Prestamos
class PagoCuotasPrestamoAPIViewByNoPrestamo(APIView):

	serializer_class = PagoCuotasPrestamoSerializer

	def get(self, request, noPrestamo=None):
		if noPrestamo == None:
			pagos = PagoCuotasPrestamo.objects.all().order_by('-fechaPago')
		else:
			pagos = PagoCuotasPrestamo.objects.filter(noPrestamo__noPrestamo=noPrestamo).order_by('-fechaPago')

		response = self.serializer_class(pagos, many=True)
		return Response(response.data)


# Listado de Prestamos Por Rango de Fecha
class PrestamosAPIViewByRangoFecha(APIView):

	serializer_class = MaestraPrestamosListadoSerializer

	def get(self, request, fechaI, fechaF, estatus=None):

		if estatus == None:
			prestamos = MaestraPrestamo.objects.filter(fechaAprobacion__range=(fechaI, fechaF)).order_by('socio')
		else:
			prestamos = MaestraPrestamo.objects.filter(fechaAprobacion__range=(fechaI, fechaF), estatus=estatus).order_by('socio')

			# prestamos = MaestraPrestamo.objects.filter(fechaAprobacion__range=(fechaI, fechaF)).values('noPrestamo','categoriaPrestamo__descripcion').annotate(total=Sum('montoInicial'))

		response = self.serializer_class(prestamos, many=True)
		return Response(response.data)


# Listado de Prestamos Por Rango de Fecha Agrupados por Categoria
class PrestamosAPIViewByCategoria(LoginRequiredMixin, DetailView):

	def get(self, request, *args, **kwargs):
		fechaI = self.request.GET.get('fechaI')
		fechaF = self.request.GET.get('fechaF')
		estatus = self.request.GET.get('estatus')

		# self.object_list = self.get_queryset().filter(fechaAprobacion__range=(fechaI, fechaF), estatus=estatus). \
		# 					annotate(totalMonto=Sum('montoInicial'), totalCantidad=Count('categoriaPrestamo'))

		return self.json_to_response(fechaI, fechaF, estatus)

	def json_to_response(self, fechaI, fechaF, estatus):
		data = list()

		for registro in MaestraPrestamo.objects.raw('SELECT c.id, c.descripcion, SUM(p.montoInicial) totalMonto, COUNT(0) totalCantidad \
													FROM prestamos_maestraprestamo p \
													LEFT JOIN administracion_categoriaPrestamo c ON c.id = p.categoriaPrestamo_id \
													GROUP BY c.descripcion \
													HAVING p.fechaAprobacion BETWEEN \'' + fechaI + '\' \
													AND \'' + fechaF + '\' AND p.estatus = \'' + estatus + '\' '):
			data.append({
				'id': registro.id,
				'categoriaPrestamo': registro.descripcion,
				'totalMonto': registro.totalMonto,
				'totalCantidad': registro.totalCantidad,
				})

		return JsonResponse(data, safe=False)


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
			SolPrestamo.ahorrosCapitalizados = decimal.Decimal(solicitud['ahorrosCapitalizados'].replace(',','')) if solicitud['ahorrosCapitalizados'] != None \
				and solicitud['ahorrosCapitalizados'] > 0 else 0			
			SolPrestamo.deudasPrestamos = decimal.Decimal(solicitud['deudasPrestamos'].replace(',','')) if solicitud['deudasPrestamos'] > 0 else 0

			SolPrestamo.prestacionesLaborales = decimal.Decimal(solicitud['prestacionesLaborales'].replace(',','')) if solicitud['prestacionesLaborales'] != None else 0

			SolPrestamo.valorGarantizado = decimal.Decimal(solicitud['valorGarantizado']) if solicitud['valorGarantizado'] != None else 0

			SolPrestamo.netoDesembolsar = decimal.Decimal(solicitud['netoDesembolsar'].replace(',',''))
			SolPrestamo.observacion = solicitud['nota']
			SolPrestamo.categoriaPrestamo = categoriaPrest
			SolPrestamo.fechaParaDescuento = fechaDescuento

			if solicitud.has_key('garante') and solicitud['garante'] != '':
				SolPrestamo.garante = Socio.objects.get(codigo=solicitud['garante']) if solicitud.has_key('garante') else None

			SolPrestamo.tasaInteresAnual = decimal.Decimal(solicitud['tasaInteresAnual'])
			SolPrestamo.tasaInteresMensual = decimal.Decimal(solicitud['tasaInteresMensual'])
			SolPrestamo.cantidadCuotas = solicitud['cantidadCuotas']
			SolPrestamo.valorCuotasCapital = decimal.Decimal(solicitud['valorCuotas'].replace(',',''))
			SolPrestamo.interesBaseAhorroMensual = decimal.Decimal(solicitud['tasaInteresBaseAhorro'])

			SolPrestamo.localidad = UserExtra.objects.get(usuario__username=request.user.username).localidad

			SolPrestamo.userLog = User.objects.get(username=request.user.username)

			#Verificar para prestamos unificados
			montoPrestamosUnificados = 0

			for pu_valida in prestamosUnificados:
				montoPrestamosUnificados += decimal.Decimal(pu_valida['balance'])
			
			if montoPrestamosUnificados > SolPrestamo.montoSolicitado:
				raise Exception('El monto de los prestamos a unificar no puede ser mayor al MONTO SOLICITADO.')

			SolPrestamo.save()

			#Guardar los prestamos a Unificar
			for pu in prestamosUnificados:
				prestamoUnif = PrestamoUnificado()
				prestamoUnif.solicitudPrestamo = SolPrestamo
				prestamoUnif.prestamoUnificado =  MaestraPrestamo.objects.get(noPrestamo=pu['noPrestamo'])
				prestamoUnif.capitalUnificado = pu['balance']
				prestamoUnif.save()
			#Fin Prestamos a Unificar

			# SolPrestamo.netoDesembolsar -= montoPrestamosUnificados
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
				'socioDepto': solicitud.socio.departamento.descripcion,
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
						maestra.tasaInteresPrestBaseAhorro = oSolicitud.interesBaseAhorroMensual
						maestra.pagoPrestamoAnterior = 0
						maestra.cantidadCuotas = oSolicitud.cantidadCuotas
						maestra.valorGarantizado = oSolicitud.prestacionesLaborales if oSolicitud.prestacionesLaborales > 0 else oSolicitud.valorGarantizado
						maestra.valorAhorro = oSolicitud.ahorrosCapitalizados
						maestra.montoCuotaQ1 = oSolicitud.valorCuotasCapital

						if oSolicitud.categoriaPrestamo.descripcion[:6] == 'AVANCE':
							tipo = oSolicitud.categoriaPrestamo.descripcion.split(' ')[1][:3]
							tipo = 'RG' if tipo == 'REG' else tipo[:2]

							maestra.balance = oSolicitud.netoDesembolsar + (oSolicitud.netoDesembolsar * (oSolicitud.tasaInteresAnual/100))
							maestra.montoCuotaQ1 = maestra.balance

							maestra.tipoPrestamoNomina = tipo
						else:
							maestra.balance = oSolicitud.netoDesembolsar
							maestra.montoCuotaQ2 = oSolicitud.valorCuotasCapital

						maestra.userLog = request.user

						maestra.save()

						#Guardar No. de Prestamo en la Solicitud
						oSolicitud.prestamo = maestra.noPrestamo
						oSolicitud.save()

					#Para cuando existe(n) Prestamo(s) Unificado(s)
					try:
						prestamosUnif = PrestamoUnificado.objects.filter(solicitudPrestamo__noSolicitud=oSolicitud.noSolicitud)

						for p in prestamosUnif:
							if oSolicitud.estatus == 'A':

								prestamo = MaestraPrestamo.objects.get(noPrestamo=p.prestamoUnificado.noPrestamo)
								# Estas lineas fueron sustituidas por el metodo de pagoCuota
								# prestamo.balance = 0
								# prestamo.estatus = 'S'
								# prestamo.save()

								# Aplicar saldo de prestado unificado -- NCPU = Nota de Credito Prestamo Unificado
								guardarPagoCuotaPrestamo(self, p.prestamoUnificado.noPrestamo, prestamo.balance, 0, 0,'{0}{1}'.format('NCPU', p.prestamoUnificado.id), 'NC')

							p.estatus = oSolicitud.estatus
							p.save()
					except:
						pass
					#Fin condicion Prestamo(s) Unificado(s)


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

				# Si es para marcar como cheque se creara la solicitud de cheque en el modulo de Conciliacion
				if accion == 'C':
					concepto = "Este es el cheque del prestamo..."
					fecha = datetime.datetime.now()
					prestSolicitud(self, fecha, prestamo['codigoSocio'], None, concepto, prestamo['balance'], prestamo['noPrestamo'])

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
				p.posteoUsr = request.user
				p.posteadoFecha = datetime.datetime.now()
				p.save()

			return HttpResponse(1)

		except Exception as e:
			return HttpResponse(e)


# Marcar como posteada la Nota de Debito y aplicarla al prestamo
class PostearNotaDebitoView(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			notaDebito = data['nd']
			
			# Marcar nota de debito con posteado
			for nd in notaDebito:
				notaD = NotaDeDebitoPrestamo.objects.get(id=nd['id'])
				notaD.estatus = 'A'
				notaD.posteado = 'S'
				notaD.posteoUsr = request.user
				notaD.fechaPosteo = datetime.datetime.now()
				notaD.save()

				# Aplicar la nota de debito
				guardarPagoCuotaPrestamo(self, nd['noPrestamo'], nd['valorCapital'], nd['valorInteres'], 0,'{0}{1}'.format('NDBT', nd['id']) , 'ND')

			return HttpResponse(1)

		except Exception as e:
			return HttpResponse(e)


# Marcar como posteada la Nota de Credito y aplicarla al prestamo
class PostearNotaCreditoView(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			notaCredito = data['nc']
			
			# Marcar nota de credito con posteado
			for nc in notaCredito:
				notaC = NotaDeCreditoPrestamo.objects.get(id=nc['id'])
				notaC.estatus = 'A'
				notaC.posteado = 'S'
				notaC.posteoUsr = request.user
				notaC.fechaPosteo = datetime.datetime.now()
				notaC.save()

				# Aplicar la nota de credito
				guardarPagoCuotaPrestamo(self, nc['noPrestamo'], nc['valorCapital'], nc['valorInteres'], 0,'{0}{1}'.format('NDCT', nc['id']) , 'NC')

			return HttpResponse(1)

		except Exception as e:
			return HttpResponse(e)


# Metodo para guardar cuota en pago de cuota a prestamo
# Esto incluye Nota de Debito, Nota de Credito, Recibo de Ingreso, pago desde Ahorros
# Todo lo concerniente a cuotas de prestamos
# Los parametros se decriben como sigue:
# 	1-noPrestamo: es el numero del prestamo en formato integer 
#	2-valorCapital: es el monto del capital en formato string, pero sin coma
#	3-valorInteres: es el monto del interes garantizado en formato string, pero sin coma
#	4-valorInteresAh: es el monto del interes en base ahorrado en formato string, pero sin coma
#	5-docReferencia: es el documento de referencia que afecta al prestamo, se especifican las 4 letras del documento de la tabla TipoDocumento.
#		Por ej: NDCT - Nota de Credito
#				NOMP - Nomina de Descuentos Prestamos
#	6-tipoDoc: es el tipo de Documento, por ej: 	NC - Nota de Credito, 
#													ND - Nota de Debito,
#													NM - Nomina, RI - Recibo de Ingreso, AH - Ahorros 
def guardarPagoCuotaPrestamo(self, noPrestamo, valorCapital, valorInteres, valorInteresAh, docReferencia, tipoDoc):

	#Obtener el prestamo como tal
	prestamo = MaestraPrestamo.objects.get(noPrestamo=noPrestamo)

	# NC = Nota de Credito   ---- RI = Recibo Ingreso
	# AH = Descontar desde ahorro para pagar capital a prestamo.
	if tipoDoc == 'NC' or tipoDoc == 'RI' or tipoDoc == 'AH':
		validaPagoPrestamo(self, prestamo, decimal.Decimal(valorCapital), docReferencia, tipoDoc)

	# Nomina de descuentos
	if tipoDoc == 'NM':
		validaPagoPrestamo(self, prestamo, decimal.Decimal(valorCapital), docReferencia, tipoDoc)

        prestamo.valorAhorro = prestamo.valorAhorro - valorInteresAh if prestamo.valorAhorro > 0 and prestamo.valorAhorro - valorInteresAh >= 0 else 0
        prestamo.valorGarantizado = prestamo.valorGarantizado - valorInteres if prestamo.valorGarantizado > 0 and prestamo.valorGarantizado - valorInteres >= 0 else 0
        
        prestamo.save()
	
	# Nota de Debito
	if tipoDoc == 'ND':
		prestamo.balance = prestamo.balance + decimal.Decimal(valorCapital)
		prestamo.save()
		
		#Guardar la cuota
		ejecutaPagoCuota(self, prestamo, valorCapital, valorInteres, valorInteresAh, docReferencia, tipodoc)
	

# Metodo para validar si el pago del prestamo es completo
# Tambien es utilizado para rebajar el balance
def validaPagoPrestamo(self, Prestamo, montoAbono, docReferencia, tipodoc):

	if Prestamo.balance - montoAbono < 0:
		raise Exception('El monto del abono al prestamo es mayor que el balance a la fecha.')

	else:
		while montoAbono > 0:

			#Calcular el interes Garantizado y de Base Ahorro
			if tipodoc != 'NM':
				valorInteresG = 0
				valorInteresA = 0
			else:
				monto = Prestamo.balance
				ahorrado = Prestamo.valorAhorro
				garantia = Prestamo.valorGarantizado

				porcentajeCuotaAhorro = ahorrado / monto if ahorrado > 0 else 0
				porcentajeCuotaGarantizado = garantia / monto if garantia > 0 else 0
			#Fin calculo interes

			if Prestamo.montoCuotaQ1 >= 0:
				if montoAbono >= Prestamo.montoCuotaQ1:
					Prestamo.balance -= Prestamo.montoCuotaQ1
					montoAbono -= Prestamo.montoCuotaQ1

					cuotaAh = Prestamo.montoCuotaQ1 * (porcentajeCuotaAhorro/100)
					cuotaGr = Prestamo.montoCuotaQ1 * (porcentajeCuotaGarantizado/100)
					
					valorInteresG = 0#Prestamo.valorInteres
					valorInteresA = 0#Prestamo.valorInteresAh

					Prestamo.save()
					ejecutaPagoCuota(self, Prestamo, Prestamo.montoCuotaQ1, valorInteresG, valorInteresA, \
						docReferencia, tipodoc)


			if Prestamo.montoCuotaQ2 >= 0:
				if montoAbono >= Prestamo.montoCuotaQ2:
					Prestamo.balance -= Prestamo.montoCuotaQ2
					montoAbono -= Prestamo.montoCuotaQ2
					Prestamo.save()
					ejecutaPagoCuota(self, Prestamo, Prestamo.montoCuotaQ1, Prestamo.valorInteres, Prestamo.valorInteresAh, \
						docReferencia, tipodoc)
		
		if Prestamo.balance == 0:
			Prestamo.estatus = 'S'

		Prestamo.save()


#Guardar una cuota de Prestamo
def ejecutaPagoCuota(self, prestamo, valorCapital, valorInteres, valorInteresAh, docReferencia, tipoDoc):

	cuota = PagoCuotasPrestamo()
	cuota.noPrestamo = prestamo
	cuota.valorCapital = valorCapital
	cuota.valorInteres = valorInteres
	cuota.valorInteresAh = valorInteresAh
	cuota.fecha = datetime.datetime.now()
	cuota.docRef = docReferencia
	cuota.tipoPago = tipoDoc
	cuota.save()


# Estado de Cuenta del Socio
class EstadoCuentaBySocio(LoginRequiredMixin, DetailView):

	queryset = Socio.objects.all()

	def get(self, request, *args, **kwargs):
		codigoSocio = self.request.GET.get('codigo')

		self.object_list = self.get_queryset().filter(codigo=codigoSocio)

		return self.json_to_response()

	def json_to_response(self):
		data = list()


		for registro in self.object_list:
			data.append({
				'cuotaAhorroQ1': registro.cuotaAhorroQ1,
				'cuotaAhorroQ2': registro.cuotaAhorroQ2,
				'nombreCompleto': registro.nombreCompleto,
				'departamento': registro.departamento.descripcion,
				'fechaIngresoCoop': registro.fechaIngresoCoop,
				'fechaIngresoEmpresa': registro.fechaIngresoEmpresa,
				'prestamos': [ 
					{	'noPrestamo': p.noPrestamo,
						'balance': p.balance,
						'estatus': p.estatus,
					} 
					for p in MaestraPrestamo.objects.filter(socio__codigo=registro.codigo)],
				})

		return JsonResponse(data, safe=False)

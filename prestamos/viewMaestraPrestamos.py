# VIEWS de Maestra de Prestamos
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, JsonResponse

from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import MaestraPrestamosListadoSerializer, BalancePrestamosSocioSerializer

from .models import MaestraPrestamo
from administracion.models import CategoriaPrestamo, Cobrador, Representante, Socio, Autorizador
from cuenta.models import DiarioGeneral

from acgm.views import LoginRequiredMixin

import json
import math
import decimal
import datetime


#Vista para Maestra de Prestamos
class MaestraPrestamosView(TemplateView):

	template_name = 'maestraprestamos.html'


# Listado de Prestamos en Maestra
class MaestraPrestamosAPIView(APIView):

	serializer_class = MaestraPrestamosListadoSerializer

	def get(self, request, prestamo=None):
		if prestamo != None:
			prestamos = MaestraPrestamo.objects.filter(noPrestamo=prestamo)
		else:
			prestamos = MaestraPrestamo.objects.all().order_by('-noPrestamo')

		response = self.serializer_class(prestamos, many=True)
		return Response(response.data)


# Listado de Prestamos por Socio
class PrestamosBySocioAPIView(APIView):

	serializer_class = MaestraPrestamosListadoSerializer

	def get(self, request, socio):
		prestamos = MaestraPrestamo.objects.filter(socio__codigo=socio)

		response = self.serializer_class(prestamos, many=True)
		return Response(response.data)

def getBalancesPrestamos(self, socio=None):
	
	if socio == None:

		return MaestraPrestamo.objects.raw('SELECT \
										p.id, \
										p.socio_id, \
										SUM(p.balance) balance \
									FROM prestamos_maestraprestamo p \
									INNER JOIN administracion_socio s ON s.id = p.socio_id \
									GROUP BY p.socio_id \
									HAVING p.estatus = \'P\' \
									\
									')
	else:
		return MaestraPrestamo.objects.raw('SELECT \
										p.id, \
										p.socio_id, \
										SUM(p.balance) balance \
									FROM prestamos_maestraprestamo p \
									INNER JOIN administracion_socio s ON s.id = p.socio_id WHERE p.estatus = \'P\' \
									GROUP BY p.socio_id \
									HAVING s.codigo =' + socio \
									)

# Listado de Prestamos por Socio
class BalancePrestamosBySocioAPIView(APIView):

	serializer_class = BalancePrestamosSocioSerializer

	def get(self, request, socio=None):
		
		prestamos = getBalancesPrestamos(self, socio)

		response = self.serializer_class(prestamos, many=True)
		return Response(response.data)


# Desglose de Prestamo Aprobado
class PrestamoById(LoginRequiredMixin, DetailView):

	queryset = MaestraPrestamo.objects.all()

	def get(self, request, *args, **kwargs):
		noPrestamo = self.request.GET.get('noprestamo')

		self.object_list = self.get_queryset().filter(noPrestamo=noPrestamo)

		format = self.request.GET.get('format')
		if format == 'json':
			return self.json_to_response()

		context = self.get_context_data()
		return self.render_to_response(context)

	def json_to_response(self):
		data = list()

		for prestamo in self.object_list:
			data.append({
				'noPrestamo': prestamo.noPrestamo,
				'documentoDescrp': 'Orden de Despacho' if prestamo.noSolicitudOD != None else 'Prestamo',
				'noSolicitudPrestamo': prestamo.noSolicitudPrestamo.noSolicitud if prestamo.noSolicitudPrestamo != None else '',
				'noSolicitudOD': prestamo.noSolicitudOD.noSolicitud if prestamo.noSolicitudOD != None else '',
				'factura': prestamo.factura.noFactura if prestamo.factura != None else '',
				'categoriaPrestamoId': prestamo.categoriaPrestamo.id,
				'categoriaPrestamoDescrp': prestamo.categoriaPrestamo.descripcion,
				'socioCodigo': prestamo.socio.codigo,
				'socioNombre': prestamo.socio.nombreCompleto,
				'socioCedula': prestamo.socio.cedula,
				'socioDepartamento': prestamo.socio.departamento.descripcion,
				'representanteCodigo': prestamo.representante.id,
				'representanteNombre': prestamo.representante.nombre,
				'oficial': prestamo.oficial.username,
				'localidad': prestamo.localidad.descripcion,
				'montoInicial': prestamo.montoInicial,
				'tasaInteresAnual': prestamo.tasaInteresAnual if prestamo.tasaInteresAnual != None else '',
				'tasaInteresMensual': prestamo.tasaInteresMensual if prestamo.tasaInteresMensual != None else '',
				'tasaInteresPrestBaseAhorro': prestamo.tasaInteresPrestBaseAhorro if prestamo.tasaInteresPrestBaseAhorro != None else '',
				'pagoPrestamoAnterior': prestamo.pagoPrestamoAnterior,
				'cantidadCuotas': prestamo.cantidadCuotas,
				'montoCuotaQ1': prestamo.montoCuotaQ1 if prestamo.montoCuotaQ1 != None else '',
				'montoCuotaQ2': prestamo.montoCuotaQ2 if prestamo.montoCuotaQ2 != None else '',
				'fechaDesembolso': prestamo.fechaDesembolso,
				'fechaEntrega': prestamo.fechaEntrega,
				'chequeNo': prestamo.chequeNo.chequeNo if prestamo.chequeNo != None else '',
				'valorGarantizado': prestamo.valorGarantizado,
				'valorAhorro': prestamo.valorAhorro,
				'balance': prestamo.balance,
				'estatus': prestamo.estatus,
				'posteadoFecha': prestamo.posteadoFecha,
				'tipoPrestamoNomina': prestamo.tipoPrestamoNomina,
				'quincenas': prestamo.quincenas,
				})

		return JsonResponse(data, safe=False)


# Guardar Cambios en Prestamo
class guardarCambiosPrestamo(View):

	def post(self, request, *args, **kwargs):

		try:

			data = json.loads(request.body)

			noPrestamo = data['noPrestamo']
			tipoNomina = data['tipoNomina']
			cuotaQ1 = data['montoQ1']
			cuotaQ2 = data['montoQ2']

			cantidadCuotas = 0

			prestamo = MaestraPrestamo.objects.get(noPrestamo=noPrestamo)

			prestamo.tipoPrestamoNomina = tipoNomina
			prestamo.montoCuotaQ1 = decimal.Decimal(cuotaQ1.replace(',','')) if cuotaQ1 != '' else 0
			prestamo.montoCuotaQ2 = decimal.Decimal(cuotaQ2.replace(',','')) if cuotaQ2 != '' else 0
			
			#Verificar que los montos quincenales no excedan el balance pendiente
			if prestamo.montoCuotaQ1 + prestamo.montoCuotaQ2 > prestamo.balance and prestamo.tipoPrestamoNomina == 'RE':
				raise Exception('Los montos quincenas exceden el balance pendiente.')
			prestamo.save()
			
			prestamo.cantidadCuotas = math.ceil(prestamo.balance / (prestamo.montoCuotaQ1 + prestamo.montoCuotaQ2)) * prestamo.quincenas

			prestamo.save()
			
			return HttpResponse(1)

		except Exception as e:
			return HttpResponse(e)


#Funcion para devolver las cuentas de un prestamo en especifico
#Parametro : Numero de Prestamo
def getCuentasByPrestamo(self, noPrestamo):

	try:
		refFind = 'PRES' + noPrestamo
		cuentas = DiarioGeneral.objects.filter(referencia=refFind)

		data = list()

		for cuenta in cuentas:
			data.append({
				'cuenta': cuenta.cuenta.codigo,
			})

		return JsonResponse(data, safe=False)
		
	except Exception as e:
		raise Exception(e)

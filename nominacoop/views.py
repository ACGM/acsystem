from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.db import IntegrityError

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import NominasGeneradasSerializer, TiposNominasSerializer, NominaGeneradaDetalleSerializer

from .models import NominaCoopH, NominaCoopD, EmpleadoCoop, TipoNomina
from administracion.models import CuotaAhorroSocio, Socio

import json

# Vista Principal de Nomina
class NominaView(TemplateView):

	template_name = 'nomina.html'


# Listado de Nominas Generadas
class ListadoNominasGeneradasViewSet(viewsets.ModelViewSet):

	queryset = NominaCoopH.objects.all()
	serializer_class = NominasGeneradasSerializer


# Listado de Nominas Generadas
class DetalleNominaGeneradaAPIView(APIView):

	serializer_class = NominaGeneradaDetalleSerializer

	def get(self, request, nomina=None):
		if nomina != None:
			detalleNomina = NominaCoopD.objects.filter(nomina__fechaNomina=nomina)
		else:
			detalleNomina = NominaCoopD.objects.all()

		response = self.serializer_class(detalleNomina, many=True)
		return Response(response.data)


# Listado de Tipos de Nominas
class ListadoTiposNominasViewSet(viewsets.ModelViewSet):

	queryset = TipoNomina.objects.all()
	serializer_class = TiposNominasSerializer


# Generar nomina a partir de la fecha y tipo
class generaNominaView(View):

	def post(self, request, *args, **kwargs):

		try:

			# Tomar los parametros enviados por el Post en JSON
			data = json.loads(request.body)

			#Paso 1: Traer todos los empleados que estaran en el proceso de nomina (activo=True)
			empleados = EmpleadoCoop.objects.filter(activo=True)

			#Paso 2: Crear la cabecera de nomina
			nominaH = NominaCoopH()
			nominaH.fechaNomina = data['fechaNomina']
			nominaH.tipoNomina = TipoNomina.objects.get(id=data['tipoNomina'])
			nominaH.quincena = int(data['quincena'])
			nominaH.nota = data['nota']
			nominaH.userLog = User.objects.get(id=request.user.id)
			nominaH.save()

			#Paso 3: Crear el detalle de nomina por cada empleado
			for empleado in empleados:
				nominaD = NominaCoopD()
				nominaD.nomina = nominaH
				nominaD.empleado = empleado
				nominaD.salario = (empleado.sueldoActual / 2)
				nominaD.isr = 0
				nominaD.afp = 0
				nominaD.ars = 0
				nominaD.cafeteria = 0
				nominaD.vacaciones = 0
				nominaD.otrosingresos = 0

				try:
					socio = Socio.objects.get(codigo=empleado.codigo)
				except socio.DoesNotExist:
					pass

				# try:
				# 	ahorro = CuotaAhorroSocio.objects.get(socio=socio)
				# 	if ahorro != None:
				# 		if quincena == 1:
				# 			montoAhorro = ahorro.cuotaAhorroQ1
				# 		else:
				# 			montoAhorro = ahorro.cuotaAhorroQ2
				# except ahorro.DoesNotExist:
				# 	montoAhorro = 0
				nominaD.descAhorros = 0 #montoAhorro
				
				# try:
				# 	cuotaPrestamo = 0
				# 	prestamos = MaestraPrestamo.objects.filter(socio=socio)
				# 	for prestamo in prestamos:
				# 		cuota = CuotasPrestamo.objects.values('valorCapital','valorInteres').filter(noPrestamo=prestamo.noPrestamo, estatus='P').latest('id')
				# 		capital = cuota.valorCapital 
				# 		interes = cuota.valorInteres
				# 		cuotaPrestamo = capital + interes
				# except prestamos.DoesNotExist:
				# 	cuotaPrestamo = 0
				# except cuota.DoesNotExist:
				# 	cuotaPrestamo = 0

				nominaD.descPrestamos = 0 #cuotaPrestamo
				nominaD.save()
			
			return HttpResponse('TODO BIEN')

		except IntegrityError as ie:
			return HttpResponse('Existe una nomina generada para esta fecha')

		except Exception as e:
			return HttpResponse(e)


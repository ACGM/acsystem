# VIEWS de Nomina

from django.contrib.auth.decorators import login_required
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

from acgm.views import LoginRequiredMixin

import json
import decimal


# Vista Principal de Nomina
class NominaView(LoginRequiredMixin, TemplateView):

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
				nominaD.isr = decimal.Decimal(empleado.sueldoActual / 2) * decimal.Decimal(0.02)
				nominaD.afp = decimal.Decimal(empleado.sueldoActual / 2) * decimal.Decimal(0.032)
				nominaD.ars = decimal.Decimal(empleado.sueldoActual / 2) * decimal.Decimal(0.087)
				nominaD.cafeteria = 0
				nominaD.vacaciones = 0
				nominaD.otrosingresos = 0

				try:
					socio = Socio.objects.get(codigo=empleado.codigo)
				except socio.DoesNotExist:
					pass

				try:
					ahorro = CuotaAhorroSocio.objects.get(socio=socio)
					if ahorro != None:
						if nominaH.quincena == 1:
							montoAhorro = ahorro.cuotaAhorroQ1
						else:
							montoAhorro = ahorro.cuotaAhorroQ2
				except ahorro.DoesNotExist:
					montoAhorro = 0
				nominaD.descAhorros = montoAhorro
				
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
			
			return HttpResponse(nominaH.id)

		except IntegrityError as ie:
			return HttpResponse(-1)

		except Exception as e:
			return HttpResponse(e)


# Guardar Cambios en Detalle de Empleado (nomina generada)
class guardarDetalleEmpleado(View):

	def post(self, request, *args, **kwargs):

		try:

			# Tomar los parametros enviados por el Post en JSON
			data = json.loads(request.body)

			detalle = data['detalle']
			nomina = data['nomina']
			tipoNomina = data['tipoNomina']

			#Paso 1: Tomar la nomina que se esta trabajando
			nominaH = NominaCoopH.objects.get(fechaNomina=nomina, tipoNomina__descripcion=tipoNomina)

			#Paso 2: Tomar el empleado que sera modificado en dicha nomina
			emp = EmpleadoCoop.objects.get(codigo=detalle['codigo'])

			#Paso 3: Tomar el detalle del empleado que sera modificado
			nominaD = NominaCoopD.objects.get(nomina=nominaH, empleado=emp)
			nominaD.salario = detalle['salario'].replace(',','')
			nominaD.isr = detalle['isr'].replace(',','') if detalle['isr'] != None else 0
			nominaD.afp = detalle['afp'].replace(',','') if detalle['afp'] != None else 0
			nominaD.ars = detalle['ars'].replace(',','') if detalle['ars'] != None else 0
			nominaD.cafeteria = detalle['cafeteria'].replace(',','') if detalle['cafeteria'] != None else 0
			nominaD.vacaciones = detalle['vacaciones'].replace(',','') if detalle['vacaciones'] != None else 0
			nominaD.otrosingresos = detalle['otrosIngresos'].replace(',','') if detalle['otrosIngresos'] !=None else 0
			nominaD.save()
			
			return HttpResponse(detalle['codigo'])
			# return HttpResponse(1)

		except IntegrityError as ie:
			return HttpResponse(-1)

		except Exception as e:
			return HttpResponse(e)


# Eliminar nomina
class EliminarNominaView(View):

	def post(self, request, *args, **kwargs):

		try:

			data = json.loads(request.body)

			nomina = data['fechaNomina']
			tipoNomina = data['tipoNomina']

			nominaH = NominaCoopH.objects.filter(fechaNomina=nomina, tipoNomina__descripcion=tipoNomina)
			NominaCoopD.objects.filter(nomina=nominaH).delete()
			nominaH.delete()

			return HttpResponse(1)
		
		except Exception as e:
			return HttpResponse(e)


# Generar archivo
class GenerarArchivoView(View):

	pass


# Postear Nomina Cooperativa
class PostearNominaCoopView(View):

	pass
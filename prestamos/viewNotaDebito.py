# VIEWS de Notas de Debito

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import NotasDebitoListado

from prestamos.models import NotaDeDebitoPrestamo

from acgm.views import LoginRequiredMixin

import json
import math
import decimal
import datetime


# Listado de Notas de Debito
class ListadoNDViewSet(viewsets.ModelViewSet):

	queryset = NotaDeDebitoPrestamo.objects.all()
	serializer_class = NotasDebitoListado


# Guardar Nota de Debito
class guardarNotaDebito(View):

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
			emp = EmpleadoCoop.objects.get(socio__codigo=detalle['codigo'])

			#Paso 3: Tomar el detalle del empleado que sera modificado
			nominaD = NominaCoopD.objects.get(nomina=nominaH, empleado=emp)
			nominaD.salario = detalle['salario'].replace(',','')
			nominaD.isr = detalle['isr'].replace(',','') if detalle['isr'] != None else 0
			nominaD.afp = detalle['afp'].replace(',','') if detalle['afp'] != None else 0
			nominaD.ars = detalle['ars'].replace(',','') if detalle['ars'] != None else 0
			nominaD.cafeteria = detalle['cafeteria'].replace(',','') if detalle['cafeteria'] != None else 0
			nominaD.vacaciones = detalle['vacaciones'].replace(',','') if detalle['vacaciones'] != None else 0
			nominaD.otrosingresos = detalle['otrosIngresos'].replace(',','') if detalle['otrosIngresos'] !=None else 0
			nominaD.horasExtras = detalle['horasExtras'].replace(',','') if detalle['horasExtras'] !=None else 0
			nominaD.save()
			
			return HttpResponse(detalle['codigo'])

		except IntegrityError as ie:
			return HttpResponse(-1)

		except Exception as e:
			return HttpResponse(e)
# VIEWS de Notas de Credito

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import NotasCreditoListado

from prestamos.models import NotaDeCreditoPrestamo, MaestraPrestamo

from acgm.views import LoginRequiredMixin

import json
import math
import decimal
import datetime


# Listado de Notas de Credito
class ListadoNCViewSet(viewsets.ModelViewSet):

	queryset = NotaDeCreditoPrestamo.objects.all().order_by('-id')
	serializer_class = NotasCreditoListado


# Guardar Nota de Credito
class guardarNotaCredito(View):

	def post(self, request, *args, **kwargs):

		try:
			# Tomar los parametros enviados por el Post en JSON
			data = json.loads(request.body)

			noND = data['noND']
			fecha = data['fecha']
			prestamo = data['prestamo']
			vc = data['valorCapital']
			vi = data['valorInteres']
			concepto = data['concepto']

			if noND == 0:
				nd = NotaDeDebitoPrestamo()
			else:
				nd = NotaDeDebitoPrestamo.objects.get(id=noND)

			nd.noPrestamo = MaestraPrestamo.objects.get(noPrestamo=prestamo)
			nd.valorCapital = decimal.Decimal(vc)
			nd.valorInteres = decimal.Decimal(vi)
			nd.concepto = concepto
			nd.userLog = request.user
			nd.save()
			
			return HttpResponse(nd.id)

		except Exception as e:
			return HttpResponse(e)
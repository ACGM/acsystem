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

from prestamos.models import NotaDeDebitoPrestamo, MaestraPrestamo

from acgm.views import LoginRequiredMixin

import json
import math
import decimal
import datetime


# Listado de Notas de Debito
class ListadoNDViewSet(viewsets.ModelViewSet):

	queryset = NotaDeDebitoPrestamo.objects.all().order_by('-id')
	serializer_class = NotasDebitoListado


# Guardar Nota de Debito
class guardarNotaDebito(View):

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


# Desglose de Nota de Debito
class NotaDeDebitoById(LoginRequiredMixin, DetailView):

	queryset = NotaDeDebitoPrestamo.objects.all()

	def get(self, request, *args, **kwargs):
		NoND = self.request.GET.get('nond')

		self.object_list = self.get_queryset().filter(id=NoND)
		return self.json_to_response()
		
	def json_to_response(self):
		data = list()

		for notadebito in self.object_list:
			data.append({
				'fecha': notadebito.fecha,
				'noPrestamo': notadebito.noPrestamo.noPrestamo,
				'categoriaPrestamo': notadebito.noPrestamo.categoriaPrestamo.descripcion,
				'valorCapital': notadebito.valorCapital,
				'valorInteres': notadebito.valorInteres,
				'concepto': notadebito.concepto,
				'estatus': notadebito.estatus,
				'posteado': notadebito.posteado,
				'fechaPosteo': notadebito.fechaPosteo,
				'socio': notadebito.noPrestamo.socio.nombreCompleto,
			})

		return JsonResponse(data, safe=False)
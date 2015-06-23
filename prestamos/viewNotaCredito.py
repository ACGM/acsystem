# VIEWS de Notas de Credito

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import NotasCreditoListado, NotasCreditoEspecialesListado

from prestamos.models import NotaDeCreditoPrestamo, NotaDeCreditoEspecial, MaestraPrestamo, PagoCuotasPrestamo

from acgm.views import LoginRequiredMixin

import json
import math
import decimal
import datetime


# Listado de Notas de Credito
class ListadoNCViewSet(viewsets.ModelViewSet):

	queryset = NotaDeCreditoPrestamo.objects.all().order_by('-id')
	serializer_class = NotasCreditoListado


# Listado de Notas de Credito Especiales
class ListadoNCEViewSet(viewsets.ModelViewSet):

	queryset = NotaDeCreditoEspecial.objects.all().order_by('-id')
	serializer_class = NotasCreditoEspecialesListado


# Guardar Nota de Credito
class guardarNotaCredito(View):

	def post(self, request, *args, **kwargs):

		try:
			# Tomar los parametros enviados por el Post en JSON
			data = json.loads(request.body)

			noNC = float(data['noNC'])
			fecha = data['fecha']
			prestamo = data['prestamo']
			aplicaCuota = data['aplicaCuota']
			vc = data['valorCapital']
			vi = data['valorInteres']
			concepto = data['concepto']

			if noNC == 0:
				nc = NotaDeCreditoPrestamo()
			else:
				nc = NotaDeCreditoPrestamo.objects.get(id=noNC)

			nc.noPrestamo = MaestraPrestamo.objects.get(noPrestamo=prestamo)
			nc.aplicadoACuota = PagoCuotasPrestamo.objects.get(id=aplicaCuota)
			nc.valorCapital = decimal.Decimal(vc)
			nc.valorInteres = decimal.Decimal(vi)
			nc.concepto = concepto
			nc.userLog = request.user
			nc.save()
			
			return HttpResponse(nc.id)

		except Exception as e:
			return HttpResponse(e)


# Desglose de Nota de Credito
class NotaDeCreditoById(LoginRequiredMixin, DetailView):

	queryset = NotaDeCreditoPrestamo.objects.all()

	def get(self, request, *args, **kwargs):
		NoNC = self.request.GET.get('nonc')

		self.object_list = self.get_queryset().filter(id=NoNC)
		return self.json_to_response()
		
	def json_to_response(self):
		data = list()

		for notacredito in self.object_list:
			data.append({
				'fecha': notacredito.fecha,
				'aplicadoACuota': notacredito.aplicadoACuota.id,
				'noPrestamo': notacredito.noPrestamo.noPrestamo,
				'valorCapital': notacredito.valorCapital,
				'valorInteres': notacredito.valorInteres,
				'concepto': notacredito.concepto,
				'estatus': notacredito.estatus,
				'posteado': notacredito.posteado,
				'fechaPosteo': notacredito.fechaPosteo,
			})

		return JsonResponse(data, safe=False)
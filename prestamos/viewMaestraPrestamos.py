# VIEWS de Maestra de Prestamos
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, JsonResponse

from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import MaestraPrestamosListadoSerializer

from .models import MaestraPrestamo
from administracion.models import CategoriaPrestamo, Cobrador, Representante, Socio, Autorizador

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

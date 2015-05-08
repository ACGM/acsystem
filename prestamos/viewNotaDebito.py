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
	
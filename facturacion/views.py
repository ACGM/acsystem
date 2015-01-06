from django.shortcuts import render

from django.views.generic import TemplateView

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ListadoFacturasSerializer
from .models import Factura

class FacturacionView(TemplateView):

	template_name = 'facturacion.html'


# Listado de Facturas registradas
class ListadoFacturasViewSet(viewsets.ModelViewSet):

	queryset = Factura.objects.all()
	serializer_class = ListadoFacturasSerializer

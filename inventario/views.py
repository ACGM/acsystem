from django.shortcuts import render

from django.views.generic import TemplateView, ListView

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import InventarioH, InventarioD
from .serializers import EntradasInventarioSerializer


class InventarioView(TemplateView):

	template_name = 'inventario.html'


class TransferenciaInvView(TemplateView):

	template_name = 'transferenciainv.html'


# Listado de Entradas de inventario
class ListadoEntradasInvView(viewsets.ModelViewSet):

	queryset = InventarioH.objects.all() #.order_by('-id')
	serializer_class = EntradasInventarioSerializer
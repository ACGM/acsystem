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
class ListadoEntradasInvView(APIView):

	serialized = EntradasInventarioSerializer

	def get(self, request, posteo=None, format=None):
		if posteo != None:
			listado = InventarioH.objects.filter(posteo=posteo).order_by('-id')
		else:
			listado = InventarioH.objects.all().order_by('-id')

		response = self.serialized(listado, many=True)
		
		return Response(response.data)

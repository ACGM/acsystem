from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import InventarioH, InventarioD, Almacen
from administracion.models import Suplidor, Producto
from .serializers import EntradasInventarioSerializer, AlmacenesSerializer

import json
import math


class InventarioView(TemplateView):

	template_name = 'inventario.html'

	# @login_required
	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			dataH = data['cabecera']
			dataD = data['detalle']
			almacen = data['almacen']


			suplidor = Suplidor.objects.get(id = int(dataH['suplidor']))
			usuario = User.objects.get(username = dataH['userlog'])

			invH = InventarioH()

			invH.fecha = dataH['fecha']
			invH.orden = dataH['orden']
			invH.factura = dataH['factura']
			invH.diasPlazo = dataH['diasPlazo']
			invH.nota = dataH['nota']
			invH.ncf = dataH['ncf']
			invH.suplidor = suplidor
			invH.userLog = usuario
			invH.save()


			for i in dataD:
				invD = InventarioD()
				invD.inventario = invH
				invD.producto = Producto.objects.get(id=i['id'])
				invD.almacen = Almacen.objects.get(id=almacen)
				invD.cantidadTeorico = i['cantidad']
				invD.costo = float(i['costo'])
				invD.save()

			return HttpResponse('1')

		except Exception as e:
			return HttpResponse(e)



class TransferenciaInvView(TemplateView):

	template_name = 'transferenciainv.html'


# Listado de Entradas de inventario
class ListadoEntradasInvView(viewsets.ModelViewSet):

	queryset = InventarioH.objects.all()
	serializer_class = EntradasInventarioSerializer


# Listado de Almacenes
class ListadoAlmacenesView(viewsets.ModelViewSet):

	queryset = Almacen.objects.all()
	serializer_class = AlmacenesSerializer

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse


from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ListadoFacturasSerializer

from .models import Factura, Detalle
from administracion.models import Producto, Socio
from inventario.models import Existencia, Almacen

import json
import math


# Eliminar producto de la factura
def quitar_producto(self, idProd, iCantidad, iAlmacen):
	try:

		exist = Existencia.objects.get(producto = Producto.objects.get(codigo = idProd), almacen = Almacen.objects.get(id = iAlmacen))
		exist.cantidad -= float(iCantidad)
		exist.save()
	except Existencia.DoesNotExist:
		return HttpResponse('No hay existencia para el producto ' + str(idProd))


# Vista para presentar la pantalla de facturacion y a la vez contiene el POST para guardar la factura.
class FacturacionView(TemplateView):

	template_name = 'facturacion.html'

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			dataH = data['cabecera']
			dataD = data['detalle']
			almacen = dataH['almacen']

			facturaNo = dataH['factura']
			usuario = User.objects.get(username = dataH['vendedor'])
			if dataH['socio'] != None:
				socio = Socio.objects.get(codigo = dataH['socio'])


			if facturaNo > 0:
				fact = Factura.objects.get(noFactura = facturaNo)
				
				for item in dataD:
					quitar_producto(self, item['codigo'], item['cantidad'], almacen)

				detalle = Detalle.objects.filter(factura_nofactura = facturaNo).delete()

			else:
				try:
					fact = Factura()
					fact.noFactura = Factura.objects.latest('noFactura').noFactura + 1
				except Factura.DoesNotExist:
					fact.noFactura = 1

			fact.fecha = dataH['fecha']
			fact.terminos = dataH['terminos']
			fact.userLog = usuario

			if socio != None: fact.socio = socio
			# fact.ordenCompra =

			fact.save()

			for item in dataD:
				detalle = Detalle()
				detalle.factura = fact
				detalle.producto = Producto.objects.get(codigo = item['codigo'])
				detalle.porcentajeDescuento = item['descuento']
				detalle.cantidad = item['cantidad']
				detalle.precio = float(item['costo'])
				detalle.almacen = Almacen.objects.get(id=almacen)
				detalle.save()

			return HttpResponse('1')

		except Exception as e:
			return HttpResponse(e)


# Listado de Facturas registradas
class ListadoFacturasViewSet(viewsets.ModelViewSet):

	queryset = Factura.objects.all()
	serializer_class = ListadoFacturasSerializer

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, ListView, DetailView

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import InventarioH, InventarioD, Almacen, Existencia
from administracion.models import Suplidor, Producto

from .serializers import EntradasInventarioSerializer, AlmacenesSerializer, EntradaInventarioByIdSerializer, \
							ExistenciaProductoSerializer

import json
import math
import decimal


# Retornar un documento con todo su detalle 
class EntradaInventarioById(ListView):

	queryset = InventarioH.objects.all()

	def get(self, request, *args, **kwargs):
		NoDoc = self.request.GET.get('nodoc')
		
		self.object_list = self.get_queryset().filter(id=NoDoc)

		format = self.request.GET.get('format')
		if format == 'json':
			return self.json_to_response()

		context = self.get_context_data()
		return self.render_to_response(context)

	def json_to_response(self):
		data = list()

		for inventario in self.object_list:
			data.append({
				'id': inventario.id,
				'suplidorId': inventario.suplidor.id,
				'suplidorName': inventario.suplidor.nombre,
				'factura': inventario.factura,
				'orden': inventario.orden,
				'ncf': inventario.ncf,
				'fecha': inventario.fecha,
				'condicion': inventario.condicion,
				'diasPlazo': inventario.diasPlazo,
				'nota': inventario.nota,
				'posteo': inventario.posteo,
				'usuario': inventario.userLog.username,
				'productos': [ 
					{	'codigo': prod.producto.codigo,
						'descripcion': prod.producto.descripcion,
						'unidad': prod.producto.unidad.descripcion,
						'cantidad': prod.cantidadTeorico,
						'cantidadAnterior': float(Existencia.objects.filter(producto__codigo=prod.producto.codigo, almacen=prod.almacen.id).values('cantidadAnterior')[0]['cantidadAnterior']) 
												if Existencia.objects.filter(producto=prod, almacen=prod.almacen.id).values('cantidadAnterior') != None else 0,
						'costo': prod.costo,
						'almacen': prod.almacen.id,
					} 
					for prod in InventarioD.objects.filter(inventario=inventario.id)]
				})

		return JsonResponse(data, safe=False)


# Eliminar producto del inventario
def quitar_producto(self, idProd, iCantidad, iAlmacen):
	try:

		exist = Existencia.objects.get(producto = Producto.objects.get(codigo = idProd), almacen = Almacen.objects.get(id = iAlmacen))
		exist.cantidad -= float(iCantidad)
		exist.save()
	except Existencia.DoesNotExist:
		return HttpResponse('No hay existencia para el producto ' + str(idProd))



# Entrada de Inventario
class InventarioView(TemplateView):

	template_name = 'inventario.html'

	# @login_required
	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			dataH = data['cabecera']
			dataD = data['detalle']
			almacen = data['almacen']

			entradaNo = dataH['entradaNo']
			suplidor = Suplidor.objects.get(id = int(dataH['suplidor']))
			usuario = User.objects.get(username = dataH['userlog'])

			if entradaNo > 0:
				invH = InventarioH.objects.get(id = entradaNo)
				
				for item in dataD:
					quitar_producto(self, item['codigo'], item['cantidad'], data['almacen'])

				invD = InventarioD.objects.filter(inventario_id = invH.id).delete()

			else:
				invH = InventarioH()

			invH.fecha = dataH['fecha']
			invH.orden = dataH['orden']
			invH.factura = dataH['factura']
			invH.diasPlazo = dataH['diasPlazo']
			invH.nota = dataH['nota']
			invH.ncf = dataH['ncf']
			invH.condicion = dataH['condicion']
			invH.suplidor = suplidor
			invH.userLog = usuario
			invH.save()


			for item in dataD:
				invD = InventarioD()
				invD.inventario = invH
				invD.producto = Producto.objects.get(codigo = item['codigo'])
				invD.almacen = Almacen.objects.get(id=almacen)
				invD.cantidadTeorico = decimal.Decimal(item['cantidad'])
				invD.costo = decimal.Decimal(item['costo'])
				invD.save()

			return HttpResponse('1')

		except Exception as e:
			return HttpResponse(e)


# Transferencia de Inventario
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


# Existencia de un producto en especifico
class getExistenciaByProductoView(APIView):

	serializer_class = ExistenciaProductoSerializer

	def get(self, request, codProd, almacen):
		existencia = Existencia.objects.filter(producto__codigo=codProd, almacen_id=almacen)

		response = self.serializer_class(existencia, many=True)
		return Response(response.data)


#Imprimir Entrada de Inventario
class ImprimirEntradaInventarioView(TemplateView):

	template_name = 'print_entrada.html'

# VIEWS de Inventario

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Count
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, ListView, DetailView

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import InventarioH, InventarioD, Almacen, Existencia, AjusteInventarioH, AjusteInventarioD
from administracion.models import Suplidor, Producto

from .serializers import EntradasInventarioSerializer, AlmacenesSerializer, EntradaInventarioByIdSerializer, \
							ExistenciaProductoSerializer, AjustesInventarioSerializer

from acgm.views import LoginRequiredMixin

import json
import math
import decimal
import datetime


# Transferencia de Inventario
class TransferenciaInvView(LoginRequiredMixin, TemplateView):

	template_name = 'transferenciainv.html'


# Imprimir Entrada de Inventario
class ImprimirEntradaInventarioView(LoginRequiredMixin, TemplateView):

	template_name = 'print_entrada.html'


# Reporte de Entrada/Salida de Articulo(s)
class RPTEntradaSalidaArticuloView(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_EntradaSalidaArticulo.html'


# Reporte de Existencia de Articulo(s)
class RPTExistenciaArticuloView(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_ExistenciaArticulo.html'


# Listado de Ajustes de inventario
class ListadoAjustesInvView(viewsets.ModelViewSet):

	queryset = AjusteInventarioH.objects.all().order_by('id')
	serializer_class = AjustesInventarioSerializer


# Listado de Entradas de inventario
class ListadoEntradasInvView(viewsets.ModelViewSet):

	queryset = InventarioH.objects.all()
	serializer_class = EntradasInventarioSerializer


# Listado de Almacenes
class ListadoAlmacenesView(viewsets.ModelViewSet):

	queryset = Almacen.objects.all()
	serializer_class = AlmacenesSerializer


# Retornar un documento con todo su detalle 
class EntradaInventarioById(LoginRequiredMixin, ListView):

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
				'tipo': inventario.getTipo,
				'numeroSalida': inventario.numeroSalida,
				'descripcionSalida': inventario.descripcionSalida,
				'fechaSalida': inventario.fechaSalida,
				'usuarioSalida': inventario.usuarioSalida.username if inventario.usuarioSalida != None else '',
				'productos': [ 
					{	'codigo': prod.producto.codigo,
						'descripcion': prod.producto.descripcion,
						'unidad': prod.producto.unidad.descripcion,
						'cantidad': prod.cantidadTeorico,
						'cantidadAnterior': float(Existencia.objects.filter(producto__codigo=prod.producto.codigo, almacen=prod.almacen.id).values('cantidadAnterior')[0]['cantidadAnterior']) 
												if Existencia.objects.filter(producto=prod, almacen=prod.almacen.id).values('cantidadAnterior') != None else 0,
						'costo': prod.costo,
						'almacen': prod.almacen.id,
						'almacenDescrp': prod.almacen.descripcion,
					} 
					for prod in InventarioD.objects.filter(inventario=inventario.id)]
				})

		return JsonResponse(data, safe=False)


# Eliminar producto del inventario
def quitar_producto(self, idProd, iCantidad, iAlmacen):
	try:

		exist = Existencia.objects.get(producto = Producto.objects.get(codigo = idProd), almacen = Almacen.objects.get(id = iAlmacen))
		exist.cantidad -= decimal.Decimal(iCantidad)
		exist.save()
	except Existencia.DoesNotExist:
		return HttpResponse('No hay existencia para el producto ' + str(idProd))


# Entrada de Inventario
class InventarioView(LoginRequiredMixin, TemplateView):

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


# Ajuste de Inventario
class AjusteInvView(LoginRequiredMixin, TemplateView):

	template_name = 'ajusteInv.html'

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			dataH = data['cabecera']
			dataD = data['detalle']
			fecha = data['fecha']

			numero = dataH['numero']

			if numero > 0:
				ajusteH = AjusteInventarioH.objects.get(id = numero)
			else:
				ajusteH = AjusteInventarioH()

			ajusteH.fecha = fecha
			ajusteH.notaAjuste = dataH['notaAjuste']
			ajusteH.usuario = User.objects.get(username=request.user.username)
			ajusteH.save()

			for item in dataD:
				ajusteD = AjusteInventarioD()
				ajusteD.ajusteInvH = ajusteH
				ajusteD.producto = Producto.objects.get(codigo = item['codigo'])
				ajusteD.almacen = Almacen.objects.get(id = item['almacen'] )
				ajusteD.cantidadFisico = decimal.Decimal(item['cantidad'])
				ajusteD.cantidadTeorico = decimal.Decimal(item['cantidadTeorico'])
				ajusteD.save()

			return HttpResponse('1')

		except Exception as e:
			return HttpResponse(e)


# Existencia de un producto en especifico
class getExistenciaByProductoView(APIView):

	serializer_class = ExistenciaProductoSerializer

	def get(self, request, codProd, almacen):
		existencia = Existencia.objects.filter(producto__codigo=codProd, almacen_id=almacen)

		response = self.serializer_class(existencia, many=True)
		return Response(response.data)


# Existencia productos (filtro: Almacen)
class getExistenciaRPT(ListView):

	queryset = Existencia.objects.all().values('producto__descripcion','producto__codigo','producto__categoria__descripcion','almacen__descripcion')\
										.annotate(total=Sum('cantidad')).order_by('producto__categoria__descripcion','producto__descripcion')
	def get(self, request, *args, **kwargs):
		
		almacen = self.request.GET.get('almacen')
		format = self.request.GET.get('format')
		producto = self.request.GET.get('producto')

		if producto != None:
			# Busqueda para tipo producto
			if almacen != None:
				if producto != None:
					self.object_list = self.get_queryset().filter(almacen=almacen, producto__descripcion__contains=producto)
				else:
					self.object_list = self.get_queryset().filter(almacen=almacen)
			else:
				self.object_list = self.get_queryset().filter(producto__descripcion__contains=producto)

		else:
			# Busqueda para tipo categoria
			if self.request.GET.get('categorias') != None:
				categoriasList = list(self.request.GET.get('categorias'))
				categorias = list()

				for categoria in categoriasList:
					if categoria != ',':
						categorias.append(categoria)

				if almacen != None:
					if categorias != None:
						self.object_list = self.get_queryset().filter(almacen=almacen, producto__categoria__id__in=categorias)
					else:
						self.object_list = self.get_queryset().filter(almacen=almacen)
				else:
					if categorias != None:
						self.object_list = self.get_queryset().filter(producto__categoria__id__in=categorias)
			else:
				self.object_list = self.get_queryset()

		if format == 'json':
			return self.json_to_response()

		context = self.get_context_data()
		return self.render_to_response(context)

	def json_to_response(self):
		data = list()

		for existencia in self.object_list:
			data.append({
				'categoria': existencia['producto__categoria__descripcion'],
				'codigo': existencia['producto__codigo'],
				'producto': existencia['producto__descripcion'],
				'almacen': existencia['almacen__descripcion'] if existencia['almacen__descripcion'] != None else '',
				'total': existencia['total'],
				})

		return JsonResponse(data, safe=False)


# Salida de Inventario
class SalidaInventarioView(TemplateView):

	template_name = 'inventario.html'

	# @login_required
	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			nota = data['nota']
			entradaNo = int(data['entradaNo'])

			# Traer el ultimo numero de Salida para incrementar
			lastNum = InventarioH.objects.latest('numeroSalida').numeroSalida

			invH = InventarioH.objects.get(id=entradaNo)
			invH.numeroSalida = lastNum + 1
			invH.descripcionSalida = nota
			invH.fechaSalida = datetime.datetime.now()
			invH.usuarioSalida = User.objects.get(username=request.user)
			invH.save()

			invD = InventarioD.objects.filter(inventario=invH)

			for item in invD:
				d = InventarioD.objects.get(id=item.id)
				d.tipoAccion = 'S'
				d.save()

			return HttpResponse(1)

		except Exception as e:
			return HttpResponse(e)
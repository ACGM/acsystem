# VIEWS de Inventario

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Count
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, ListView, DetailView, View

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import InventarioH, InventarioD, Almacen, Existencia, AjusteInventarioH, AjusteInventarioD, \
					TransferenciasAlmacenes, InventarioHSalidas, Movimiento

from administracion.models import Suplidor, Producto

from .serializers import EntradasInventarioSerializer, AlmacenesSerializer, EntradaInventarioByIdSerializer, \
							ExistenciaProductoSerializer, AjustesInventarioSerializer, TransferenciasAlmacenesSerializer, \
							SalidasInventarioSerializer, MovimientoProductoSerializer

from acgm.views import LoginRequiredMixin

import json
import math
import decimal
import datetime


# Imprimir Entrada de Inventario
class ImprimirEntradaInventarioView(LoginRequiredMixin, TemplateView):

	template_name = 'print_entrada.html'


# Reporte de Movimiento de Articulo(s)
class RPTMovimientoArticuloView(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_HistMovArt.html'


# Reporte de Existencia de Articulo(s)
class RPTExistenciaArticuloView(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_ExistenciaArticulo.html'


# Reporte para Conteo Fisico de Articulos
class RPTConteoFisicoArticuloView(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_ConteoFisico.html'


# Reporte Ajuste de Inventario
class RPTAjusteInventarioView(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_AjusteInv.html'


# Listado de Ajustes de inventario
class ListadoAjustesInvView(viewsets.ModelViewSet):

	queryset = AjusteInventarioH.objects.all().order_by('-id')
	serializer_class = AjustesInventarioSerializer


# Listado de Ajustes de inventario
class ListadoTransfInvView(viewsets.ModelViewSet):

	queryset = TransferenciasAlmacenes.objects.all().order_by('-id')
	serializer_class = TransferenciasAlmacenesSerializer


# Listado de Entradas de inventario
class ListadoEntradasInvView(viewsets.ModelViewSet):

	queryset = InventarioH.objects.all()
	serializer_class = EntradasInventarioSerializer


# Listado de Salidas de inventario
class ListadoSalidasInvView(viewsets.ModelViewSet):

	queryset = InventarioHSalidas.objects.all()
	serializer_class = SalidasInventarioSerializer


# Listado de Almacenes
class ListadoAlmacenesView(viewsets.ModelViewSet):

	queryset = Almacen.objects.all()
	serializer_class = AlmacenesSerializer


# # # # # # # # # # # # # # # # # # # # # # # # # # #
# Retornar un documento con todo su detalle (ENTRADA)
# # # # # # # # # # # # # # # # # # # # # # # # # # #
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
				'borrado': inventario.borrado,
				'borradoPor': inventario.borradoPor.username if inventario.borrado == True else '',
				'borradoFecha': inventario.borradoFecha if inventario.borrado == True else '',
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


# # # # # # # # # # # # # # # # # # # # # # # # # # #
# Retornar un documento con todo su detalle (SALIDA)
# # # # # # # # # # # # # # # # # # # # # # # # # # #
class SalidaInventarioById(LoginRequiredMixin, ListView):

	queryset = InventarioHSalidas.objects.all()

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
				'fecha': inventario.fecha,
				'descripcionSalida': inventario.descripcionSalida,
				'usuarioSalida': inventario.usuarioSalida.username,
				'posteo': inventario.posteo,
				'datetimeServer': inventario.datetimeServer,
				'borrado': inventario.borrado,
				'borradoPor': inventario.borradoPor.username if inventario.borrado == True else '',
				'borradoFecha': inventario.borradoFecha if inventario.borrado == True else '',
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
					for prod in InventarioD.objects.filter(inventarioSalida=inventario.id)]
				})

		return JsonResponse(data, safe=False)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Retornar un ajuste de inventario con todo su detalle
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class AjusteInventarioById(LoginRequiredMixin, ListView):

	queryset = AjusteInventarioH.objects.all()

	def get(self, request, *args, **kwargs):
		NoDoc = self.request.GET.get('numero')
		
		self.object_list = self.get_queryset().filter(id=NoDoc)

		format = self.request.GET.get('format')
		if format == 'json':
			return self.json_to_response()

		context = self.get_context_data()
		return self.render_to_response(context)

	def json_to_response(self):
		data = list()

		for ajuste in self.object_list:
			data.append({
				'id': ajuste.id,
				'fecha': ajuste.fecha,
				'notaAjuste': ajuste.notaAjuste,
				'estatus': ajuste.estatus,
				'usuario': ajuste.usuario.username,
				'datetimeServer': ajuste.datetimeServer,
				'productos': [ 
					{	'codigo': ajusteD.producto.codigo,
						'descripcion': ajusteD.producto.descripcion,
						'unidad': ajusteD.producto.unidad.descripcion,
						'almacen': ajusteD.almacen.id,
						'almacenDescrp': ajusteD.almacen.descripcion,
						'cantidad': ajusteD.cantidadFisico,
						'cantidadTeorico': ajusteD.cantidadTeorico,
					} 
					for ajusteD in AjusteInventarioD.objects.filter(ajusteInvH=ajuste.id)]
				})

		return JsonResponse(data, safe=False)


# Eliminar producto del inventario
def quitar_producto(self, codProd, idAlmacen, entradaNo):
	try:
		exist = Existencia.objects.get(producto__codigo=codProd, almacen__id=idAlmacen)
		entrada = InventarioD.objects.get(inventario=entradaNo, producto__codigo=codProd, almacen__id=idAlmacen)

		exist.cantidad -= decimal.Decimal(entrada.cantidadTeorico)
		exist.save()
	except Existencia.DoesNotExist:
		return HttpResponse('No hay existencia para el producto ' + str(codProd))


# Reponer producto del inventario
def reponer_producto(self, codProd, idAlmacen, salidaNo):
	try:
		exist = Existencia.objects.get(producto__codigo=codProd, almacen__id=idAlmacen)

		try:
			salida = InventarioD.objects.get(inventarioSalida=salidaNo, producto__codigo=codProd, almacen__id=idAlmacen)
			exist.cantidad += decimal.Decimal(salida.cantidadTeorico)
			exist.save()
		except InventarioD.DoesNotExist:
			pass

	except Existencia.DoesNotExist:
		return HttpResponse('No se pudo reponer la existencia del producto ' + str(codProd))




# # # # # # # # # # # # # # # # # # # # # # #
# Entrada de Inventario
# # # # # # # # # # # # # # # # # # # # # # #
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
					quitar_producto(self, item['codigo'], data['almacen'], entradaNo)

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


# # # # # # # # # # # # # # # # # # # # # # #
# Eliminar Entrada de Inventario
# # # # # # # # # # # # # # # # # # # # # # #
class InventarioEliminarView(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)
			entradaNo = int(data['entradaNo'])

			invH = InventarioH.objects.get(id=entradaNo)
			dataD = InventarioD.objects.filter(inventario=invH)

			for item in dataD:
				quitar_producto(self, item.producto.codigo, item.almacen.id, entradaNo)

				mov = Movimiento()
				mov.producto = item.producto
				mov.cantidad = decimal.Decimal(InventarioD.objects.get(inventario__id=entradaNo).cantidadTeorico) * -1
				mov.almacen = item.almacen
				mov.documento = 'EINV'
				mov.documentoNo = entradaNo
				mov.tipo_mov = 'E'
				mov.userLog = request.user
				mov.save()
			
			invH.borrado = True
			invH.borradoPor = request.user
			invH.borradoFecha = datetime.datetime.now()
			invH.save()

			return HttpResponse('1')

		except Exception as e:
			return HttpResponse(e)


# # # # # # # # # # # # # # # # # # # # # # #
# Salida de Inventario
# # # # # # # # # # # # # # # # # # # # # # #
class InventarioSalidaView(LoginRequiredMixin, TemplateView):

	template_name = 'inventariosalida.html'

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			dataH = data['cabecera']
			dataD = data['detalle']
			almacen = data['almacen']
			salidaNo = int(dataH['salidaNo'])

			if salidaNo > 0:
				invH = InventarioHSalidas.objects.get(id=salidaNo)

				#Validar si la cantidad de salida no excede la existente
				for item in dataD:
					if item['cantidad'] > InventarioD.objects.get(inventarioSalida=invH, producto__codigo=item['codigo']):
						raise Exception('La cantidad digitada al producto : ' + item['codigo'] + ' es mayor a la existencia actual') 
				#Fin Validacion
				
				for item in dataD:
					reponer_producto(self, item['codigo'], data['almacen'], salidaNo)

				invD = InventarioD.objects.filter(inventarioSalida_id=invH.id).delete()

			else:
				invH = InventarioHSalidas()

			invH.descripcionSalida = dataH['nota']
			invH.usuarioSalida = request.user
			invH.save()

			#Verificar si tiene existencia para dar salida
			for item in dataD:
				try:
					if decimal.Decimal(Existencia.objects.get(producto__codigo=item['codigo'], almacen__id=almacen).cantidad) < decimal.Decimal(item['cantidad']):
						raise Exception('La salida que esta intentando realizar sobre el producto: ' + item['codigo'] + ' sobrepasa lo que tiene en existencia.')
				except Existencia.DoesNotExist:
					raise Exception('El producto ' + item['codigo'] + ' no tiene existencia para el almacen seleccionado.')

			# Llevar a cabo la accion
			for item in dataD:
				invD = InventarioD()
				invD.inventarioSalida = invH
				invD.producto = Producto.objects.get(codigo = item['codigo'])
				invD.almacen = Almacen.objects.get(id=almacen)
				invD.cantidadTeorico = decimal.Decimal(item['cantidad'])
				invD.costo = decimal.Decimal(item['costo'])
				invD.tipoAccion = 'S'
				invD.save()
				
			return HttpResponse('1')

		except Exception as e:
			return HttpResponse(e)


# # # # # # # # # # # # # # # # # # # # # # #
# Eliminar Salida de Inventario
# # # # # # # # # # # # # # # # # # # # # # #
class InventarioSalidaEliminarView(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)
			salidaNo = int(data['salidaNo'])

			invH = InventarioHSalidas.objects.get(id=salidaNo)
			dataD = InventarioD.objects.filter(inventarioSalida=invH)

			for item in dataD:
				reponer_producto(self, item.producto.codigo, item.almacen.id, salidaNo)

				mov = Movimiento()
				mov.producto = item.producto
				mov.cantidad = decimal.Decimal(InventarioD.objects.get(inventarioSalida__id=salidaNo).cantidadTeorico) * -1
				mov.almacen = item.almacen
				mov.documento = 'SINV'
				mov.documentoNo = salidaNo
				mov.tipo_mov = 'S'
				mov.userLog = request.user
				mov.save()
			
			invH.borrado = True
			invH.borradoPor = request.user
			invH.borradoFecha = datetime.datetime.now()
			invH.save()

			return HttpResponse('1')

		except Exception as e:
			return HttpResponse(e)


# # # # # # # # # # # # # # # # # # # # # # #
# Transferencia de Inventario
# # # # # # # # # # # # # # # # # # # # # # #
class TransferenciaInvView(LoginRequiredMixin, TemplateView):

	template_name = 'transferenciainv.html'

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			almacenOrigen = data['almacenOrigen']
			almacenDestino = data['almacenDestino']
			producto = data['producto']
			cantidadTransferir = data['cantidadTransferir']

			# Restar al almacen ORIGEN
			existOrigen = Existencia.objects.get(producto__codigo=producto, almacen__id=almacenOrigen)
			existOrigen.cantidadAnterior = existOrigen.cantidad
			existOrigen.cantidad = existOrigen.cantidad - decimal.Decimal(cantidadTransferir)
			existOrigen.save()

			# Sumar al almacen DESTINO
			try:				
				existDestino = Existencia.objects.get(producto__codigo=producto, almacen__id=almacenDestino)
				existDestino.cantidadAnterior = existDestino.cantidad
				existDestino.cantidad = existDestino.cantidad + decimal.Decimal(cantidadTransferir)
				
			except Existencia.DoesNotExist:
				existDestino = Existencia()
				existDestino.producto = Producto.objects.get(codigo=producto)
				existDestino.almacen = Almacen.objects.get(id=almacenDestino)
				existDestino.cantidadAnterior = 0
				existDestino.cantidad = decimal.Decimal(cantidadTransferir)

			existDestino.save()

			# Registrar transferencia en la tabla de transferenciasAlmacenes
			transf = TransferenciasAlmacenes()
			transf.desdeAlmacen = Almacen.objects.get(id=almacenOrigen)
			transf.hastaAlmacen = Almacen.objects.get(id=almacenDestino)
			transf.producto = Producto.objects.get(codigo=producto)
			transf.cantidad = cantidadTransferir
			transf.userLog = User.objects.get(username=request.user.username)
			transf.save()

			return HttpResponse('1')

		except Exception as e:
			return HttpResponse(e)


# # # # # # # # # # # # # # # # # # # # # # #
# Ajuste de Inventario
# # # # # # # # # # # # # # # # # # # # # # #
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
				ajusteD = AjusteInventarioD.objects.filter(ajusteInvH=ajusteH).delete()
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


# # # # # # # # # # # # # # # # # # # # # # #
# Procesar Ajuste de Inventario 
# (Este proceso es uno de los mas delicados 
#   ya que reemplaza los valores en Existencia)
# # # # # # # # # # # # # # # # # # # # # # #
class ProcesarAjusteInvView(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			ajusteNo = int(data['ajusteNo'])

			for item in AjusteInventarioD.objects.filter(ajusteInvH__id=ajusteNo):
				exist = Existencia.objects.get(producto=item.producto, almacen=item.almacen)
				exist.cantidadAnterior = exist.cantidad
				exist.cantidad = item.cantidadFisico
				exist.save()

				mov = Movimiento()
				mov.producto = item.producto
				mov.cantidad = item.cantidadFisico
				mov.precio = item.producto.precio
				mov.almacen = item.almacen
				mov.documento = 'AINV'
				mov.documentoNo = ajusteNo
				mov.tipo_mov = 'E'
				mov.userLog = request.user
				mov.save()

			ajusteH = AjusteInventarioH.objects.get(id=ajusteNo)
			ajusteH.estatus = 'S'
			ajusteH.save()

			return HttpResponse('1')

		except Exception as e:
			return HttpResponse(e)


# # # # # # # # # # # # # # # # # # # # # # #
# Existencia de un producto en especifico
# # # # # # # # # # # # # # # # # # # # # # #
class getExistenciaByProductoView(APIView):

	serializer_class = ExistenciaProductoSerializer

	def get(self, request, codProd, almacen):
		existencia = Existencia.objects.filter(producto__codigo=codProd, almacen_id=almacen)

		response = self.serializer_class(existencia, many=True)
		return Response(response.data)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Movimiento de un producto en especifico en un rango de fecha
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class RPTMovimientoProductoAPIView(APIView):

	serializer_class = MovimientoProductoSerializer

	def get(self, request, codProd, fechaInicio, fechaFin, almacen):
		movimientos = Movimiento.objects.filter(producto__codigo=codProd, fechaMovimiento__range=(fechaInicio, fechaFin), \
												almacen__id=almacen).order_by('fechaMovimiento')

		response = self.serializer_class(movimientos, many=True)
		return Response(response.data)


# # # # # # # # # # # # # # # # # # # # # # #
# Existencia productos (filtro: Almacen)
# # # # # # # # # # # # # # # # # # # # # # #
class getExistenciaRPT(ListView):

	queryset = Existencia.objects.all().values('producto__descripcion','producto__codigo','producto__categoria__descripcion')\
										.annotate(totalCantidad=Sum('cantidad'),totalCosto=Sum('producto__costo')).order_by('producto__categoria__descripcion','producto__descripcion')
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
				categoriasList = self.request.GET.get('categorias').split(',')
				categorias = list()

				for categoria in categoriasList:
					if categoria != '':
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
				'totalCantidad': existencia['totalCantidad'],
				'totalCosto': existencia['totalCosto'],
				})

		return JsonResponse(data, safe=False)


# # # # # # # # # # # # # # # # # # # # # # #
# Existencia productos para Conteo Fisico
# # # # # # # # # # # # # # # # # # # # # # #
class getExistenciaConteoFisicoRPT(ListView):

	queryset = Producto.objects.all().order_by('categoria__descripcion','descripcion')

	def get(self, request, *args, **kwargs):
		
		format = self.request.GET.get('format')

		categoriasList = self.request.GET.get('categorias').split(',')
		categorias = list()

		for categoria in categoriasList:
			if categoria != '':
				categorias.append(int(categoria))

		self.object_list = self.get_queryset().filter(categoria__id__in=categorias)

		if format == 'json':
			return self.json_to_response()

		context = self.get_context_data()
		return self.render_to_response(context)

	def json_to_response(self):
		data = list()

		almacen = self.request.GET.get('almacen')

		for producto in self.object_list:
			cantidad = 0
			
			if almacen == '*':
				existAll = Existencia.objects.filter(producto__codigo=producto.codigo).values('producto').annotate(totalCantidad=Sum('cantidad'))
				cantidad = existAll[0]['totalCantidad']

			else:
				try:
					exist = Existencia.objects.get(producto__codigo=producto.codigo, almacen__id=almacen)
					cantidad = exist.cantidad
				except Existencia.DoesNotExist:
					pass

			data.append({
				'categoria': producto.categoria.descripcion,
				'codigo': producto.codigo,
				'producto': producto.descripcion,
				'totalCantidad': cantidad
				})

		return JsonResponse(data, safe=False)

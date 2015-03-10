# VIEWS de Facturacion

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, JsonResponse


from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ListadoFacturasSerializer, DetalleFacturasSerializer

from .models import Factura, Detalle
from administracion.models import Producto, Socio, CategoriaPrestamo
from inventario.models import Existencia, Almacen
from prestamos.models import SolicitudOrdenDespachoH

from acgm.views import LoginRequiredMixin

import json
import math
import decimal

# Eliminar producto de la factura
def quitar_producto(self, codProd, iAlmacen, noFactura):
	try:

		exist = Existencia.objects.get(producto__codigo=codProd, almacen__id=iAlmacen)
		factura = Detalle.objects.get(factura__noFactura=noFactura, producto__codigo=codProd, almacen__id=iAlmacen)

		exist.cantidad -= decimal.Decimal(factura.cantidad)
		exist.save()
	except Existencia.DoesNotExist:
		return HttpResponse('No hay existencia para el producto ' + str(codProd))


# Retornar una factura con todo su detalle  -- url(r'^facturajson/$',
class FacturaById(LoginRequiredMixin, DetailView):

	queryset = Factura.objects.all()

	def get(self, request, *args, **kwargs):
		NoFact = self.request.GET.get('nofact')

		self.object_list = self.get_queryset().filter(noFactura=NoFact)

		format = self.request.GET.get('format')
		if format == 'json':
			return self.json_to_response()

		context = self.get_context_data()
		return self.render_to_response(context)

	def json_to_response(self):
		data = list()

		try:
			o = SolicitudOrdenDespachoH.objects.get(noSolicitud=self.object_list[0].ordenCompra)
		except SolicitudOrdenDespachoH.DoesNotExist:
			o = None

		for factura in self.object_list:
			data.append({
				'noFactura': factura.noFactura,
				'fecha': factura.fecha,
				'socioCodigo': factura.socio.codigo,
				'socioNombre': factura.socio.nombreCompleto,
				'orden': factura.ordenCompra if factura.ordenCompra != None else '',
				'terminos': factura.terminos,
				'vendedor': factura.userLog.username,
				'posteo': factura.posteo,
				'impresa': factura.impresa,
				'productos': [ 
					{	'codigo': prod.producto.codigo,
						'descripcion': prod.producto.descripcion,
						'unidad': prod.producto.unidad.descripcion,
						'cantidad': prod.cantidad,
						'precio': prod.precio,
						'descuento': prod.porcentajeDescuento,
						'almacen': prod.almacen.id,
					} 
					for prod in Detalle.objects.filter(factura=factura)],
				'ordenDetalle':
					{	'categoriaId': o.categoriaPrestamo.id if o != None else '',
						'categoriaDescrp': o.categoriaPrestamo.descripcion if o != None else '',
						'autorizador': o.autorizadoPor.username if o != None else '',
						'representante': o.representante.nombre if o != None else '',
						'tasaInteresAnual': o.tasaInteresAnual if o != None else '',
						'tasaInteresMensual': o.tasaInteresMensual if o != None else '',
						'cuotas': o.cantidadCuotas if o != None else '',
						'valorCuotas': o.valorCuotasCapital if o != None else '',
						'solicitud': o.noSolicitud if o != None else 0,
					}
				})
		return JsonResponse(data, safe=False)


# Vista para presentar la pantalla de facturacion y a la vez contiene el POST para guardar la factura.
class FacturacionView(LoginRequiredMixin, TemplateView):

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
					quitar_producto(self, item['codigo'], almacen, facturaNo)

				detalle = Detalle.objects.filter(factura = fact).delete()

			else:
				#Verificar la existencia de cada producto
				for item in dataD:
					exist = Existencia.objects.filter(producto__codigo=item['codigo'], almacen__id=almacen).values('cantidad','producto__descripcion')

					if decimal.Decimal(item['cantidad']) > exist[0]['cantidad']:
						raise Exception('No tiene existencia el producto: ' + exist[0]['producto__descripcion'] + ', solo tiene : '+ str(exist[0]['cantidad']))
				#Fin de verificacion de existencia
				
				try:
					fact = Factura()
					fact.noFactura = Factura.objects.latest('noFactura').noFactura + 1
				except Factura.DoesNotExist:
					fact.noFactura = 1

			fact.fecha = dataH['fecha']
			fact.terminos = dataH['terminos']
			fact.userLog = usuario

			if socio != None: fact.socio = socio

			fact.save()

			for item in dataD:
				detalle = Detalle()
				detalle.factura = fact
				detalle.producto = Producto.objects.get(codigo = item['codigo'])
				detalle.porcentajeDescuento = item['descuento']
				detalle.cantidad = item['cantidad']
				detalle.precio = float(item['precio'])
				detalle.almacen = Almacen.objects.get(id=almacen)
				detalle.save()

			return HttpResponse(fact.noFactura)

		except Exception as e:
			return HttpResponse(e)


# Listado de Facturas registradas
class ListadoFacturasViewSet(viewsets.ModelViewSet):

	queryset = Factura.objects.all()
	serializer_class = ListadoFacturasSerializer


# Documentos Relacionados a Cuentas
class DetalleFacturasView(APIView):

	serializer_class = DetalleFacturasSerializer

	def get(self, request, fechaInicio, fechaFin):
		
		# detalle = Detalle.objects.filter(factura__fecha__range=[fechaInicio, fechaFin])
		detalle = Detalle.objects.raw('SELECT * FROM facturacion_detalle group by producto_id')

		response = self.serializer_class(detalle, many=True)
		return Response(response.data)


# Retornar detalle de facturas (para Reporte Utilidades)
class RPTUtilidades(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.json_to_response()

	def json_to_response(self):
		data = list()

		registros = Detalle.objects.raw('SELECT \
											d.id, \
											f.fecha, \
											c.descripcion categoriaDescrp, \
											d.producto_id, \
											p.descripcion productoDescrp, \
											d.cantidad,  \
											d.precio,  \
											((d.cantidad * d.precio) - ((d.porcentajeDescuento/100) * d.precio * d.cantidad)) valor,  \
											d.costo, \
											d.precio - d.costo margen \
										FROM facturacion_detalle d \
										LEFT JOIN facturacion_factura f \
										LEFT JOIN administracion_producto p ON p.id = d.producto_id \
										LEFT JOIN administracion_categoriaProducto c ON c.id = p.categoria_id \
										GROUP BY d.producto_id, c.descripcion \
										ORDER BY c.descripcion, p.descripcion \
										')

		for detalle in registros:
			data.append({
				'id': detalle.id,
				'fecha': detalle.fecha,
				'productoId': detalle.producto_id,
				'productoDescrp': detalle.productoDescrp,
				'categoriaDescrp': detalle.categoriaDescrp,
				'cantidad': detalle.cantidad,
				'precio': detalle.precio,
				'valor': detalle.valor,
				'costo': detalle.costo,
				'margen': detalle.margen,
				})
		return JsonResponse(data, safe=False)


# Retornar resumen de ventas
class RPTResumenVentas(LoginRequiredMixin, DetailView):

	queryset = Detalle.objects.all()

	def get(self, request, *args, **kwargs):
		fechaI = request.GET.get('fechaI')
		fechaF = request.GET.get('fechaI')

		return self.json_to_response(fechaI, fechaF)

	def json_to_response(self, fechaInicio, fechaFin):
		data = list()

		registros = Detalle.objects.raw('SELECT \
											d.id, \
											s.nombreCompleto, \
											SUM((d.cantidad * d.precio) - ((d.porcentajeDescuento/100) * d.precio * d.cantidad)) valor  \
										FROM facturacion_detalle d \
										LEFT JOIN facturacion_factura f ON d.factura_id = f.id \
										LEFT JOIN administracion_socio s ON s.id = f.socio_id \
										GROUP BY s.nombreCompleto \
										ORDER BY s.nombreCompleto \
										')

		for detalle in registros:
			data.append({
				'id': detalle.id,
				'nombreCompleto': detalle.nombreCompleto,
				'valor': detalle.valor,
				})
		return JsonResponse(data, safe=False)


#Imprimir Factura
class ImprimirFacturaView(LoginRequiredMixin, TemplateView):

	template_name = 'print_factura.html'

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)
			factura = data['factura']

			fact = Factura.objects.get(noFactura=factura)
			fact.impresa = fact.impresa + 1
			fact.save()

			return HttpResponse(fact.impresa)

		except Exception as e:
			return HttpResponse(e)


#Reporte de Utilidades
class RPTUtilidadesView(LoginRequiredMixin, TemplateView):

	template_name = 'print_utilidades.html'


#Reporte de Ventas Resumido
class RPTVentasResumidoView(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_ventasResumido.html'


#Reporte de Ventas Diarias
class RPTVentasDiariasView(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_ventasDiarias.html'

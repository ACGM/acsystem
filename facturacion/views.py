from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, JsonResponse


from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ListadoFacturasSerializer

from .models import Factura, Detalle, OrdenDespachoSuperCoop
from administracion.models import Producto, Socio, CategoriaPrestamo
from inventario.models import Existencia, Almacen

import json
import math
import decimal

# Eliminar producto de la factura
def quitar_producto(self, idProd, iCantidad, iAlmacen):
	try:

		exist = Existencia.objects.get(producto = Producto.objects.get(codigo = idProd), almacen = Almacen.objects.get(id = iAlmacen))
		exist.cantidad -= decimal.Decimal(iCantidad)
		exist.save()
	except Existencia.DoesNotExist:
		return HttpResponse('No hay existencia para el producto ' + str(idProd))


# Retornar una factura con todo su detalle  -- url(r'^facturajson/$',
class FacturaById(DetailView):

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
			o = OrdenDespachoSuperCoop.objects.get(noSolicitud=self.object_list[0].ordenCompra)
		except OrdenDespachoSuperCoop.DoesNotExist:
			o = None

		for factura in self.object_list:
			data.append({
				'noFactura': factura.noFactura,
				'fecha': factura.fecha,
				'socioCodigo': factura.socio.codigo,
				'socioNombre': factura.socio.nombreCompleto,
				'orden': factura.ordenCompra if factura.ordenCompra != None else 0,
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
					{	'categoriaId': o.categoria.id if o != None else '',
						'categoriaDescrp': o.categoria.descripcion if o != None else '',
						'oficial': o.oficial.username if o != None else '',
						'pagarPor': o.pagarPor if o != None else '',
						'formaPago': o.formaPago if o != None else '',
						'tasaInteresAnual': o.tasaInteresAnual if o != None else '',
						'tasaInteresMensual': o.tasaInteresMensual if o != None else '',
						'quincena': o.quincena if o != None else '',
						'cuotas': o.cuotas if o != None else '',
						'valorCuotas': o.valorCuotas if o != None else '',
						'solicitud': o.noSolicitud if o != None else 0,
					}
				})
		return JsonResponse(data, safe=False)


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


# Vista para guardar la orden de despacho SUPERCOOP  --- url(r'^ordenSuperCoop/$'
class OrdenDespachoSPView(View):

	def post(self, request, *args, **kwargs):

		try:
			data = json.loads(request.body)

			OrdenD = data['orden']

			solicitud = int(OrdenD['solicitud'])
			categoriaP = OrdenD['categoriaPrestamo']
			oficial = OrdenD['oficial']
			pagarPor = OrdenD['pagarPor']
			formaPago = OrdenD['formaPago']
			tasaInteresAnual = OrdenD['tasaInteresAnual']
			tasaInteresMensual = OrdenD['tasaInteresMensual']
			quincena = int(OrdenD['quincena'])
			cantidadCuotas = OrdenD['cantidadCuotas']
			valorCuotas = float(OrdenD['valorCuotas'])

			factura = OrdenD['factura']

			if categoriaP != None:
				CP = CategoriaPrestamo.objects.get(id=categoriaP)
			if oficial != None:
				oficial = User.objects.get(username = oficial)

			if solicitud > 0:
				ordenDespacho = OrdenDespachoSuperCoop.objects.get(noSolicitud = solicitud)
			else:
				ordenDespacho = OrdenDespachoSuperCoop()

			ordenDespacho.categoria = CP
			ordenDespacho.oficial = oficial
			ordenDespacho.pagarPor = pagarPor
			ordenDespacho.formaPago = formaPago
			ordenDespacho.tasaInteresAnual = tasaInteresAnual
			ordenDespacho.tasaInteresMensual = tasaInteresMensual
			ordenDespacho.quincena = quincena
			ordenDespacho.cuotas = cantidadCuotas
			ordenDespacho.valorCuotas = valorCuotas

			ordenDespacho.save()

			if not solicitud > 0:
				fact = Factura.objects.get(noFactura=factura)
				fact.ordenCompra = ordenDespacho.noSolicitud
				fact.save()

			return HttpResponse(ordenDespacho.noSolicitud)

		except Exception as e:
			return HttpResponse(e)


# Listado de Facturas registradas
class ListadoFacturasViewSet(viewsets.ModelViewSet):

	queryset = Factura.objects.all()
	serializer_class = ListadoFacturasSerializer


#Imprimir Factura
class ImprimirFacturaView(TemplateView):

	template_name = 'print_factura.html'

from django.shortcuts import render

from rest_framework import viewsets, serializers

from .models import OrdenCompra, DetalleOrden, DetalleCuentasOrden

#Serializador para el ViewSet de Ordenes de compra
class OrdenSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=OrdenCompra
		fields=('orden','suplidor','socio','fecha','monto','cuotas','montocuotas','detalleOrden','detalleCuentas')

#ViewSet de ordenes de compra, listo para API
class OrdenViewSet(viewsets.ModelViewSet):
	queryset=OrdenCompra.objects.all()
	serializer_class=OrdenSerializer

#Serializador para el ViewSet de Detalles Ordenes
class DetalleOrdenSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=DetalleOrden
		fields=('articulo','monto')

#ViewSet de Detalles Ordenes
class DetalleOrderViewSet(viewsets.ModelViewSet):
	queryset=DetalleOrden.objects.all()
	serializer_class=DetalleOrdenSerializer

#Serializador para el detalle de las cuentas de las ordenes
class DetalleCuentaSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model=DetalleCuentasOrden
		fields=("cuenta","auxiliar","debito","credito")

#ViewSet para el detalle de las cuentas de las Ordenes de compra
class DetalleCuentaViewSet(viewsets.ModelViewSet):
	queryset=DetalleCuentasOrden.objects.all()
	serializer_class=DetalleCuentaSerializer

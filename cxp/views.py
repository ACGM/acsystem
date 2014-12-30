from django.shortcuts import render

from rest_framework import viewsets

from .models import OrdenCompra, DetalleOrden, CxpSuperCoop
from .serializers import OrdenSerializer, DetalleOrdenSerializer, CxpSuperCoopSerializer



#ViewSet de ordenes de compra, listo para API
class OrdenViewSet(viewsets.ModelViewSet):
	queryset=OrdenCompra.objects.all()
	serializer_class=OrdenSerializer


#ViewSet de Detalles Ordenes
class DetalleOrderViewSet(viewsets.ModelViewSet):
	queryset=DetalleOrden.objects.all()
	serializer_class=DetalleOrdenSerializer

#ViewSet de Cxp de SuperCoop
class CxpSuperViewSet(viewsets.ModelViewSet):
	queryset=CxpSuperCoop.objects.all()
	serializer_class=CxpSuperCoopSerializer



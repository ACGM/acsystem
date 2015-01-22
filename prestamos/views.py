from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SolicitudesPrestamosSerializer

from .models import SolicitudPrestamo


#Vista para Maestra de Prestamos
class MaestraPrestamosView(TemplateView):

	template_name = 'maestraprestamos.html'


#Vista para Desembolso Electronico de Prestamos
class DesembolsoPrestamosView(TemplateView):

	template_name = 'desembolsoelectronico.html'


#Vista para Solicitud de Prestamo
class SolicitudPrestamoView(TemplateView):

	template_name = 'solicitudprestamo.html'


#Vista para Solicitud de Ordenes de Despacho
class SolicitudOrdenDespachoView(TemplateView):

	template_name = 'solicitudordendespacho.html'


#Vista para Notas de Debito
class NotaDeDebitoView(TemplateView):

	template_name = 'notasdebito.html'


#Vista para Notas de Credito
class NotaDeCreditoView(TemplateView):

	template_name = 'notascredito.html'


#Vista para Notas de Credito Especiales
class NotaDeCreditoEspView(TemplateView):

	template_name = 'notacreditoespecial.html'


# Listado de Solicitudes de Prestamos
class SolicitudesPrestamosAPIView(APIView):

	serializer_class = SolicitudesPrestamosSerializer

	def get(self, request, solicitud=None):
		if solicitud != None:
			solicitudes = SolicitudPrestamo.objects.filter(noSolicitud=solicitud)
		else:
			solicitudes = SolicitudPrestamo.objects.all()

		response = self.serializer_class(solicitudes, many=True)
		return Response(response.data)


# Listado de Solicitudes de Prestamos Por Codigo de Socio
class SolicitudesPrestamosAPIViewByCodigoNombre(APIView):

	serializer_class = SolicitudesPrestamosSerializer

	def get(self, request, codigo=None, nombre=None):
		if codigo != None:
			solicitudes = SolicitudPrestamo.objects.filter(socio__codigo=codigo)
		else:
			solicitudes = SolicitudPrestamo.objects.filter(socio__nombreCompleto__contains=nombre)

		response = self.serializer_class(solicitudes, many=True)
		return Response(response.data)
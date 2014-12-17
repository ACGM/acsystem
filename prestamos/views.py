from django.shortcuts import render

from django.views.generic import TemplateView


#Vista para Notas de Debito
class NotaDeDebitoView(TemplateView):

	template_name = 'notasdebito.html'


#Vista para Notas de Credito
class NotaDeCreditoView(TemplateView):

	template_name = 'notascredito.html'


#Vista para Maestra de Prestamos
class MaestraPrestamosView(TemplateView):

	template_name = 'maestraprestamos.html'


#Vista para Desembolso Electronico de Prestamos
class DesembolsoPrestamosView(TemplateView):

	template_name = 'desembolsoelectronico.html'


#Vista para Solicitud de Prestamo
class SolicitudPrestamoView(TemplateView):

	template_name = 'solicitudprestamo.html'
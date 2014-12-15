from django.shortcuts import render

from django.views.generic import TemplateView


#Vista para Notas de Debito
class NotaDeDebitoView(TemplateView):

	template_name = 'notasdebito.html'


#Vista para Maestra de Prestamos
class MaestraPrestamosView(TemplateView):

	template_name = 'maestraprestamos.html'

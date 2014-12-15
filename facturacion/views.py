from django.shortcuts import render

from django.views.generic import TemplateView


class FacturacionView(TemplateView):

	template_name = 'facturacion.html'
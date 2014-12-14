from django.shortcuts import render

from django.views.generic import TemplateView


class InventarioView(TemplateView):

	template_name = 'inventario.html'
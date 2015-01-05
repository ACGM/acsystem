from django.shortcuts import render

from django.views.generic import TemplateView


class FacturacionView(TemplateView):

	template_name = 'facturacion.html'


# Listado de Facturas registradas
class ListadoEntradasInvView(viewsets.ModelViewSet):

	queryset = InventarioH.objects.all()
	serializer_class = EntradasInventarioSerializer

from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework import viewsets, serializers
from rest_framework.response import Response

from .serializers import DesembolsosCajasSerializer
from .models import DesembolsoH


# Vista de desembolsos
class DesembolsoView(TemplateView):
	
	template_name = 'desembolsos.html'


# Listado de Desembolsos de Caja
class ListadoDesembolsosViewSet(viewsets.ModelViewSet):

	queryset = DesembolsoH.objects.all()
	serializer_class = DesembolsosCajasSerializer
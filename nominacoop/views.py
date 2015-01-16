from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework import viewsets, serializers

from .serializers import NominasGeneradasSerializer

from .models import NominaCoopH, NominaCoopD


# Vista Principal de Nomina
class NominaView(TemplateView):

	template_name = 'nomina.html'


# Listado de Nominas Generadas
class ListadoNominasGeneradasViewSet(viewsets.ModelViewSet):

	queryset = NominaCoopH.objects.all()
	serializer_class = NominasGeneradasSerializer
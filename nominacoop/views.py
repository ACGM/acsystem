from django.shortcuts import render

from django.views.generic import TemplateView


class NominaView(TemplateView):

	template_name = 'nomina.html'
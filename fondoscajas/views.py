from django.shortcuts import render

from django.views.generic import TemplateView


class DesembolsoView(TemplateView):
	
	template_name = 'desembolsos.html'

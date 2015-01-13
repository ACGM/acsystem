from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets, serializers
from rest_framework.response import Response

from .serializers import DesembolsosCajasSerializer
from .models import DesembolsoH, DesembolsoD


# Vista de desembolsos
class DesembolsoView(TemplateView):
	
	template_name = 'desembolsos.html'


# Retornar un desembolso con todo su detale -- url(r'^desembolsojson/$',
class DesembolsoByCheque(DetailView):

	queryset = DesembolsoH.objects.all()

	def get(self, request, *args, **kwargs):
		NoCheque = self.request.GET.get('nocheque')

		self.object_list = self.get_queryset().filter(cheque=NoCheque)

		format = self.request.GET.get('format')
		if format == 'json':
			return self.json_to_response()

		context = self.get_context_data()
		return self.render_to_response(context)

	def json_to_response(self):
		data = list()

		try:
			detalle = DesembolsoD.objects.filter(desembolso=self.object_list[0])
		except DesembolsoD.DoesNotExist:
			detalle = None

		for desembolso in self.object_list:
			data.append({
				'beneficiario': desembolso.beneficiario,
				'fecha': desembolso.fecha,
				'fondo': desembolso.fondo.descripcion,
				'distrito': desembolso.distrito,
				'estatus': desembolso.estatus,
				'impreso': desembolso.impreso,
				'cheque': desembolso.cheque,
				'id': desembolso.id,
				'detalle': [{
					'id': item.id if detalle != None else '',
					'conceptoId': item.concepto.id if detalle != None else '',
					'conceptoDescrp': item.concepto.descripcion if detalle != None else '',
					'monto': item.monto if detalle != None else ''

				} for item in DesembolsoD.objects.filter(desembolso=desembolso)],

				})
		return JsonResponse(data, safe=False)


# Listado de Desembolsos de Caja
class ListadoDesembolsosViewSet(viewsets.ModelViewSet):

	queryset = DesembolsoH.objects.all()
	serializer_class = DesembolsosCajasSerializer
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets, serializers
from rest_framework.response import Response

from .serializers import DesembolsosCajasSerializer
from .models import DesembolsoH, DesembolsoD

from acgm.views import LoginRequiredMixin


# Vista de desembolsos
class DesembolsoView(TemplateView):
	
	template_name = 'desembolsos.html'


# Retornar un desembolso con todo su detale -- url(r'^desembolsojson/$',
class DesembolsoByCheque(DetailView):

	queryset = DesembolsoH.objects.all()

	def get(self, request, *args, **kwargs):
		NoCheque = self.request.GET.get('nocheque')
		byId = self.request.GET.get('id')

		if byId != None:
			self.object_list = self.get_queryset().filter(id=byId)
		else:
			self.object_list = self.get_queryset().filter(cheque=NoCheque)
		
		return self.json_to_response()

	def json_to_response(self):
		data = list()

		try:
			detalle = DesembolsoD.objects.filter(desembolso=self.object_list[0])
		except DesembolsoD.DoesNotExist:
			detalle = None

		for desembolso in self.object_list:
			data.append({
				'fecha': desembolso.fecha,
				'fondo': desembolso.fondo.descripcion,
				'localidad': desembolso.localidad.descripcion,
				'detalleHeader': desembolso.detalle,
				'conceptoHeader': desembolso.concepto,
				'estatus': desembolso.estatus,
				'impreso': desembolso.impreso,
				'cheque': desembolso.cheque,
				'id': desembolso.id,
				'totalGeneral': float(desembolso.totalGeneral.replace(',','')),
				'userLog': desembolso.userLog.username if desembolso.userLog != None else '',
				'detalle': [{
					'id': item.id if detalle != None else '',
					'beneficiario': item.beneficiario if detalle != None else '',
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


# Imprimir Desembolso
class ImprimirDesembolsoView(LoginRequiredMixin, TemplateView):

	template_name = 'print_desembolso.html'

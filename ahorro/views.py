from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, ListView, DetailView

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import InteresesAhorro, MaestraAhorro, AhorroSocio, RetiroAhorro
from administracion.models import Socio
from cuenta.models import DiarioGeneral, Cuentas
from .serializers import interesAhorroSerializer, maestraAhorroSerializer, AhorroSocioSerializer, RetiroAhorroSerializer

class MaestraAhorroView(ListView):
	queryset=MaestraAhorro.objects.all()

	def get(self, request, *args, **kwargs):
		id_socio = self.request.GET.get('socio')

		self.object_list= self.get_queryset().filter(socio=id_socio)
		format = self.request.GET.get('format')
		if format=="json":
			return self.json_to_response

		context = self.get_context_data()
		return self.render_to_response(context)

	def json_to_response(self):
		data=list()

		for ahorro in self.object_list:
			data.append({
				'id':ahorro.id,
				'socio':ahorro.socio.nombres +' '+ ahorro.socio.apellidos,
				'balance':ahorro.balance,
				'disponible':ahorro.disponible,
				'maestra':[
					{
						'id':maestra.id,
						'fecha':maestra.fecha,
						'monto':maestra.monto,
						'interes':maestra.interes.porcentaje,
						'balance':maestra.balance,
						'estatus':maestra.estatus,
						'cuentas':[
							{
								'id':cuentas.id,
								'fecha':cuentas.fecha,
								'cuenta':cuentas.cuenta,
								'referencia':cuentas.referencia,
								'auxiliar':cuentas.auxiliar,
								'tipoDoc':cuentas.tipoDoc.tipoDoc,
								'estatus':cuentas.estatus,
								'debito':cuentas.debito,
								'credito':cuentas.credito

							}
							for cuentas in DiarioGeneral.objects.filter(referencia='AH-'+str(maestra.pk))]
								
					}
						for maestra in MaestraAhorro.objects.filter(ahorro=ahorro.id)]
				})
			return JsonResponse(data,safe=False)

			

		

class InteresAhorroViewSet(viewsets.ModelViewSet):
	queryset=InteresesAhorro.objects.all()
	serializer_class=interesAhorroSerializer
		

class MaestraAhorroViewSet(viewsets.ModelViewSet):
	queryset=MaestraAhorro.objects.all()
	serializer_class=maestraAhorroSerializer

class AhorroViewSet(viewsets.ModelViewSet):
	queryset=AhorroSocio.objects.all()
	serializer_class=AhorroSocioSerializer

class RetirosAhorroViewSet(viewsets.ModelViewSet):
	queryset=RetiroAhorro.objects.all()
	serializer_class=RetiroAhorroSerializer

class AhorroView(TemplateView):
	template_name = 'ahorro.html'




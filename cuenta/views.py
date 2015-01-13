from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime

from rest_framework import viewsets
from django.views.generic import TemplateView, ListView, DetailView, View

from .models import Cuentas,Auxiliares,DiarioGeneral, TipoDocumento , CuentasControl
from .serializers import CuentasSerializer, AuxiliarSerualizer, DiarioSerializer, TipoDocSerializer, CuentasControlSerializer


class DiarioGeneralView(DetailView):
	queryset = DiarioGeneral.objects.all()
	solTipo = ''
	def post(self, request, *args, **kwargs):
		InfoType= self.request.Get.get('infoType')

		try:
			if infoType=='cuentas':
				data=json.loads(request.body)

				cta=data['codigo']
				ctId=data['id']

				if ctId != null:
					regCuenta = Cuentas.objects.filter(id=ctId)
					regCuenta.descripcion=data['descripcion']
					regCuenta.save()
				
				if cta != null:
					regCuenta = Cuentas.objects.filter(codigo=cta)
					if regCuenta == null:
						regCuenta = Cuentas()
						regCuenta.codigo= data['codigo']
						regCuenta.descripcion = data['descripcion']
						regCuenta.origen = data['origen']
						regCuenta.control = data['control']
						regCuenta.cuentasControl = data['cuentaControl']
						regCuenta.save()

			if infoType =='Diario':
				data=json.loads(request.body)

				for item in data:
					drid=data['id']
					
					if drid != null:
						regDiario=DiarioGeneral.objects.get(id=drid)
						regDiario.referencia = data['referencia']
						regDiario.auxiliar = data['auxiliar']
						regDiario.tipoDoc = data['tipoDoc']
						regDiario.estatus = data['estatus']
						regDiario.debito = data['debito']
						regDiario.credito = data['credito']
						regDiario.save()
					
					else:
						regDiario = DiarioGeneral()
						regDiario.fecha = data['fecha']
						regDiario.cuenta = data['cuenta']
						regDiario.referencia = data['referencia']
						regDiario.Auxiliares = data['auxiliar']
						regDiario.tipoDoc = data['tipoDoc']
						regDiario.estatus = data['estatus']
						regDiario.debito = data['debito']
						regDiario.credito = data['credito']
						regDiario.save()

			return HttpResponse('1')
		except Exception as ex:
			return HttpResponse(ex)

	def get(self, request, *args, **kwargs):
		id_diario= self.request.GET.get('id_diario')
		self.solTipo = self.request.GET.get('solicitud')

		self.object_list = self.get_queryset()
		format = self.request.GET.get('format')
		if format == 'json':
			return self.json_to_response()

		context =self.get_context_data()
		return self.render_to_response(context)

	def json_to_response(self):
		data=list()

		if self.solTipo == 'diario':
			for diario in self.object_list:
				data.append({
					'id' : diario.id,
					'fecha' : diario.fecha,
					'cuenta' : diario.cuenta.codigo,
					'referencia' : diario.referencia,
					'auxiliar' : diario.auxiliar,
					'tipoDoc' : diario.tipoDoc.tipoDoc,
					'estatus' : diario.estatus,
					'debito' : diario.debito,
					'credito' : diario.credito
					})
		else:
			if self.solTipo == 'cuenta':
				cuentaList = Cuentas.objects.all()
				for cuenta in cuentaList:
					data.append({
						'id' : cuenta.id,
						'codigo' : cuenta.codigo,
						'descripcion' : cuenta.descripcion,
						'origen' : cuenta.origen,
						'control' : cuenta.control
						#'cuentaControl' : cuenta.cuentaControl.pk
						})
			else: 
				if self.solTipo == 'aux':
					auxList = Auxiliares.objects.all()

					for aux in auxList:
						data.append({
							'id' : aux.id,
							'codigo' : aux.codigo,
							'descripcion' : aux.descripcion,
							'cuenta' : aux.cuenta.codigo
							})
				else:
					tipoList = TipoDocumento.objects.all()
					for tipo in tipoList:
						data.append({
							'id' : tipo.id,
							'tipoDoc' : tipo.tipoDoc,
							'descripcion' : tipo.descripcion
							})



		return JsonResponse(data, safe=False)



class CuentasViewSet(viewsets.ModelViewSet):
	queryset=Cuentas.objects.all()
	serializer_class=CuentasSerializer


class AuxiliarViewSet(viewsets.ModelViewSet):
	queryset=Auxiliares.objects.all()
	serializer_class=AuxiliarSerualizer

class DiarioViewSet(viewsets.ModelViewSet):
	queryset=DiarioGeneral.objects.all()
	serializer_class=DiarioSerializer

class TipoDocViewSet(viewsets.ModelViewSet):
	queryset=TipoDocumento.objects.all()
	serializer_class=TipoDocSerializer

class CuentaControlViewSet(viewsets.ModelViewSet):
	queryset=CuentasControl
	serializer_class=CuentasControlSerializer
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime

from django.views.generic import TemplateView, ListView, DetailView, View

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import InteresesAhorro, MaestraAhorro, AhorroSocio, RetiroAhorro
from administracion.models import Socio
from cuenta.models import DiarioGeneral, Cuentas
from .serializers import interesAhorroSerializer, maestraAhorroSerializer, AhorroSocioSerializer, RetiroAhorroSerializer

class MaestraAhorroView(DetailView):
	
	queryset=AhorroSocio.objects.all()

	#Metodo Post para el proceso completo
	def post(self,request,*args, **kwargs):
		Ref= self.request.Get.get('Ref') #Referencia de tipo de operacion
		Ret= self.request.Get.get('Ret') #Referecia especifica para retiro

		try:
			dataAh=json.loads(request.body)
			data=dataAh['maestra']
			ahorroId=dataAh['id']
			dataCuentas=data['cuentas']

			maestraId=dataMaestra['id']

			# Operacion para registar un retiro de ahorro
			if Ret == 'Rt':
				listaDiario=[]
				ahorro = AhorroSocio.objects.get(id =ahorroId)
				maestraRg = MaestraAhorro()
				rsDiario = DiarioGeneral()

				# Recalcula el balance y el disponible del socio
				balanceAc = ahorro.balance
				disponibleAc = ahorro.disponible

				balanceAc = balanceAc - dataAh['monto']
				disponible = disponible - dataAh['monto']

				# Actualiza los cambios en el registro de ahorros
				ahorro.balance=balanceAc
				ahorro.disponible=disponible
				ahorro.save()

				# Registra el retiro
				retiro=RetiroAhorro()
				retiro.socio=dataRet
				retiro.ahorro=dataAh['id']
				retiro.tipoRetiro=dataAh['tipoRetiro']
				retiro.monto=dataAh['monto']
				retiro.save()

				# Registra las cuentas afectadas en el Diario General
				for item in dataCuentas:
					rsDiario.fecha = datetime.now()
					rsDiario.cuenta = item['cuenta']
					rsDiario.referencia = item['referencia']
					rsDiario.auxiliar = item['auxiliar']
					rsDiario.tipoDoc = item['tipoDoc']
					rsDiario.estatus = item['estatus']
					rsDiario.debito = item['debito']
					rsDiario.credito = item['credito']
					rsDiario.save()
					listaDiario.append(rsDiario.id)

				# Registra en el historico de ahorros
				maestra.fecha=datetime.now
				maestra.retiro=retiro.id
				maestra.monto=data['monto']
				maestra.interes=data['interes']
				maestra.balance=balanceAc
				maestra.estatus=False
				
				for c in listaDiario:
					maestra.cuentas.append(c)
				
				maestra.save()

				# Actualiza las referencia de la Maestra
				for item in listaDiario:
					rsDiario=DiarioGeneral.objects.get(id=item)
					rsDiario.referencia = 'AR-'+str(maestra.id)
					rsDiario.save()

			else:
				# Corre el escenario de edicion o creacion de registro de ingreso de ahorro en la Maestra
				if maestraId > 0:
					regMaestra=MaestraAhorro.objects.get(id=maestraId)
					
					ahorroE=AhorroSocio.objects.get(id=dataAr['id'])

					# Recalcula el Balance y el Disponible 
					balanceAnt = regMaestra.monto 
					balanceArE = ahorroE.balance
					
					dispoArE = ahorroE.disponible
					montoArE = data['monto']
					
					# Recalcula el Balance y el Disponible en caso de ser un prestamo o un ahorro
					if Ref == 'RTE' or Ref =='PR':
						balanceArE = balanceArE + balanceAnt
						balanceArE = balanceArE - dmontoArE
					else:
						balanceArE = balanceArE - balanceAnt
						dispoArE = dispoArE - balanceAnt 
						balanceArE = balanceArE + montoArE
						dispoArE = dispoArE + montoArE

					# Edital el registro en de las cuentas o auxiliares en el Diario General
					for cuentaAhE in regMaestra.cuentas:
						rsDiario = DiarioGeneral.objects.get(id=cuentaAhE)
						
						for itemCuenta in dataCuentas:
							if itemCuenta['cuenta'] == rsDiario.cuenta or itemCuenta['auxiliar'] == rsDiario.auxiliar:
								rsDiario.debito = itemCuenta['debito']
								rsDiario.credito = itemCuenta['credito']
								rsDiario.save()

					# Guarda los cambios de la Maestra Ahorro
					regMaestra = MaestraAhorro()
					regMaestra.monto = data['monto']
					regMaestra.interes = data['interes']
					regMaestra.save()

					# En caso de ser una edicion de un retiro Actualiza el monto de retiro.
					if Ref == 'RTE':
						retiro = RetiroAhorro.objects.get(ahorro=data['id'])
						retiro.monto = dataAh['monto']
						retiro.save()

					# Actualiza el registro de ahorro
					regAhorro.balance = balanceArE
					regAhorro.disponible = dispoArE
					regAhorro.save()

				else:
					# Guarda un registro nuevo en la Maestra
					regMaestra = MaestraAhorro()
					rsDiario = DiarioGeneral()
					ahorroE=AhorroSocio.objects.get(id=dataAr['id'])
					listaDiario=[]

					# Registra las cuentas y/o auxiliares en el Diario General
					for item in dataCuentas:
						rsDiario.fecha = datetime.now()
						rsDiario.cuenta = item['cuenta']
						rsDiario.referencia = item['referencia']
						rsDiario.auxiliar = item['auxiliar']
						rsDiario.tipoDoc = item['tipoDoc']
						rsDiario.estatus = item['estatus']
						rsDiario.debito = item['debito']
						rsDiario.credito = item['credito']
						rsDiario.save()
						listaDiario.append(rsDiario.id)

					regMaestra.fecha = datetime.now()
					regMaestra.monto = data['monto']
					regMaestra.interes = data['interes']
					regMaestra.balance = data['balance']
					regMaestra.estatus = data['estatus']

					# Relaciona los registros del Diario General a la Maestra
					for c in listaDiario:
						regMaestra.cuentas.append(c)
					
					regMaestra.save()

					# Actualiza las referencia de la Maestra
					for item in listaDiario:
						rsDiario=DiarioGeneral.objects.get(id=item)
						rsDiario.referencia = 'AR-'+str(regMaestra.id)
						rsDiario.save()

					ahorroE.maestra.append(regMaestra.id)
					ahorroE.save()
			return HttpResponse('1')

		except Exception as ex:
			return HttpResponse(ex)

	def get(self, request, *args, **kwargs):
		# id_ahorro = self.request.GET.get('ahorro')
		#Reg= self.request.Get.get('Reg')
		Socio = self.request.GET.get(socio)

		self.object_list= self.get_queryset()#.filter(id=id_ahorro)
		format = self.request.GET.get('format')
		if format=="json":
			return self.json_to_response(Ret,Socio)

		context = self.get_context_data()
		return self.render_to_response(context)

	def json_to_response(self, Reg, Socio):
		data=list()
		if 'AR' =='AR':
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
									'cuenta':cuentas.cuenta.codigo,
									'referencia':cuentas.referencia,
									'auxiliar':cuentas.auxiliar,
									'tipoDoc':cuentas.tipoDoc.tipoDoc,
									'estatus':cuentas.estatus,
									'debito':cuentas.debito,
									'credito':cuentas.credito,

								}
								for cuentas in DiarioGeneral.objects.filter(referencia=('AH-'+str(maestra.id)))]
									
						}
							for maestra in MaestraAhorro.objects.filter(ahorro=ahorro.id)]
					})
		else:
			for retiro in self.object_list:
				data.append({
					'id' : retiro.id,
					'socio' : retiro.socio.nombres+' '+retiro.socio.apellidos,
					'ahorro' : retiro.socio.id,
					'tipoRetiro' : retiro.tipoRetiro,
					'monto' : retiro.monto
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




import json
import decimal

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView

from administracion.models import Socio
from prestamos.models import MaestraPrestamo
from ahorro.models import AhorroSocio

from rest_framework import viewsets

from .models import DetalleRecibo, RecibosIngreso



class reciboView(viewsets.ModelViewSet):
    queryset = RecibosIngreso.objects.all()

    def post(self, request):
        data = json.loads(request.body)
        dataDp= data['detalle']

        if data[id] is None:
            regRecibo = RecibosIngreso()
            regDetalle = DetalleRecibo()
            regSocio = Socio.objects.get(codigo=data['socio'])
            regPrest = MaestraPrestamo.objects.get(id=data['prestamo'])
            regAHorro = AhorroSocio.objects.get(id=data['ahorro'])

            regRecibo.socioIngreso = regSocio
            regRecibo.prestamo = regPrest
            regRecibo.ahorro = regAHorro
            regRecibo.montoPrestamo = data['montoPrestamo']
            regRecibo.montoAhorro = data['montoAhorro']
            regRecibo.fecha  = data['fecha']
            regRecibo.estatus = data['estatus']
            regRecibo.save()

            regDetalle.cantCuotas = dataDp['CantCuotas']
            regDetalle.montoCuota = dataDp['montoCuotas']
            regDetalle.montoDistribuir = dataDp['distribuir']
            regDetalle.save()
            
            regRecibo.detallePrestamo(regDetalle)
        else:
            if data['estatus'] == 'A':
                regRecibo = RecibosIngreso.objects.get(id=data['id'])
                regRecibo.montoPrestamo = data['montoPrestamo']
                regRecibo.montoAhorro = data['montoAhorro']
                regRecibo.save()

                regDetalle = DetalleRecibo.objects.get(id=dataDp['id'])
                regDetalle.cantCuotas = dataDp['CantCuotas']
                regDetalle.montoCuotas = dataDp['montoCuotas']
                regDetalle.montoDistribuir = dataDp['distribuir']
                regDetalle.save()

            elif data['estatus'] == 'P':
                regRecibo = RecibosIngreso.objects.get(id=data['id'])
                regRecibo.estatus = data['estatus']
                regRecibo.save()


    def get(self, request, *args, **kwargs):

        self.objects_list = self.get_queryset()
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        for recibos in self.objects_list:
            data.append({
                'id': recibos.id,
                'socioCod': recibos.socioIngreso.codigo,
                'socio': recibos.socioIngreso.nombre + ' ' + recibos.socioIngreso.apellido,
                'prestamo': {
                    'id' : recibos.prestamo.id,
                    'montoInicial': recibos.prestamo.montoInicial,
                    'balance': recibos.prestamo.balance
                },
                'ahorro': {
                    'id': recibos.ahorro.id,
                    'balance': recibos.ahorro.balance,
                    'disponible': recibos.ahorro.disponible
                },
                'montoPrestamo': recibos.montoPrestamo,
                'montoAhorro': recibos.montoAhorro,
                'fecha': recibos.fecha,
                'estatus': recibos.estatus,
                'detallePrestamo':{
                    'id': recibos.detallePrestamo.id,
                    'montoCuota': recibos.detallePrestamo.montoCuota,
                    'montoDistribuir': recibos.detallePrestamo.montoDistribuir,
                    'CantCuotas': recibos.detallePrestamo.cantCuotas
                }
            })


class reciboTemplateView(TemplateView):
    template_name = "reciboIng.html"


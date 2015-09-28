import json
import decimal

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView

from administracion.models import Socio
from prestamos.models import MaestraPrestamo
from prestamos.views import guardarPagoCuotaPrestamo
from ahorro.models import AhorroSocio, MaestraAhorro

from rest_framework import viewsets

from .models import DetalleRecibo, RecibosIngreso

class reciboPost(TemplateView):
    template_name="recigoImp.html"

    def post(self, request):
        registro = self.request.GET.get('recibo')
        fecha = self.request.GET.get('fecha')

        recibo = RecibosIngreso.objects.get(id=registro)

        regAhorro = AhorroSocio.objects.get(id=recibo.ahorro.id)

        regMaestra = MaestraAhorro()
        regMaestra.ahorro = regAhorro
        regMaestra.fecha = fecha
        regMaestra.monto = recibo.montoAhorro
        regMaestra.estatus = 'P'
        regMaestra.save()
        
        guardarPagoCuotaPrestamo(recibo.prestamo.noPrestamo,recibo.montoPrestamo,0,0,'RI')



class reciboTemplateView(TemplateView):
    template_name = "reciboIng.html"

    def post(self, request):
        data = json.loads(request.body)
        dataDp= data['detalle']

        if data[id] is None:
            regRecibo = RecibosIngreso()
            regSocio = Socio.objects.get(codigo=data['socio'])

            if data['prestamo'] != None:
                MaestraPrestamo.objects.get(noPrestamo=data['prestamo'])
            
            if data['ahorro'] == 1:
                regAHorro = AhorroSocio.objects.get(socio=regSocio)

            regRecibo.socioIngreso = regSocio
            regRecibo.prestamo = regPrest
            regRecibo.ahorro = regAHorro
            regRecibo.montoPrestamo = data['montoPrestamo']
            regRecibo.montoAhorro = data['montoAhorro']
            regRecibo.fecha  = data['fecha']
            regRecibo.estatus = data['estatus']
            regRecibo.save()

        else:
            if data['estatus'] == 'A':
                regRecibo = RecibosIngreso.objects.get(id=data['id'])
                regRecibo.montoPrestamo = data['montoPrestamo']
                regRecibo.montoAhorro = data['montoAhorro']
                regRecibo.estatus = data['estatus']
                regRecibo.save()

    def get(self, request, *args, **kwargs):

        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        for recibos in RecibosIngreso.objects.all():
            data.append({
                'id': recibos.id,
                'socioCod': recibos.socioIngreso.codigo,
                'socio': recibos.socioIngreso.nombre + ' ' + recibos.socioIngreso.apellido,
                'prestamo': {
                    'noPrestamo' : recibos.prestamo.noPrestamo if recibos.prestamo != None else '',
                    'montoInicial': recibos.prestamo.montoInicial if recibos.prestamo != None else '',
                    'balance': recibos.prestamo.balance if recibos.prestamo != None else ''
                },
                'montoPrestamo': recibos.montoPrestamo,
                'montoAhorro': recibos.montoAhorro,
                'fecha': recibos.fecha,
                'estatus': recibos.estatus,
            })
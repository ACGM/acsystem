import json
import decimal

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView

from administracion.models import Socio
from prestamos.models import MaestraPrestamo
from prestamos.views import guardarPagoCuotaPrestamo
from ahorro.models import AhorroSocio, MaestraAhorro
from cuenta.models import DiarioGeneral, Cuentas
from administracion.models import Socio, DocumentoCuentas, TipoDocumento

from rest_framework import viewsets

from .models import DetalleRecibo, RecibosIngreso

class reciboPost(TemplateView):
    template_name="recigoImp.html"

    def setCuentaMaestra(self, idMaestra, doc, Fecha):
        regMaestra = MaestraAhorro.objects.get(id= idMaestra)

        cuenta = Cuentas.objects.get(codigo=doc.cuenta.codigo)

        diario = DiarioGeneral()
        diario.fecha = fecha
        diario.referencia = 'AH-' + str(idMaestra)
        diario.cuenta = cuenta
        diario.estatus = 'P'

        if doc.accion == 'D':
            diario.debito = monto
            diario.credito = 0
        else:
            diario.debito = 0
            diario.credito = monto

        diario.save()


        regMaestra.cuentas.add(diario)
        return diario.id

    def post(self, request):
        data = json.loads(request.body)
        registro = data['recibo']
        fecha = data['fecha']

        recibo = RecibosIngreso.objects.get(id=registro)

        regAhorro = AhorroSocio.objects.get(id=recibo.ahorro.id)

        regMaestra = MaestraAhorro()
        regMaestra.ahorro = regAhorro
        regMaestra.fecha = fecha
        regMaestra.monto = recibo.montoAhorro
        regMaestra.estatus = 'P'
        regMaestra.save()

        tipo = TipoDocumento.objects.get(codigo='AH')
        doc = DocumentoCuentas.objects.filter(documento = tipo)

        for docu in doc:
            self.setCuenta(regMaestra.id, doc, Fecha)
        
        guardarPagoCuotaPrestamo(recibo.prestamo.noPrestamo,recibo.montoPrestamo,0,'RIRG-'+str(recibo.id),'RIRG')

        return HttpResponse('Ok')

class reciboTemplateView(TemplateView):
    template_name = "reciboIng.html"

    def post(self, request):
        data = json.loads(request.body)
        dataR= data['recibo']

        if dataR['id'] is None:
            regRecibo = RecibosIngreso()
            regSocio = Socio.objects.get(codigo=dataR['socio'])

            if dataR['NoPrestamo'] != None:
                regPrest = MaestraPrestamo.objects.get(noPrestamo=dataR['NoPrestamo'])
            
            if dataR['montoAhorro'] != None :
                regAHorro = AhorroSocio.objects.get(socio=regSocio)

            regRecibo.socioIngreso = regSocio
            regRecibo.prestamo = regPrest
            regRecibo.ahorro = regAHorro
            regRecibo.montoPrestamo = dataR['montoPrestamo']
            regRecibo.montoAhorro = dataR['montoAhorro']
            regRecibo.fecha  = dataR['fecha']
            regRecibo.estatus = dataR['estatus']
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

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

    def setCuentaMaestra(self, idMaestra, doc, Fecha, ref):
        regMaestra = MaestraAhorro.objects.get(id= idMaestra)

        cuenta = Cuentas.objects.get(codigo=doc.cuenta.codigo)

        diario = DiarioGeneral()
        diario.fecha = fecha
        diario.referencia = ref+'-' + str(idMaestra)
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
        if recibo.ahorro != None:
            regAhorro = AhorroSocio.objects.get(id=recibo.ahorro.id)

            regMaestra = MaestraAhorro()
            regMaestra.ahorro = regAhorro
            regMaestra.fecha = fecha
            regMaestra.monto = recibo.montoAhorro
            regMaestra.estatus = 'P'
            regMaestra.save()

            if regMaestra.ahorro.socio.estatus == 'Socio':
                ref = 'AHTS'
            if regMaestra.ahorro.socio.estatus == 'Empleado':
                ref = 'AHTE'


            tipo = TipoDocumento.objects.get(codigo=ref)
            doc = DocumentoCuentas.objects.filter(documento = tipo)

            for docu in doc:
                self.setCuenta(self,regMaestra.id, doc, Fecha, ref)
        
        if recibo.prestamo != None:
            self.guardarPagoCuotaPrestamo(self,recibo.prestamo.noPrestamo,recibo.montoPrestamo,0,'RIRG-'+str(recibo.id),'RI')

        return HttpResponse('Ok')

class reciboTemplateView(TemplateView):
    template_name = "reciboIng.html"

    def post(self, request):
        data = json.loads(request.body)
        dataR= data['recibo']

        if dataR['id'] is None:
            regRecibo = RecibosIngreso()
            regSocio = Socio.objects.get(codigo=dataR['socio'])

            regRecibo.socioIngreso = regSocio
            regRecibo.fecha  = dataR['fecha']
            regRecibo.estatus = dataR['estatus']

            if dataR['NoPrestamo'] != None:
                regPrest = MaestraPrestamo.objects.get(noPrestamo=dataR['NoPrestamo'])
                regRecibo.prestamo = regPrest
                regRecibo.montoPrestamo = dataR['montoPrestamo']

            if dataR['montoAhorro'] != None :
                regAHorro = AhorroSocio.objects.get(socio=regSocio)
                regRecibo.ahorro = regAHorro
                regRecibo.montoAhorro = dataR['montoAhorro']
            
            regRecibo.save()

        else:
            if data['estatus'] == 'A':
                regRecibo = RecibosIngreso.objects.get(id=data['id'])
                
                if dataR['NoPrestamo'] != None:
                    regPrest = MaestraPrestamo.objects.get(noPrestamo=dataR['NoPrestamo'])
                    regRecibo.prestamo = regPrest
                    regRecibo.montoPrestamo = dataR['montoPrestamo']

                if dataR['montoAhorro'] != None :
                    regAHorro = AhorroSocio.objects.get(socio=regSocio)
                    regRecibo.ahorro = regAHorro
                    regRecibo.montoAhorro = dataR['montoAhorro']

                regRecibo.estatus = data['estatus']
                regRecibo.save()
        return HttpResponse('Ok')

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
                'socio': recibos.socioIngreso.nombres + ' ' + recibos.socioIngreso.apellidos,
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
        return JsonResponse(data, safe=False)

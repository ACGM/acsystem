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

from .models import DetalleRecibo, RecibosIngreso, ReciboIngresoNomina

class reciboPost(TemplateView):
    template_name="recigoImp.html"

    def setCuentaMaestra(self, idMaestra, doc, Fecha, ref):
        regMaestra = MaestraAhorro.objects.get(id= idMaestra)
        
        cuenta = Cuentas.objects.get(codigo=doc.cuenta.codigo)

        diario = DiarioGeneral()
        diario.fecha = Fecha
        diario.referencia = ref+'-' + str(idMaestra)
        diario.cuenta = cuenta
        diario.estatus = 'P'

        if doc.accion == 'D':
            diario.debito = regMaestra.monto
            diario.credito = 0
        else:
            diario.debito = 0
            diario.credito = regMaestra.monto

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

            regAhorro.balance = regAhorro.balance + recibo.montoAhorro
            regAhorro.disponible = regAhorro.disponible + recibo.montoAhorro
            regAhorro.save()

            if regMaestra.ahorro.socio.estatus == 'S':
                ref = 'AHTS'
            if regMaestra.ahorro.socio.estatus == 'E':
                ref = 'AHTE'


            tipo = TipoDocumento.objects.get(codigo=ref)
            doc = DocumentoCuentas.objects.filter(documento = tipo)

            for docu in doc:
                self.setCuentaMaestra(regMaestra.id, docu, fecha, ref)
            recibo.estatus= 'P'
            recibo.save()

        if recibo.prestamo != None:
            guardarPagoCuotaPrestamo(self,recibo.prestamo.noPrestamo,recibo.montoPrestamo,0,0,'RIRG-'+str(recibo.id),'AH')

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

            if dataR['montoAhorro'] != None or dataR['montoAhorro'] == 0:
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


class reciboNominaTemplateView(TemplateView):
    template_name="ReciboNomina.html"

    def setCuentas(selt, recibo, fecha, ref, cuenta, debito, credito):
        try:
            diario = DiarioGeneral()

            diario.fecha = fecha
            diario.cuenta = Cuentas.objects.get(codigo=cuenta)
            diario.referencia = ref+str(recibo)
            diario.estatus = "P"
            diario.debito = debito
            diario.credito = credito
            diario.save()

            reciboNom = ReciboIngresoNomina.objects.get(id=recibo)
            reciboNom.cuenta.add(diario)

            return "Ok"
        except Exception, e:
            raise e
        

    def get(self, request, *args, **kwargs):

        format = self.request.GET.get('format')

        if format =="json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)


    def json_to_response(self):
        data = list()

        for reciboNom in ReciboIngresoNomina.objects.all():
            data.append({
                'id': reciboNom.id,
                'fecha': reciboNom.fecha,
                'concepto': reciboNom.concepto,
                'estatus': reciboNom.estatus,
                'cuentas':[{
                    'id': cta.id,
                    'fecha': cta.fecha,
                    'ref': cta.referencia,
                    'cuenta': cta.cuenta.codigo,
                    'debito': cta.debito,
                    'credito': cta.credito
                    }
                   for cta in reciboNom.cuentas.all()]
                })
        return JsonResponse(data, safe=False) 


    def post(self, request):
        try:
            dataR = json.loads(request.body)
            data = dataR['reciboN']
            
            fecha = data['fecha']

            if data['id'] == None:
                reciboNom = ReciboIngresoNomina()
                
                # tipo = TipoDocumento.objects.get(codigo='RINO')
                # document = DocumentoCuentas.objects.filter(documento = tipo)

                reciboNom.fecha = data['fecha']
                reciboNom.concepto = data['concepto']
                reciboNom.estatus = "R"
                reciboNom.save()

                # for doc in document:
                #     setCuentas(reciboNom.id, data['fecha'], "RINO", doc.cuenta.codigo, data['debito'], data['credito'])

            return HttpResponse("Ok")
        except Exception, e:
            raise e


class reciboPrint(TemplateView):
    template_name="ImpReciboNomina.html"
        






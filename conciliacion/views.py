import json
import decimal

from datetime import date
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets
from django.shortcuts import render

from cuenta.models import DiarioGeneral, Auxiliares, Cuentas
from administracion.models import Socio, CoBeneficiario, Suplidor

# Local Imports
from .models import SolicitudCheque, ConcCheques, NotaDCConciliacion, ConBanco
from .serializers import solicitudSerializer, chequesSerializer, NotasSerializer, ConBancoSerializer




class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = SolicitudCheque.objects.all()
    serializer_class = solicitudSerializer


class ChequesConsViewSet(viewsets.ModelViewSet):
    queryset = ConcCheques.objects.all()
    serializer_class = chequesSerializer


class NotasConsViewSet(viewsets.ModelViewSet):
    queryset = NotaDCConciliacion.objects.all()
    serializer_class = NotasSerializer


class conBancoViewSet(viewsets.ModelViewSet):
    queryset = ConBanco.objects.all()
    serializer_class = ConBancoSerializer

def prestSolicitud(self, fecha, socio, suplidor, concepto, monto, prestamo):
    try:
        solicitud = SolicitudCheque()
        solicitud.fecha = fecha
        if socio != None:
            soc = Socio.objects.get(codigo=socio)
            solicitud.socio = soc
        if suplidor != None:
            sup = Suplidor.objects.get(id=suplidor)
            solicitud.suplidor = sup
        solicitud.concepto = concepto
        solicitud.monto = monto
        solicitud.prestamo = prestamo
        solicitud.estatus = 'P'
        solicitud.save()
        return 'Ok'
    except Exception, e:
        return e.message
    
class SolicitudView(TemplateView):
    template_name = 'solicitudCheque.html'

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()
        solicitud = SolicitudCheque.objects.all()

        for sol in solicitud:
            data.append({
                'id': sol.id,
                'fecha': sol.fecha,
                'socioId': sol.socio.id if sol.socio != None else '',
                'socio': sol.socio.nombreCompleto if sol.socio != None else '',
                'suplidorId': sol.suplior.id if sol.suplior != None else '',
                'suplidor': sol.suplidor.nombre if sol.suplidor != None else '',
                'concepto': sol.concepto,
                'monto': sol.monto
            })
            return JsonResponse(data, safe=False)

    def post(self, request):
        DataT = json.loads(request.body)
        Data = DataT['solicitud']

        if Data['id'] is None:


            solicitud = SolicitudCheque()
            solicitud.fecha = Data['fecha']
            if Data['socio'] != None:
                socio = Socio.objects.get(codigo=Data['socio'])
                solicitud.socio = socio
            if Data['suplidor'] != None:
                suplidor = Suplidor.objects.get(id=Data['suplidor'])
                solicitud.suplidor = suplidor
            solicitud.concepto = Data['concepto']
            solicitud.monto = Data['monto']
            solicitud.estatus = Data['estatus']
            solicitud.save()
        else:
            solicitud = SolicitudCheque.objects.get(id=Data['id'])
            solicitud.concepto = Data['concepto']
            solicitud.monto = Data['monto']
            solicitud.estatus = Data['estatus']
            solicitud.save()

        return HttpResponse('1')


class SSolicitud(TemplateView):
    template_name = 'impSolicitud.html'

    def post(self, request):
        data = json.loads(request.body)
        try:
            sol = SolicitudCheque.objects.get(id=data['solicitud'])
            sol.estatus = data['estatus']
            sol.save()

            return HttpResponse("Ok")
        except Exception, e:
            return HttpResponse(e.message)
        
    
class ChequesView(TemplateView):
    template_name = 'ConciliacionCheque.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        cheque = ConcCheques.objects.all()

        for chk in cheque:
            data.append({
                'id': chk.id,
                'solicitudId': chk.solicitud.id + '-' + chk.solicitud.fecha,
                'noCheque': chk.chequeNo,
                'fecha': chk.fecha,
                'estatus': chk.estatus
            })
        return JsonResponse(data, safe=False)

    def post(self, request):
        DataT = json.loads(request.body)
        Data = DataT['cheque']

        if Data['id'] is None:
            solicitud = SolicitudCheque.objects.get(id=Data['solicitud'])

            cheque = ConcCheques()
            cheque.solicitud = solicitud
            cheque.chequeNo = Data['noCheque']
            cheque.fecha = Data['fecha']
            cheque.estatus = 'R'
            cheque.save()

        else:
            cheque = ConcCheques.objects.get(id=Data['id'])
            cheque.fecha = Data['fecha']
            cheque.estatus = Data['estatus']
            cheque.save()

        return HttpResponse('1')


class NotasConciliacionView(TemplateView):
    template_name = 'NotasConciliacion.html'

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        notaConc = NotaDCConciliacion.objects.all()

        for nota in notaConc:
            data.append({
                'id': nota.id,
                'concepto': nota.concepto,
                'fecha': nota.fecha,
                'tipo': nota.tipo,
                'monto': nota.monto,
                'estatus': nota.estatus,
                'cuenta': [{
                               'fecha': ctas.fecha,
                               'cuentaId': ctas.cuenta.codigo,
                               'cuenta': ctas.cuenta.descripcion,
                               'referencia': ctas.referencia,
                               'auxiliarId': ctas.auxiliar.codigo,
                               'auxiliar': ctas.auxiliar.descripcion,
                               'estatus': ctas.estatus,
                               'debito': ctas.debito,
                               'credito': ctas.credito

                           }
                           for ctas in DiarioGeneral.objects.filter(referencia='NCC-' + str(nota.id))]
            })
        return JsonResponse(data, safe=False)

    def post(self, request):
        DataT = json.loads(request.body)

        Data = DataT['Notas']
        try:
            if Data['id'] is None:
                nota = NotaDCConciliacion()
                nota.fecha = Data['fecha']
                nota.concepto = Data['concepto']
                nota.monto = decimal.Decimal(Data['monto'])
                nota.tipo = Data['tipo']
                nota.estatus = Data['estatus']
                nota.save()
            else:
                nota = NotaDCConciliacion.objects.get(id=1)
                nota.concepto = Data['concepto']
                nota.estatus = Data['estatus']
                nota.save()

            return HttpResponse('Ok')   
        except Exception, e:
            return HttpResponse(e.message)
        

class SSNotasView(DetailView):
    queryset = NotaDCConciliacion.objects.all()

    def get(self, request, *args, **kwargs):
        fechaI = request.GET.get('fechaI')
        fechaF = request.GET.get('fechaF')

        return self.json_to_response(fechaI, fechaF)

    def json_to_response(self, fechaI, fechaF):
        Data = list()

        registros = ConBanco.objects.raw('select id, concepto, '
                                         'fecha, tipo, '
                                         'monto, estatus '
                                         'from conciliacion_notadcconciliacion'
                                         'WHERE fecha BETWEEN '+fechaI+' AND '+fechaF)

        for detalle in registros:
            Data.append({
                'id': detalle.id,
                'fecha': detalle.fecha,
                'concepto': detalle.concepto,
                'tipo': detalle.tipo,
                'monto': detalle.monto,
                'estatus': detalle.estatus,
            })

        return JsonResponse(Data, safe=False)

    def post(self, request):
        DataT = json.loads(request.body)
        Data = DataT['cuenta']

        regCuenta = Cuentas.objects.get(codigo=Data['cuenta'])
        regNota = NotaDCConciliacion.objects.get(id=Data['nota'])

        regDiario = DiarioGeneral()
        regDiario.cuenta = regCuenta
        regDiario.fecha = Data[fecha]
        regDiario.referencia = Data['ref']
        regDiario.estatus = 'P'
        regDiario.debito = data['debito']
        regDiario.credito = data['credito']
        regDiario.save()

        regNota.cuentas.add(regDiario)


class ConBancoView(TemplateView):
    template_name = "ConBanco.html"

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        Data = list()

        bancaria = ConBanco.objects.all()

        for banc in bancaria:
            Data.append({
                'id': banc.pk,
                'fecha': banc.fecha,
                'descripcion': banc.descripcion,
                'tipo': banc.tipo,
                'monto': banc.monto,
                'estatus': banc.estatus
            })

        return JsonResponse(Data, safe=False)

    def post(self, request):
        DataT = json.loads(request.body)
        Data = DataT['banco']

        if Data['id'] is None:
            banco = ConBanco()
            banco.fecha = Data['fecha']
            banco.descripcion = Data['descripcion']
            banco.tipo = Data['tipo'],
            banco.monto = Data['monto']
            banco.estatus = Data['estatus']
            banco.save()
        else:
            banco = ConBanco.objects.get(id=Data['id'])
            banco.fecha = Data['fecha']
            banco.descripcion = Data['descripcion']
            banco.estatus = Data['estatus']
            banco.monto = Data['monto']
            banco.save(())
        return HttpResponse(Data['tipo'])

        
class ConBancoLs(DetailView):
    queryset = ConBanco.objects.all()

    def get(self, request, *args, **kwargs):
        fechaI = request.GET.get('fechaI')
        fechaF = request.GET.get('fechaF')

        return self.json_to_response(fechaI, fechaF)

    def json_to_response(self, fechaI, fechaF):
        Data = list()

        registros = ConBanco.objects.raw('select id, fecha, '
                                         'descripcion, tipo, '
                                         'monto, estatus '
                                         'from conciliacion_conbanco '
                                         'WHERE fecha BETWEEN ' + fechaI + ' AND ' + fechaF)

        for detalle in registros:
            Data.append({
                'id': detalle.id,
                'fecha': detalle.fecha,
                'descripcion': detalle.descripcion,
                'tipo': detalle.tipo,
                'monto': detalle.monto,
                'estatus': detalle.estatus,
            })

        return JsonResponse(Data, safe=False)

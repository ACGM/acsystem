import json
import decimal

from datetime import date
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets
from django.shortcuts import render

from cuenta.models import DiarioGeneral, Auxiliares, Cuentas
from administracion.models import Socio, CoBeneficiario

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


class SolicitudView(TemplateView):
    template_name = 'solicitudCheque.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
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
                'socioId': sol.socio.id,
                'socio': sol.socio.nombreCompleto,
                'concepto': sol.concepto,
                'monto': sol.monto,
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
                           for ctas in DiarioGeneral.objects.filter(referencia='SLC-' + str(sol.id))]
            })
            return JsonResponse(data, safe=False)

    def post(self, request):
        DataT = json.loads(request.body)
        Data = DataT['solicitud']

        if Data['id'] is None:
            socio = Socio.objects.get(id=Data['socioId'])

            solicitud = SolicitudCheque()
            solicitud.fecha = Data['fecha']
            solicitud.socio = socio
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
        self.object_list = self.get_queryset()
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

        if Data['id'] is None:
            nota = NotaDCConciliacion()
            nota.fecha = Data['fecha']
            nota.concepto = Data['concepto']
            nota.monto = Data['estatus']
            nota.tipo = Data['tipo']
            nota.estatus = Data['estatus']
            nota.save()
        else:
            nota = NotaDCConciliacion.objects.get(id=Data['id'])
            nota.concepto = Data['concepto']
            nota.estatus = Data['estatus']
            nota.save()

        return HttpResponse('1')


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


class ConBancoView(TemplateView):
    template_name = "ConBanco.html"

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
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
                'id': banc.id,
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

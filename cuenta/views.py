from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets

from django.views.generic import DetailView, TemplateView, View

from django.shortcuts import render

from .models import Cuentas, Auxiliares, DiarioGeneral, CuentasControl
from administracion.models import TipoDocumento

from .serializers import CuentasSerializer, AuxiliarSerializer, DiarioSerializer,  \
    CuentasControlSerializer

import json


# Cuentas Busqueda (GENERICO)
def cuentasSearch(request):
    return render(request, 'cuentas_search.html')

class MaestroView(View):

    def get(self, request, *args, **kwargs):
        # self.object_list = self.get_queryset()

        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()
        Mayor = DiarioGeneral.objects.raw('select s.id \
                                             ,s.fecha\
                                             ,s.codigo \
                                             ,sum(s.debito) as debito \
                                             ,sum(s.credito) as credito\
                                             from (\
                                                 select di.id\
                                                 ,di.fecha\
                                                 ,c.codigo\
                                                 ,sum(di.debito) as debito\
                                                 ,sum(di.credito) as credito \
                                                 from cuenta_diariogeneral as di \
                                                    left join cuenta_cuentas c on c.id = di.cuenta_id\
                                                    where di.cuenta_id is not NULL group by di.fecha, c.codigo\
                                             union \
                                                 select di.id\
                                                 ,di.fecha\
                                                 ,c.codigo\
                                                 ,sum(di.debito) as debito\
                                                 ,sum(di.credito) as credito\
                                                    from cuenta_diariogeneral as di\
                                                 left join cuenta_auxiliares au on au.id =di.auxiliar_id\
                                                 left join cuenta_cuentas c on c.id = au.cuenta_id\
                                                 where di.auxiliar_id is not NULL\
                                                 group by di.fecha, c.codigo) as s group by s.codigo\
                                                  order by s.fecha, s.codigo ')

        for maestro in Mayor:
            data.append({
                'fecha': maestro.fecha,
                'cuenta': maestro.codigo,
                'debito': maestro.debito,
                'credito': maestro.credito
            })

        return JsonResponse(data, safe=False)


class CuentasView(DetailView):
    queryset = Cuentas.objects.all()

    def post(self, request):
        try:
            data = json.loads(request.body)
            regId = data['id']

            if regId == None:
                regDiario = DiarioGeneral()
                regDiario.fecha = data['fecha']
                if data['cuenta'] != None:
                    regDiario.cuenta = data['cuenta']

                regDiario.referencia = data['ref']

                if data['auxiliar'] != None:
                    regDiario.auxiliar = data['auxiliar']

                regDiario.tipoDoc = TipoDocumento.objects.filter(tipoDoc=data['tipoDoc'])
                regDiario.estatus = data['estatus']
                regDiario.debito = data['debito']
                regDiario.credito = data['credito']
                regDiario.save()

            else:
                regDiario = DiarioGeneral.objects.filter(referencia=regId)
                if data['cuenta'] != None:
                    regDiario.cuenta = data['cuenta']

                if data['auxiliar'] != None:
                    regDiario.auxiliar = data['auxiliar']

                regDiario.tipoDoc = TipoDocumento.objects.filter(tipoDoc=data['tipoDoc'])
                regDiario.estatus = data['estatus']
                regDiario.debito = data['debito']
                regDiario.credito = data['credito']
                regDiario.save()

            return HttpResponse('1')
        except Exception as ex:
            return HttpResponse(ex)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        format = self.request.GET.get('format')

        if hasattr(self, 'idReg'):
            self.idReg = self.request.Get.get('idReg')
        else:
            self.idReg = None

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        if self.idReg != None:
            regDiario = DiarioGeneral.objects.filter(referencia=self.idReg)

            for item in regDiario:
                data.append({
                    'id': item.id,
                    'cuenta': item.cuenta.codigo if item.cuenta != None else '',
                    'auxiliar': item.auxiliar.codigo if item.auxiliar != None else '',
                    'ref': item.referencia,
                    'fecha': item.fecha,
                    'estatus': item.estatus,
                    'debito': item.debito,
                    'credito': item.credito
                })
        else:
            regDiario = DiarioGeneral.objects.all()

            for item in regDiario:
                data.append({
                    'id': item.id,
                    'cuenta': item.cuenta.codigo if item.cuenta != None else '',
                    'auxiliar': item.auxiliar.codigo if item.auxiliar != None else '',
                    'ref': item.referencia,
                    'fecha': item.fecha,
                    'estatus': item.estatus,
                    'debito': item.debito,
                    'credito': item.credito
                })
        return JsonResponse(data, safe=False)


class CuentasViewSet(viewsets.ModelViewSet):
    queryset = Cuentas.objects.all()
    serializer_class = CuentasSerializer


class AuxiliarViewSet(viewsets.ModelViewSet):
    queryset = Auxiliares.objects.all()
    serializer_class = AuxiliarSerializer


class DiarioViewSet(viewsets.ModelViewSet):
    queryset = DiarioGeneral.objects.all()
    serializer_class = DiarioSerializer


class CuentaControlViewSet(viewsets.ModelViewSet):
    queryset = CuentasControl.objects.all()
    serializer_class = CuentasControlSerializer


class diarioView(TemplateView):
    template_name = 'Diario.html'


class mayorView(TemplateView):
    template_name = 'Mayor.html'
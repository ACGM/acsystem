from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets

from django.views.generic import DetailView, TemplateView, View

from django.shortcuts import render

from .models import Cuentas, DiarioGeneral, CuentasControl
from administracion.models import TipoDocumento

from .serializers import CuentasSerializer, DiarioSerializer,  \
    CuentasControlSerializer

import json


# Cuentas Busqueda (GENERICO)
def cuentasSearch(request):
    return render(request, 'cuentas_search.html')

class MaestroView(View):

    def get(self, request, *args, **kwargs):

        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()
        Mayor = DiarioGeneral.objects.raw('select di.id\
                                                 ,di.fecha\
                                                 ,c.codigo\
                                                 ,c.descripcion\
                                                 ,sum(di.debito) as debito\
                                                 ,sum(di.credito) as credito \
                                                 from cuenta_diariogeneral as di \
                                                    left join cuenta_cuentas c on c.id = di.cuenta_id\
                                                    where di.cuenta_id is not NULL group by di.fecha, c.codigo order by di.id , c.codigo' )

        for maestro in Mayor:
            data.append({
                'fecha': maestro.fecha,
                'cuenta': maestro.codigo,
                'descripcion': maestro.descripcion,
                'debito': maestro.debito,
                'credito': maestro.credito
            })

        return JsonResponse(data, safe=False)


class CuentasView(DetailView):
    queryset = Cuentas.objects.all()

    def post(self, request):
        DataT = json.loads(request.body)
        Data = DataT['cuenta']

        try:

            if DiarioGeneral.objects.filter(referencia=Data['ref'], cuenta__codigo=Data['codCuenta'], credito=Data['credito']).exists():
                raise Exception('-Este documento fue posteado')

            cta = Cuentas.objects.get(codigo=Data['codCuenta'])
            diario = DiarioGeneral()
            diario.cuenta = cta
            diario.fecha = Data['fecha']
            diario.referencia = Data['ref']
            diario.estatus = Data['estatus']
            diario.debito = Data['debito']
            diario.credito = Data['credito']
            diario.save()

            return HttpResponse(str(diario.id))
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
                    'cDescripcion': item.cuenta.descripcion if item.cuenta != None else '',
                    'aDescripcion': item.auxiliar.descripcion if item.auxiliar != None else '',
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
                    'cDescripcion': item.cuenta.descripcion if item.cuenta != None else '',
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
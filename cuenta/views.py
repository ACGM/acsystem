from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets
<<<<<<< HEAD
from django.views.generic import DetailView, TemplateView
=======
from django.views.generic import DetailView
from django.shortcuts import render
>>>>>>> FETCH_HEAD

from .models import Cuentas, Auxiliares, DiarioGeneral, TipoDocumento, CuentasControl
from .serializers import CuentasSerializer, AuxiliarSerializer, DiarioSerializer, TipoDocSerializer, \
    CuentasControlSerializer

import json


# Cuentas Busqueda (GENERICO)
def cuentasSearch(request):
    return render(request, 'cuentas_search.html')


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
                    'tipoDoc': item.tipoDoc.tipoDoc,
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
                    'tipoDoc': item.tipoDoc.tipoDoc,
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


class TipoDocViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocSerializer


class CuentaControlViewSet(viewsets.ModelViewSet):
    queryset = CuentasControl.objects.all()
    serializer_class = CuentasControlSerializer


class diarioView(TemplateView):
    template_name = 'Diario.html'
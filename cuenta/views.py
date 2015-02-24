from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets
from django.views.generic import DetailView

from .models import Cuentas, Auxiliares, DiarioGeneral, TipoDocumento, CuentasControl
from .serializers import CuentasSerializer, AuxiliarSerualizer, DiarioSerializer, TipoDocSerializer, \
    CuentasControlSerializer

import json


class CuentasView(DetailView):
    queryset = Cuentas.objects.all()

    def post(self, request):
        InfoType = self.request.Get.get('tipo')
        try:
            data = json.loads(request.body)
            regId=data['id']

            if regId == None:
                if InfoType == 'diario':
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

                if InfoType == 'cuenta':
                    regCuenta = Cuentas()
                    regCuenta.codigo = data['codigo']
                    regCuenta.descripcion = data['descripcion']
                    regCuenta.origen = data['origen']
                    regCuenta.control = data['control']
                    regCuenta.save()

                if InfoType == 'aux':
                    regAux = Auxiliares()
                    regAux.codigo = data['codigo']
                    regAux.descripcion = data['descripcion']
                    regAux.cuenta = data['cuenta']
                    regAux.save()

            else:
                if InfoType == 'diario':
                    regDiario = DiarioGeneral.objects.filter(referencia = regId)
                    if data['cuenta'] != None:
                        regDiario.cuenta = data['cuenta']

                    if data['auxiliar'] != None:
                        regDiario.auxiliar = data['auxiliar']

                    regDiario.tipoDoc = TipoDocumento.objects.filter(tipoDoc=data['tipoDoc'])
                    regDiario.estatus = data['estatus']
                    regDiario.debito = data['debito']
                    regDiario.credito = data['credito']
                    regDiario.save()

                if InfoType == 'cuenta':
                    regCuenta = Cuentas.objects.filter(codigo=regId)
                    regCuenta.descripcion = data['descripcion']

                if InfoType == 'aux':
                    regAux = Auxiliares.objects.filter(codigo =regId)
                    regAux.descripcion = data['descripcion']
                    regAux.cuenta = data['cuenta']
            return HttpResponse('1')
        except Exception as ex:
            return HttpResponse(ex)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        format = self.request.GET.get('format')
        if hasattr(self, 'tipo'):
            self.tipo = self.request.GET.get('tipo')
        else:
            self.tipo = None

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

        if self.tipo == 'cuenta':
            if self.idReg != None:
                regCuentas = Cuentas.objects.filter(codigo=self.idReg)

                data.append({
                    'codigo': regCuentas.codigo,
                    'descripcion': regCuentas.descripcion,
                    'origen': regCuentas.origen,
                    'control': regCuentas.control,
                    'cuentaControl': regCuentas.cuentaControl
                    }
                )
            else:
                regCuentas = self.object_list

                for item in regCuentas:
                    data.append({
                        'codigo': item.codigo,
                        'descripcion': item.descripcion,
                        'origen': item.origen,
                        'control': item.control,
                        'cuentaControl': item.cuentaControl
                    })


        elif self.tipo == 'diario':
            if self.idReg != None:
                regDiario = DiarioGeneral.objects.filter(referencia=self.idReg)

                for item in regDiario:
                    data.append({
                        'id': item.id,
                        'cuenta': item.cuenta,
                        'auxiliar': item.auxiliar,
                        'ref': item.referencia,
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
                        'cuenta': item.cuenta,
                        'auxiliar': item.auxiliar,
                        'ref': item.referencia,
                        'tipoDoc': item.tipoDoc.tipoDoc,
                        'estatus': item.estatus,
                        'debito': item.debito,
                        'credito': item.credito
                })
        else:
            if self.idReg != None:
                regAux = Auxiliares.objects.filter(codigo=self.idReg)

                data.append({
                    'codigo': regAux.codigo,
                    'Descripcion': regAux.descripcion,
                    'cuenta': regAux.cuenta
                })
            else:
                regAux = Auxiliares.objects.all()

                for item in regAux:
                    data.append({
                        'codigo': item.codigo,
                        'descripcion': item.descripcion,
                        'cuenta': item.cuenta
                    })
        return JsonResponse(data, safe=False)


class CuentasViewSet(viewsets.ModelViewSet):
    queryset = Cuentas.objects.all()
    serializer_class = CuentasSerializer


class AuxiliarViewSet(viewsets.ModelViewSet):
    queryset = Auxiliares.objects.all()
    serializer_class = AuxiliarSerualizer


class DiarioViewSet(viewsets.ModelViewSet):
    queryset = DiarioGeneral.objects.all()
    serializer_class = DiarioSerializer


class TipoDocViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocSerializer


class CuentaControlViewSet(viewsets.ModelViewSet):
    queryset = CuentasControl.objects.all()
    serializer_class = CuentasControlSerializer
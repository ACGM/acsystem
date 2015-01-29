from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets
from django.views.generic import DetailView

from .models import Cuentas, Auxiliares, DiarioGeneral, TipoDocumento, CuentasControl
from .serializers import CuentasSerializer, AuxiliarSerualizer, DiarioSerializer, TipoDocSerializer, \
    CuentasControlSerializer

import json
import decimal


class CuentasView(DetailView):
    queryset = Cuentas.objects.all()
    solTipo = ''

    def __init__(self, **kwargs):
        super(CuentasView, self).__init__(**kwargs)
        self.object_list = self.get_queryset()

    def post(self, request, *args, **kwargs):
        InfoType = self.request.Get.get('infoType')

        try:
            if InfoType == 'cuentas':
                data = json.loads(request.body)

                cta = data['codigo']
                ctId = data['id']

                if ctId != None:
                    regCuenta = Cuentas.objects.filter(id=ctId)
                    regCuenta.descripcion = data['descripcion']
                    regCuenta.save()

                if cta != None:
                    regCuenta = Cuentas.objects.filter(codigo=cta)
                    if regCuenta == None:
                        regCuenta = Cuentas()
                        regCuenta.codigo = data['codigo']
                        regCuenta.descripcion = data['descripcion']
                        regCuenta.origen = data['origen']
                        regCuenta.control = data['control']
                        regCuenta.cuentasControl = data['cuentaControl']
                        regCuenta.save()

            elif InfoType == 'Diario':
                data = json.loads(request.body)

                for item in data:
                    drid = data['id']

                    if drid != None:
                        regDiario = DiarioGeneral.objects.get(id=drid)
                        regDiario.referencia = data['referencia']
                        regDiario.auxiliar = data['auxiliar']
                        regDiario.tipoDoc = data['tipoDoc']
                        regDiario.estatus = data['estatus']
                        regDiario.debito = data['debito']
                        regDiario.credito = data['credito']
                        regDiario.save()

                    else:
                        regDiario = DiarioGeneral()
                        regDiario.fecha = data['fecha']
                        regDiario.cuenta = data['cuenta']
                        regDiario.referencia = data['referencia']
                        regDiario.Auxiliares = data['auxiliar']
                        regDiario.tipoDoc = data['tipoDoc']
                        regDiario.estatus = data['estatus']
                        regDiario.debito = data['debito']
                        regDiario.credito = data['credito']
                        regDiario.save()
            else:
                data = json.load(request.body)

                aux = data['codigo']
                auxId = data['id']

                if aux != None:
                    regAuxiliar = Auxiliares.objects.get(id=auxId)
                    regAuxiliar.descripcion = data['descripcion']
                    regAuxiliar.save()
                else:
                    regAuxiliar = Auxiliares()
                    regcuenta = Cuentas.objects.get(codigo=data['cuenta'])
                    regAuxiliar.codigo = data['codigo']
                    regAuxiliar.descripcion = data['descripcion']
                    regAuxiliar.cuenta = regcuenta
                    regAuxiliar.save()

            return HttpResponse('1')
        except Exception as ex:
            return HttpResponse(ex)

    def get(self, request, *args, **kwargs):
        self.solTipo = self.request.GET.get('solicitud')

        if hasattr(self, 'idReg'):
            self.idReg = self.request.Get.get('idReg')
        else:
            self.idReg = None

        format = self.request.GET.get('format')

        if format == 'json':
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        if self.solTipo == 'diario':
            if self.idReg != None:
                regDiario = DiarioGeneral.objects.get(id=self.idReg)
            else:
                regDiario = DiarioGeneral.objects.all()

            for diario in regDiario:
                data.append({
                    'id': diario.id,
                    'fecha': diario.fecha,
                    'cuenta': diario.cuenta.codigo,
                    'referencia': diario.referencia,
                    'auxiliar': diario.auxiliar,
                    'tipoDoc': diario.tipoDoc.tipoDoc,
                    'estatus': diario.estatus,
                    'debito': diario.debito,
                    'credito': diario.credito
                })
        else:
            if self.solTipo == 'cuenta':
                if self.idReg != None:
                    regCuenta = Cuentas.objects.get(id=self.idReg)
                else:
                    regCuenta = Cuentas.objects.all()

                for cuenta in regCuenta:
                    data.append({
                        'id': cuenta.id,
                        'codigo': cuenta.codigo,
                        'descripcion': cuenta.descripcion,
                        'origen': cuenta.origen,
                        'control': cuenta.control  # 'cuentaControl' : cuenta.cuentaControl.pk
                    })
            else:
                if self.solTipo == 'aux':
                    if self.idReg != None:
                        auxList = Auxiliares.objects.get(id=self.idReg)
                    else:
                        auxList = Auxiliares.objects.all()

                    for aux in auxList:
                        data.append({
                            'id': aux.id,
                            'codigo': aux.codigo,
                            'descripcion': aux.descripcion,
                            'cuenta': aux.cuenta.codigo
                        })
                else:
                    if self.idReg != None:
                        tipoList = TipoDocumento.objects.get(id=self.idReg)
                    else:
                        tipoList = TipoDocumento.objects.all()

                    for tipo in tipoList:
                        data.append({
                            'id': tipo.id,
                            'tipoDoc': tipo.tipoDoc,
                            'descripcion': tipo.descripcion
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
    queryset = CuentasControl
    serializer_class = CuentasControlSerializer
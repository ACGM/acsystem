import json
import decimal

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets

from .models import InteresesAhorro, MaestraAhorro, AhorroSocio, RetiroAhorro
from cuenta.models import DiarioGeneral, Cuentas, Auxiliares, TipoDocumento
from administracion.models import Socio
from .serializers import interesAhorroSerializer, maestraAhorroSerializer, AhorroSocioSerializer, RetiroAhorroSerializer


class MaestraAhorroView(DetailView):
    queryset = AhorroSocio.objects.all()

    # Metodo Post para el proceso completo
    def post(self, request, *args, **kwargs):

        try:
            data = json.loads(request.body)


            if data['id'] != None:
                regRet = RetiroAhorro.object.get(id = data['id'])
                regRet.tipoRetiro = data['tipo']
                regRet.monto = data['monto']
                regRet.save()
            else:
                regRet = RetiroAhorro()
                regRet.ahorro = AhorroSocio.objects.get(id=data['ahorro'])
                regRet.socio = Socio.objects.get(id=data['socio'])
                regRet.tipoRetiro = data['tipo']
                regRet.monto = decimal.Decimal(data['monto'])

            return HttpResponse('1')

        except Exception as ex:
            return HttpResponse(ex)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        format = self.request.GET.get('format')
        self.tipo = self.request.GET.get('tipo')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()
        if self.tipo == 'AR':
            for ahorro in self.object_list:
                data.append({
                    'id': ahorro.id,
                    'socioId': ahorro.socio.id,
                    'socio': ahorro.socio.nombres + ' ' + ahorro.socio.apellidos,
                    'balance': ahorro.balance,
                    'disponible': ahorro.disponible,
                    'maestra': [
                        {
                            'id': maestra.id,
                            'fecha': maestra.fecha,
                            'monto': maestra.monto,
                            'interes': maestra.interes.porcentaje,
                            'balance': maestra.balance,
                            'estatus': maestra.estatus,
                            'retiro' : maestra.retiro.id if maestra.retiro != None else '',
                            'cuentas': [
                                {
                                    'id': cuentas.id,
                                    'fecha': cuentas.fecha,
                                    'cuenta': cuentas.cuenta,
                                    'referencia': cuentas.referencia,
                                    'auxiliar': cuentas.auxiliar,
                                    'tipoDoc': cuentas.tipoDoc.tipoDoc,
                                    'estatus': cuentas.estatus,
                                    'debito': cuentas.debito,
                                    'credito': cuentas.credito,

                                }
                                for cuentas in DiarioGeneral.objects.filter(referencia=('AH-' + str(maestra.id)))]

                        }
                        for maestra in MaestraAhorro.objects.filter(ahorro=ahorro.id)]
                })
        else:
            for retiro in RetiroAhorro.objects.all():
                data.append({
                    'id': retiro.id,
                    'socio': retiro.socio.nombres + ' ' + retiro.socio.apellidos,
                    'ahorro': retiro.socio.id,
                    'tipoRetiro': retiro.tipoRetiro,
                    'monto': retiro.monto
                })

        return JsonResponse(data, safe=False)


class InteresAhorroViewSet(viewsets.ModelViewSet):
    queryset = InteresesAhorro.objects.all()
    serializer_class = interesAhorroSerializer


class MaestraAhorroViewSet(viewsets.ModelViewSet):
    queryset = MaestraAhorro.objects.all()
    serializer_class = maestraAhorroSerializer


class AhorroViewSet(viewsets.ModelViewSet):
    queryset = AhorroSocio.objects.all()
    serializer_class = AhorroSocioSerializer


class RetirosAhorroViewSet(viewsets.ModelViewSet):
    queryset = RetiroAhorro.objects.all()
    serializer_class = RetiroAhorroSerializer


class AhorroView(TemplateView):
    template_name = 'ahorro.html'




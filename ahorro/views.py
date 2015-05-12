import json
import decimal

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView, View
from rest_framework import viewsets

from .models import InteresesAhorro, MaestraAhorro, AhorroSocio, RetiroAhorro

from cuenta.models import DiarioGeneral
from prestamos.models import MaestraPrestamo
from administracion.models import Socio

from .serializers import interesAhorroSerializer, maestraAhorroSerializer, AhorroSocioSerializer, RetiroAhorroSerializer




def insMaestra(self, CodSocio, Fecha, Monto):
    regSocio = AhorroSocio.objects.get(socio__codigo=CodSocio)
    regInteres = InteresesAhorro.objects.get(id=1)
    regMaestra = MaestraAhorro()
    regMaestra.estatus = "A"
    regMaestra.fecha = Fecha
    regMaestra.interes = regInteres
    regMaestra.monto = Monto
    regMaestra.ahorro = regSocio
    regMaestra.balance = Monto + regSocio.balance
    regMaestra.save()

def getSocioAhorro(self, codSocio):
    regSocio = AhorroSocio.objects.raw('select socio_id'
                                       ', balance '
                                       'from ahorro_ahorrosocio '
                                       'where socio_id =' + codSocio)
    return regSocio


class MaestraAhorroView(DetailView):
    queryset = AhorroSocio.objects.all()

    # Metodo Post para el proceso completo
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
                    'socioId': ahorro.socio.codigo,
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
                            'retiro': maestra.retiro.id if maestra.retiro != None else '0',
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
                    'socio': retiro.socio.codigo,
                    'fecha': retiro.fecha,
                    'estatus': retiro.estatus,
                    'tipo': retiro.tipoRetiro,
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


class impRetiroAHorro(TemplateView):
    template_name = "AhorroPrint.html"


class AhorroView(TemplateView):
    template_name = 'ahorro.html'

    def BalanceSocioP(self, socio):
        prestamos = MaestraPrestamo.objects.raw('SELECT '
                                                'SUM(p.balance) balance '
                                                'FROM prestamos_maestraprestamo p '
                                                'INNER JOIN administracion_socio s ON s.id = p.socio_id '
                                                'HAVING p.estatus = \'P\' and s.codigo =' + socio \
                                                )
        return prestamos

    def post(self, request, *args, **kwargs):
        dataT = json.loads(request.body)

        data = dataT['retiro']

        regSocio = Socio.objects.get(codigo=data['socio'])
        regAhorro = AhorroSocio.objects.get(socio=regSocio.id)

        prestamos = self.BalanceSocioP(self, data['socio'])

        try:

            if data['id'] is None:

                disponible = regAhorro.balance - prestamos

                regRet = RetiroAhorro()
                regRet.socio = regSocio
                regRet.fecha = data['fecha']
                regRet.estatus = data['estatus']
                regRet.tipoRetiro = data['tipo']
                regRet.monto = decimal.Decimal(data['monto'])
                regRet.save()

                regMaestra = MaestraAhorro()
                regMaestra.ahorro = regAhorro
                regMaestra.fecha = data['fecha']
                regMaestra.retiro = regRet
                regMaestra.interes = InteresesAhorro.objects.get(id=1)
                regMaestra.monto = decimal.Decimal(data['monto'])
                regMaestra.balance = disponible - decimal.Decimal(data['monto'])
                regMaestra.estatus = 'A'
                regMaestra.save()

            elif data['estatus'] == 'I':
                regRet = RetiroAhorro.objects.get(id=data['id'])

                regRet.estatus = data['estatus']
                regRet.save()

                regMaestra = MaestraAhorro.objects.get(retiro=data['id'])
                regMaestra.estatus = data['estatus']
                regMaestra.save()

            elif data['estatus' == "P"]:
                return HttpResponse('posteada')

            elif data['estatus'] == 'A':
                regRet = RetiroAhorro.objects.get(id=data['id'])

                regRet.tipoRetiro = data['tipo']
                regRet.estatus = data['estatus']
                regRet.monto = decimal.Decimal(data['monto'])
                regRet.save()

                disponible = regAhorro.balance - prestamos

                regMaestra = MaestraAhorro.objects.get(id=data['maestraId'])
                regMaestra.monto = decimal.Decimal(data['monto'])
                regMaestra.balance = disponible - decimal.Decimal(data['monto'])
                regMaestra.estatus = data['estatus']
                regMaestra.save()

            else:
                return HttpResponse('0')

            return HttpResponse('1')

        except Exception as ex:
            return HttpResponse(ex)


class MaestraAhorroApi(DetailView):
    queryset = MaestraAhorro.objects.all()

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        regSocio = Socio.objects.get(codigo=data['socio'])
        regAhorro = AhorroSocio.objects.get(socio=regSocio)

        regMaestra = MaestraAhorro()
        regMaestra.ahorro = regAhorro
        regAhorro.fecha = data['fecha']
        regAhorro.monto = data['monto']
        regMaestra.interes = InteresesAhorro.objects.get(id=1)
        regMaestra.balance = regAhorro.disponible + decimal.Decimal(data['monto'])
        regMaestra.estatus = 'A'
        regMaestra.save()

        regAhorro.balance = regAhorro.balance + data['monto']
        regAhorro.disponible = regAhorro.disponible + data['monto']
        regAhorro.save()











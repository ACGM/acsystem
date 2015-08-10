import json
import decimal

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets

from .models import InteresesAhorro, MaestraAhorro, AhorroSocio
from cuenta.models import DiarioGeneral
from prestamos.models import MaestraPrestamo
from administracion.models import Socio

from .serializers import interesAhorroSerializer, maestraAhorroSerializer, AhorroSocioSerializer

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
    return '0'

def getSocioAhorro(self, codSocio):
    regSocio = AhorroSocio.objects.raw('select id, socio_id'
                                       ', balance '
                                       'from ahorro_ahorrosocio '
                                       'where socio_id =' + str(codSocio))
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
                        'estatus': maestra.estatus,
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
            disponible = regAhorro.balance - prestamos

            if data['id'] is None:

                regMaestra = MaestraAhorro()
                regMaestra.ahorro = regAhorro
                regMaestra.fecha = data['fecha']
                regMaestra.monto = decimal.Decimal(data['monto'])* (-1)
                regMaestra.estatus = 'A'
                regMaestra.save()

            return HttpResponse('1')

        except Exception as ex:
            return HttpResponse(ex)



 










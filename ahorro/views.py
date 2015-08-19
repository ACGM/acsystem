import json
import decimal

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets

from .models import InteresesAhorro, MaestraAhorro, AhorroSocio
from cuenta.models import DiarioGeneral, Cuentas
from prestamos.models import MaestraPrestamo
from administracion.models import Socio, DocumentoCuentas, TipoDocumento

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


def insAhorro(self, socioId):
    regSocio = Socio.objects.get(codigo=socioId)

    regAhorro = AhorroSocio()
    regAhorro.socio = regSocio
    regAhorro.balance = 0
    regAhorro.disponible = 0
    regAhorro.save()


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
                'estatus': ahorro.estatus,
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
                                'cuenta': cuentas.cuenta.codigo,
                                'referencia': cuentas.referencia,
                                'auxiliar': cuentas.auxiliar,
                                'estatus': cuentas.estatus,
                                'debito': cuentas.debito,
                                'credito': cuentas.credito,

                            }
                            for cuentas in DiarioGeneral.objects.filter(referencia=('AH-' + str(maestra.id)))]

                    }
                    for maestra in MaestraAhorro.objects.filter(ahorro=ahorro.id)]
            })

        return JsonResponse(data, safe=False)


class DocumentosAhorro(DetailView):
    queryset = DocumentoCuentas.objects.all()

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        for documento in DocumentoCuentas.objects.all():
            data.append({
                'id': documento.id,
                'codigo': documento.documento.codigo,
                'cuenta': documento.cuenta.codigo,
                'accion': documento.accion
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


class generarAhorro(TemplateView):
    template_name = "generarAhorro.html"

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        fecha = data['fecha']
        Qui = data['quincena']

        regtipo = TipoDocumento.objects.get(codigo="AH")
        regDocumentos = DocumentoCuentas.objects.filter(documento=regtipo)

        for ah in AhorroSocio.objects.filter(estatus="A"):
            socio = Socio.objects.get(codigo=ah.socio.codigo)
            if Qui == 1:
                monto = socio.cuotaAhorroQ1
            else:
                monto = socio.cuotaAhorroQ2

            regMaestra = MaestraAhorro()
            regMaestra.ahorro = ah
            regMaestra.fecha = fecha
            regMaestra.monto = monto
            regMaestra.estatus = "P"
            regMaestra.save()

            ah.balance = ah.balance + monto
            ah.disponible = ah.disponible + monto
            ah.save()

            # for cta in regDocumentos:         
            #     cuenta = DiarioGeneral()
            #     cuenta.fecha = fecha
            #     cuenta.cuenta = cta.cuenta
            #     if cta.accion == "D":
            #         cuenta.debito = monto
            #         cuenta.credito = 0
            #     else:
            #         cuenta.credito = monto
            #         cuenta.debito = 0
            #     cuenta.referencia = "AH-" + str(regMaestra.id)
            #     cuenta.estatus = "P"
            #     cuenta.save()
            #     regMaestra.cuentas = cuenta
            #     cuenta.close()

        return HttpResponse("Ok")


class generarInteres(TemplateView):
    template_name = "interesAhorro.html"

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        fechaI = data["fechaI"]
        fechaF = data["fechaF"]
        regtipo = TipoDocumento.objects.get(codigo="AHIN")
        regDocumentos = DocumentoCuentas.objects.filter(documento=regtipo)

        for ah in AhorroSocio.objects.all():
            inter = InteresesAhorro.objects.get(id=1)
            mensual = MaestraAhorro.objects.raw('select '
                                                'x.ahorro_id'
                                                ',sum(x.monto)'
                                                'from ahorro_maestraahorro x'
                                                'where x.fecha between ' + fechaI + ' and ' + fechaF + 'and x.ahorro_id =1 Group by ahorro_id')

            reInt = decimal.Decimal(inter.porcentaje / 100)
            monto = mensual[1] * reInt

            regMaestra = MaestraAhorro()
            regMaestra.ahorro = ah
            regMaestra.fecha = fechaF
            regMaestra.monto = monto
            regMaestra.estatus = "p"
            regMaestra.save()

            for cta in regDocumentos:
                cuenta = DiarioGeneral()
                cuenta.fecha = fechaF
                cuenta.cuenta = cta.cuenta
                if cta.accion == "D":
                    cuenta.debito = monto
                    cuenta.credito = 0
                else:
                    cuenta.credito = monto
                    cuenta.debito = 0
                cuenta.referencia = "AH-" + str(regMaestra.id)
                cuenta.estatus = "P"
                cuenta.save()
                regMaestra.cuentas = cuenta

            ah.balance = ah.balance + monto

        return HttpResponse("Ok")


class impRetiroAHorro(TemplateView):
    template_name = "AhorroPrint.html"

class historicoAHView(TemplateView):
    template_name = "impHyAhorro.html"

class AhorroView(TemplateView):
    template_name = 'ahorro.html'

    def BalanceSocioP(self, socio):
        prestamos = MaestraPrestamo.objects.raw('SELECT '
                                                'SUM(p.balance) balance '
                                                'FROM prestamos_maestraprestamo p '
                                                'INNER JOIN administracion_socio s ON s.id = p.socio_id '
                                                'HAVING p.estatus = "P" and s.codigo =' + int(socio) \
                                                )
        return prestamos

    def post(self, request, *args, **kwargs):
        dataT = json.loads(request.body)
        data = dataT['retiro']

        regSocio = Socio.objects.get(codigo=dataT['retiro']['socio'])
        regAhorro = AhorroSocio.objects.get(socio=regSocio.id)

        balance = regAhorro.balance

        try:
            disponible = balance
            if dataT['retiro']['id'] is None:
                balance = balance  - decimal.Decimal(dataT['retiro']['monto']) 
                regMaestra = MaestraAhorro()
                regMaestra.ahorro = regAhorro
                regMaestra.fecha = dataT['retiro']['fecha']
                regMaestra.monto = decimal.Decimal(dataT['retiro']['monto']) * (-1)
                regMaestra.estatus = dataT['retiro']['estatus']
                regMaestra.save()

                # for cta in dataT['retiro']['cuentas']:
                #     cuent = Cuentas.objects.get(codigo=cta['cuenta'])
                #     diario = DiarioGeneral()
                #     diario.fecha = dataT['retiro']['fecha']
                #     diario.cuenta = cuent
                #     diario.referencia = 'RAH-'+str(regMaestra.id)
                #     diario.estatus = 'P'
                #     if cta['accion'] == 'C':
                #         diario.credito = decimal.Decimal(dataT['retiro']['monto'])
                #         diario.decimal = 0
                #     else:
                #         diario.credito = 0
                #         diario.decimal = decimal.Decimal(dataT['retiro']['monto'])
                #     diario.save()
                regAhorro.balance = balance
                regAhorro.disponible = disponible
                regAhorro.save()

            return HttpResponse(dataT['retiro']['cuentas'])

        except Exception as ex:
            return HttpResponse(ex)

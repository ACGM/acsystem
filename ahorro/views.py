import json
import decimal

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets

from .models import InteresesAhorro, MaestraAhorro, AhorroSocio, ahorroGenerados
from cuenta.models import DiarioGeneral, Cuentas
from prestamos.models import MaestraPrestamo
from prestamos.views import guardarPagoCuotaPrestamo
from administracion.models import Socio, DocumentoCuentas, TipoDocumento

from .serializers import interesAhorroSerializer, maestraAhorroSerializer, AhorroSocioSerializer


def BalanceSocioP(self, socio):
        prestamos = MaestraPrestamo.objects.raw('SELECT '
                                                'SUM(p.balance) balance '
                                                'FROM prestamos_maestraprestamo p '
                                                'INNER JOIN administracion_socio s ON s.id = p.socio_id '
                                                'HAVING p.estatus = "P" and s.codigo =' + int(socio) \
                                                )
        return prestamos

def setCuentaMaestra(self, idMaestra, doc, fecha, ref):
    regMaestra = MaestraAhorro.objects.get(id= idMaestra)
    cuenta = Cuentas.objects.get(codigo=doc.cuenta.codigo)

    diario = DiarioGeneral()
    diario.fecha = fecha
    diario.referencia = ref+'-'+ str(idMaestra)
    diario.cuenta = cuenta
    diario.estatus = 'P'

    if doc.accion == 'D':
        diario.debito = regMaestra.monto
        diario.credito = 0
    else:
        diario.debito = 0
        diario.credito = regMaestra.monto

    diario.save()


    regMaestra.cuentas.add(diario)
    return diario.id


def insMaestra(self, CodSocio, Fecha, Monto):
    regSocio = AhorroSocio.objects.get(socio__codigo=CodSocio)
    regInteres = InteresesAhorro.objects.get(id=1)
    regMaestra = MaestraAhorro()
    regMaestra.estatus = "P"
    regMaestra.fecha = Fecha
    
    regMaestra.monto = Monto
    regMaestra.ahorro = regSocio
    regMaestra.save()
    prestamo = BalanceSocioP(self, CodSocio)
    ahorro = AhorroSocio.objects.get(codigo=CodSocio)
    ahorro.balance = ahorro.balance + monto
    ahorro.disponible = ahorro.disponible + monto
    ahorro.save()

    if regSocio.socio.estatus == 'Socio':
        ref = 'AHTS'
    else:
        ref = 'AHTE'

    tipo = TipoDocumento.objects.get(codigo=ref)
    doc = DocumentoCuentas.objects.filter(documento = tipo)

    for docu in doc:
        setCuentaMaestra(self,regMaestra.id, doc, Fecha, ref)

    return 'Ok'


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

    def post(self, request, *args, **kwargs):
        dataR = json.loads(request.body)
        data = dataR['registro']

        regMaestra = MaestraAhorro.objects.get(id=data['idMaestra'])
        return HttpResponse("Entro")
        if data['estatus'] == 'P':
            regMaestra.estatus = 'P'
            regAhorro = AhorroSocio.objects.get(id=regMaestra.ahorro.id)

            if regMaestra.prestamo != None:
                guardarPagoCuotaPrestamo(regMaestra.prestamo,regMaestra.prestamo,0,'RIRG-'+str(regMaestra.id),'RIRG')
                # if regAhorro.socio.estatus == 'Socio':
                #     ref = 'AHXS'
                # else:
                #     ref = 'AHXE'
            else:
                if regAhorro.socio.estatus == 'Socio':
                    ref = 'AHRS'
                else:
                    ref = 'AHRE'

            balance = regAhorro.balance
            balance = balance  - regMaestra.monto
            prestamos = self.BalanceSocioP(self,regAhorro.socio.codigo)
            disponible = balance - prestamos

            regMaestra.save()
            regAhorro.balance = balance
            regAhorro.disponible = disponible
            regAhorro.save()



            regtipo = TipoDocumento.objects.get(codigo=ref)
            regDocumentos = DocumentoCuentas.objects.filter(documento=regtipo)

            for doc in regDocumentos:
                self.setCuentaMaestra(self, regMaestra.id, doc, regMaestra.fecha, ref)

        else: 
            regMaestra.estatus = 'I'
            regMaestra.save()
        return HttpResponse('Ok')


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

            if ah.socio.estatus == 'Socio':
                referen = 'AHRS'
            else:
                referen = 'AHRE'

            regtipo = TipoDocumento.objects.get(codigo=referen)
            regDocumentos = DocumentoCuentas.objects.filter(documento=regtipo)

            ah.balance = ah.balance + monto
            ah.disponible = ah.disponible + monto
            ah.save()

            for doc in regDocumentos:
                self.setCuentaMaestra(self, regMaestra.id, doc, regMaestra.fecha, referen)

            regComp = ahorroGenerados()
            regComp,fecha = fecha
            regComp.save()

        return HttpResponse("Ok")


class generarInteres(TemplateView):
    template_name = "interesAhorro.html"

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        fechaI = data["fechaI"]
        fechaF = data["fechaF"]

        for ah in AhorroSocio.objects.all():
            
            if ah.socio.estatus == 'Socio':
                ref = 'AHIS'
            else:
                ref = 'AHIE'

            regtipo = TipoDocumento.objects.get(codigo=ref)
            regDocumentos = DocumentoCuentas.objects.filter(documento=regtipo)

            inter = InteresesAhorro.objects.get(id=1)
            mensual = MaestraAhorro.objects.raw('select '
                                                'x.ahorro_id'
                                                ',sum(x.monto) as monto'
                                                'from ahorro_maestraahorro x'
                                                'WHERE x.fecha BETWEEN ' + fechaI + ' and ' + fechaF + ' and x.ahorro_id = 1')

            data = list()
            for mes in mensual:
                data.append({
                    'id': mes.ahorro_id,
                    'monto': mes.monto
                    })

            reInt = decimal.Decimal(inter.porcentaje / 100)
            monto = data[0].monto * reInt

            regMaestra = MaestraAhorro()
            regMaestra.ahorro = ah
            regMaestra.fecha = fechaF
            regMaestra.monto = monto
            regMaestra.estatus = "p"
            regMaestra.save()

            self.setCuentaMaestra(self, regMaestra.id, regDocumentos, fechaF, ref)

            ah.balance = ah.balance + monto
            ah.save()

        return HttpResponse("Ok")

class impRetiroAHorro(TemplateView):
    template_name = "AhorroPrint.html"

class historicoAHView(TemplateView):
    template_name = "impHyAhorro.html"

class AhorroView(TemplateView):
    template_name = 'ahorro.html'

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        for doc in DocumentoCuentas.objects.all():
            data.append({
                'id': doc.id,
                'documentoId' : doc.documento.codigo,
                'documento' : doc.documento.descripcion,
                'cuenta' : doc.cuenta.codigo,
                'accion' : doc.accion
                })

        return JsonResponse(data, safe=False)

    def post(self, request, *args, **kwargs):
        dataT = json.loads(request.body)
        data = dataT['retiro']

        regSocio = Socio.objects.get(codigo=dataT['retiro']['socio'])
        regAhorro = AhorroSocio.objects.get(socio=regSocio.id)

        try:
            idMaestra = dataT['retiro']['id']
            if dataT['retiro']['id'] is None:
                
                regMaestra = MaestraAhorro()
                if dataT['retiro']['prestamo'] != None:
                    regMaestra.prestamo = dataT['retiro']['prestamo']

                regMaestra.ahorro = regAhorro
                regMaestra.fecha = dataT['retiro']['fecha']
                regMaestra.monto = decimal.Decimal(dataT['retiro']['monto']) * (-1)

                regMaestra.estatus = dataT['retiro']['estatus']
                regMaestra.save()

            else:
                regMaestra = get_object_or_404(MaestraAhorro, pk=idMaestra)
                
                regMaestra.save()

            return HttpResponse('Ok')


        except Exception as ex:
            return HttpResponse(ex)

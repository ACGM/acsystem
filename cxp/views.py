import json
import decimal
import datetime

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets
from django.utils import timezone

from cxp.models import OrdenCompra, CxpSuperCoop
from cuenta.models import DiarioGeneral, Cuentas
from administracion.models import Suplidor, Socio, TipoDocumento, DocumentoCuentas
from prestamos.models import SolicitudOrdenDespachoH
from .serializers import OrdenSerializer



def SetCuentaOrden(self, ordenId, doc, ref):
    regOrden = OrdenCompra.objects.get(id=ordenId)
    cuenta = Cuentas.objects.get(codigo=doc.cuenta.codigo)

    diario = DiarioGeneral()
    diario.fecha = fecha
    diario.referencia = ref+'-'+ str(ordenId)
    diario.cuenta = cuenta
    diario.estatus = 'P'

    if doc.accion == 'D':
        diario.debito = regOrden.monto
        diario.credito = 0
    else:
        diario.debito = 0
        diario.credito = regOrden.monto
    diario.save()

    regOrden.detalleCuentas.add(diario)


def SetCuentaSuper(self, superCxp, doc, ref):
    regSuper = CxpSuperCoop.objects.get(id=superCxp);
    cuenta = Cuentas.objects.get(codigo=doc.cuenta.codigo)

    diario = DiarioGeneral()
    diario.fecha = timezone.now()
    diario.referencia = ref+'-'+ str(superCxp)
    diario.cuenta = cuenta
    diario.estatus = 'P'

    if doc.accion == 'D':
        diario.debito = regSuper.monto - regSuper.descuento
        diario.credito = 0
    else:
        diario.debito = 0
        diario.credito = regSuper.monto - regSuper.descuento
    diario.save()

    regSuper.detalleCuentas.add(diario)

class CxpOrdenView(DetailView):
    queryset = OrdenCompra.objects.all()

    def post(self, request):

        dataT = json.loads(request.body)

        # try:
        data = dataT['Orden']

        if data['id'] is None:
        
            regOrden = OrdenCompra()
            regOrden.suplidor = Suplidor.objects.get(id=data['suplidorId'])
            regOrden.socio = Socio.objects.get(codigo=data['socioId'])
            regOrden.orden = int(data['orden'])
            regOrden.fecha = data['fecha']
            regOrden.monto = decimal.Decimal(data['monto'])
            regOrden.estatus = data['estatus']
            regOrden.save()

            regDespacho = SolicitudOrdenDespachoH.objects.get(id = data['orden'])
            regDespacho.cxp ='P'
            regDespacho.save()

        else:

            OrdenCompra.objects.filter(id=data['id']).update(monto=decimal.Decimal(data['monto']))
            OrdenCompra.objects.filter(id=data['id']).update(cuotas = decimal.Decimal(data['cuotas']))
            OrdenCompra.objects.filter(id=data['id']).update(montocuotas = decimal.Decimal(data['montoCuotas']))
        
        return HttpResponse('Ok')
        # except Exception as ex:
        #     return HttpResponse(ex)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()
        for ordenes in self.object_list:
            data.append({
                'id': ordenes.id,
                'suplidorId': ordenes.suplidor.id,
                'suplidor': ordenes.suplidor.nombre,
                'socioId': ordenes.socio.id,
                'socio': ordenes.socio.nombreCompleto,
                'orden': ordenes.orden,
                'fecha': ordenes.fecha,
                'monto': ordenes.monto,
                'estatus': ordenes.estatus,
                'detalleCuentas': [
                    {
                        'id': cuentas.id,
                        'fecha': cuentas.fecha,
                        'cuenta': cuentas.cuenta.codigo,
                        'referencia': cuentas.referencia,
                        'estatus': cuentas.estatus,
                        'debito': cuentas.debito,
                        'credito': cuentas.credito,

                    }
                    for cuentas in ordenes.detalleCuentas.all()
                ],
            
            })
        return JsonResponse(data, safe=False)


class CxpSuperCoopView(DetailView):
    queryset = CxpSuperCoop.objects.all()

    def post(self, request):
        dataT = json.loads(request.body)
        data = dataT['regSuper']

        sup = Suplidor.objects.get(id=data['suplidor'])

        cxpSuper = CxpSuperCoop()
        cxpSuper.factura = data['factura']
        cxpSuper.suplidor = sup
        cxpSuper.fecha = data['fecha']
        cxpSuper.concepto = data['concepto']
        cxpSuper.descuento = data['descuento']
        cxpSuper.monto = decimal.Decimal(data['monto'])
        cxpSuper.estatus = data['estatus']
        cxpSuper.save()

        return HttpResponse('Ok')

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        for cxpSuper in CxpSuperCoop.objects.all():
            data.append({
                'id': cxpSuper.id,
                'suplidorId': cxpSuper.suplidor.id,
                'suplidor': cxpSuper.suplidor.nombre,
                'factura': cxpSuper.factura,
                'fecha': cxpSuper.fecha,
                'concepto': cxpSuper.concepto,
                'estatus': cxpSuper.estatus,
                'monto': cxpSuper.monto,
                'descuento': cxpSuper.descuento,
                'detalleCuentas': [
                    {
                        'id': cuentas.id,
                        'fecha': cuentas.fecha,
                        'cuenta': cuentas.cuenta.codigo,
                        'referencia': cuentas.referencia,
                        'estatus': cuentas.estatus,
                        'debito': cuentas.debito,
                        'credito': cuentas.credito,

                    }
                    for cuentas in cxpSuper.detalleCuentas.all()
                ],
            })
        return JsonResponse(data, safe=False)


class CxpView(TemplateView):
    template_name = 'CxpOrden.html'

    def post(self,request):
        try:
            orden = self.request.GET.get('orden')

            regOrden = OrdenCompra.objects.get(id=orden);
            regOrden.estatus = 'P'

            if regOrden.socio.estatus == 'S':
                ref = 'CXOS'
            else:
                ref = 'CXOE'

            tipo = TipoDocumento.objects.get(codigo=ref)
            doc = DocumentoCuentas.objects.filter(documento = tipo)

            for document in doc:
                self.SetCuentaOrden(self,regOrden.id,document,ref)

            return HttpResponse('Ok')
        except Exception, e:
            return HttpResponse(e)

class cxpSuperView(TemplateView):
    template_name = 'CxpOrdenSuper.html'

    def post(self,request):
        try:
            superCxp = self.request.GET.get('super')

            regSuper = CxpSuperCoop.objects.get(id=superCxp);
            regSuper.estatus = 'P'

            ref = 'CXSS'

            tipo = TipoDocumento.objects.get(codigo=ref)
            doc = DocumentoCuentas.objects.filter(documento = tipo)

            for document in doc:
                SetCuentaSuper(self,regSuper.id,document,ref)

            regSuper.save()
            
            return HttpResponse('Ok')
        except Exception, e:
            return HttpResponse(e)

# class CxpSolicitud(DetailView):
#     queryset = OrdenCompra.objects.all()

#     def post(request):
        






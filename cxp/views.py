import json
import decimal

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets

from cxp.models import OrdenCompra, CxpSuperCoop
from cuenta.models import DiarioGeneral, Cuentas
from administracion.models import Suplidor, Socio, TipoDocumento
from .serializers import OrdenSerializer



def SetCuentaOrden(self, ordenId, doc, ref):
    regOrden = OrdenCompra.objects.get(id=ordenId)
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

    regOrden.detalleCuentas.add(diario)

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
            
            })
        return JsonResponse(data, safe=False)


class CxpSuperCoop(DetailView):
    queryset = CxpSuperCoop.objects.all()

    def post(self, request):
        data = request.body
        dataCuentas = data['cuentas']

        cxpSuper = CxpSuperCoop()
        cxpSuper.factura = data['factura']
        cxpSuper.suplidor = Suplidor.objects.filter(id=data['suplidor'])
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

        for cxpSuper in self.object_list:
            data.append({
                'id': cxpSuper.id,
                'suplidorId': cxpSuper.suplidor.id,
                'suplidor': cxpSuper.suplidor.nombre,
                'factura': cxpSuper.factura,
                'fecha': cxpSuper.fecha,
                'concepto': cxpSuper.concepto,
                'monto': cxpSuper.monto,
                'descuento': cxpSuper.descuento,
                'detalleCuentas': [
                    {
                        'id': cuentas.id,
                        'fecha': cuentas.fecha,
                        'cuenta': cuentas.cuenta,
                        'referencia': cuentas.referencia,
                        'auxiliar': cuentas.auxiliar,
                        'estatus': cuentas.estatus,
                        'debito': cuentas.debito,
                        'credito': cuentas.credito,

                    }
                    for cuentas in DiarioGeneral.objects.filter(reference='CXPS-' + cxpSuper.id)
                ]
            })


class CxpView(TemplateView):
    template_name = 'CxpOrden.html'

    def post(self,request):
        try:
            orden = self.request.GET.get('orden')

            regOrden = OrdenCompra.objects.get(id=orden);
            regOrden.estatus = 'P'

            if regOrden.socio.estatus == 'Socio':
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




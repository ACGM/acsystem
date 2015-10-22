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
from conciliacion.views import ordenSolicitud, superSolicitud
from .serializers import OrdenSerializer



def SetCuentaOrden(self, ordenId, doc, ref):
    try:    
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
        return HttpResponse('Ok')
    except Exception, e:
        return HttpResponse(e)


def SetCuentaSuper(self, superCxp, doc, ref):
    try:
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
        return HttpResponse('Ok')
    except Exception, ex:
        return HttpResponse(ex)

class CxpOrdenView(DetailView):
    queryset = OrdenCompra.objects.all()

    def post(self, request):

        dataT = json.loads(request.body)

        try:
            data = dataT['Orden']

            if data['id'] is None:
            
                regOrden = OrdenCompra()
                regOrden.suplidor = Suplidor.objects.get(id=data['suplidorId'])
                regOrden.socio = Socio.objects.get(codigo=data['socioId'])
                regOrden.orden = int(data['orden'])
                regOrden.fecha = data['fecha']
                regOrden.monto = decimal.Decimal(data['monto'])
                regOrden.estatus = data['estatus']
                regOrden.estatusCh = 'N'
                regOrden.save()

                regDespacho = SolicitudOrdenDespachoH.objects.get(id = data['orden'])
                regDespacho.cxp ='P'
                regDespacho.save()

            else:

                OrdenCompra.objects.filter(id=data['id']).update(monto=decimal.Decimal(data['monto']))
                OrdenCompra.objects.filter(id=data['id']).update(cuotas = decimal.Decimal(data['cuotas']))
                OrdenCompra.objects.filter(id=data['id']).update(montocuotas = decimal.Decimal(data['montoCuotas']))
            
            return HttpResponse('Ok')
        except Exception as ex:
            return HttpResponse(ex)

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
                'estatusCh': ordenes.estatusCh,
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
        try:
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
            cxpSuper.estatusCh = 'N'
            cxpSuper.estatus = data['estatus']
            cxpSuper.save()

            return HttpResponse('Ok')
        except Exception, e:
            return HttpResponse(e)
        

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        try:
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
                    'estatusCh': cxpSuper.estatusCh,
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
        except Exception, e:
            return HttpResponse(e)


class CxpView(TemplateView):
    template_name = 'CxpOrden.html'

    def post(self,request):
        try:
            orden = self.request.GET.get('orden')

            regOrden = OrdenCompra.objects.get(id=orden);
            regOrden.estatus = 'P'
            regOrden.estatusCh = 'S'

            if regOrden.socio.estatus == 'S':
                ref = 'CXOS'
            else:
                ref = 'CXOE'

            tipo = TipoDocumento.objects.get(codigo=ref)
            doc = DocumentoCuentas.objects.filter(documento = tipo)

            for document in doc:
                SetCuentaOrden(self,regOrden.id,document,ref)

            regOrden.save()

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
            regSuper.estatusCh = 'S'

            ref = 'CXSS'

            tipo = TipoDocumento.objects.get(codigo=ref)
            doc = DocumentoCuentas.objects.filter(documento = tipo)

            for document in doc:
                SetCuentaSuper(self,regSuper.id,document,ref)

            regSuper.save()
            
            return HttpResponse('Ok')
        except Exception, e:
            return HttpResponse(e)

class CxpSolicitud(DetailView):
    queryset = OrdenCompra.objects.all()

    def post(self, request):
        try:
            idOrden = self.request.GET.get('orden')
            orden = OrdenCompra.objects.get(id=idOrden)


            concepto = "Pago Orden #"+str(orden.id)+" del suplidor "+ str(orden.suplidor.nombre)

            reg = ordenSolicitud(self,timezone.now(), orden.suplidor.id,concepto, orden.monto, idOrden)
            if reg == 'Ok':
                orden.estatusCh = 'R'
                orden.save()
                return HttpResponse(reg)
            else:
                raise Exception(reg)
        except Exception, e:
            return HttpResponse(e.message)

class CxpSuperSolicitud(DetailView):
    queryset = CxpSuperCoop.objects.all()

    def post(self, request):
        try:
            idSuper = self.request.GET.get('super')
            cxpSuper = CxpSuperCoop.objects.get(id=idSuper)

            monto = cxpSuper.monto - cxpSuper.descuento

            reg = superSolicitud(self,timezone.now(), cxpSuper.suplidor.id, cxpSuper.concepto, monto, idSuper)

            if reg =='Ok':
                cxpSuper.estatusCh = 'R'
                cxpSuper.save()
                return HttpResponse('Ok')
            else:
                raise Exception(reg)

        except Exception, e:
            return HttpResponse(e.message)
       
        
       

        






import json
import decimal
import datetime

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets
from django.utils import timezone

from cxp.models import  OrdenGeneral, OrdenDetalleFact, cxpSuperDetalle, cxpSuperGeneral
from cuenta.models import DiarioGeneral, Cuentas
from administracion.models import Suplidor, Socio, TipoDocumento, DocumentoCuentas
from prestamos.models import SolicitudOrdenDespachoH
from conciliacion.views import ordenSolicitud, superSolicitud
from inventario.models import InventarioH
# from .serializers import OrdenSerializer



def SetCuentaOrden(self, ordenId, doc, ref):
    try:    
        regOrden = OrdenGeneral.objects.get(id=ordenId)
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
            diario.credito = regOrden.monto - regOrden.descuento
        diario.save()

        regOrden.cuentas.add(diario)
        return HttpResponse('Ok')
    except Exception, e:
        return HttpResponse(e)


def SetCuentaSuper(self, superCxp, doc, ref):
    try:
        regSuper = cxpSuperGeneral.objects.get(id=superCxp);
        cuenta = Cuentas.objects.get(codigo=doc.cuenta.codigo)

        diario = DiarioGeneral()
        diario.fecha = timezone.now()
        diario.referencia = ref+'-'+ str(superCxp)
        diario.cuenta = cuenta
        diario.estatus = 'P'

        if doc.accion == 'D':
            diario.debito = regSuper.monto 
            diario.credito = 0
        else:
            diario.debito = 0
            diario.credito = regSuper.monto - regOrden.descuento
        diario.save()

        regSuper.cuentas.add(diario)
        return HttpResponse('Ok')
    except Exception, ex:
        return HttpResponse(ex)


class CxpOrdenView(DetailView):
    queryset = OrdenGeneral.objects.all()


    def post(self, request):

        dataT = json.loads(request.body)
        dataGeneral = dataT['Orden']
        dataDetalle = dataT['Detalle']

        try:
            regGeneral = OrdenGeneral()
            regGeneral.fecha = dataGeneral['fecha']
            regGeneral.suplidor = Suplidor.objects.get(id=dataGeneral['suplidorId'])
            regGeneral.concepto = dataGeneral['concepto']
            regGeneral.monto = dataGeneral['monto']
            regGeneral.descuento = dataGeneral['descuento']
            regGeneral.estatus ='A'
            regGeneral.chk = 'N'
            regGeneral.save()

            for det in dataDetalle:
                regDetalle =OrdenDetalleFact()
                regDetalle.idRegistro = int(det['id'])
                regDetalle.fecha = det['fechaSolicitud']
                regDetalle.factura = int(det['id'])
                regDetalle.monto = decimal.Decimal(det['netoDesembolsar'])
                regDetalle.save()
                regGeneral.detalle.add(regDetalle)

                regDespacho = SolicitudOrdenDespachoH.objects.get(id = det['id'])
                regDespacho.cxp ='P'
                regDespacho.save()

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
        for ordenes in OrdenGeneral.objects.all():
            data.append({
                'id': ordenes.id,
                'suplidorId': ordenes.suplidor.id,
                'suplidor': ordenes.suplidor.nombre,
                'fecha': ordenes.fecha,
                'concepto': ordenes.concepto,
                'monto': ordenes.monto,
                'descuento': ordenes.descuento,
                'estatus': ordenes.estatus,
                'chk': ordenes.chk,
                'detalle': [{
                    'id': det.id,
                    'factura': det.factura,
                    'fecha': det.fecha,
                    'monto': det.monto,
                }
                 for det in ordenes.detalle.all()],
                'cuentas': [{
                    'id': cta.id,
                    'fecha': cta.fecha,
                    'Codcuenta': cta.cuenta.codigo,
                    'cuenta': cta.cuenta.descripcion,
                    'referencia': cta.referencia,
                    'estatus': cta.estatus,
                    'debito': cta.debito,
                    'credito': cta.credito,
                }
                for cta in ordenes.cuentas.all()],
                })
           
        return JsonResponse(data, safe=False)


class CxpSuperCoopView(DetailView):
    queryset = cxpSuperGeneral.objects.all()

    def post(self, request):
        try:
            dataT = json.loads(request.body)
            data = dataT['regSuper']
            dataD = dataT['Detalle']

            sup = Suplidor.objects.get(id=data['suplidorId'])

            superGeneral = cxpSuperGeneral()
            superGeneral.suplidor = sup
            superGeneral.fecha = data['fecha']
            superGeneral.concepto = data['concepto']
            superGeneral.monto = data['monto']
            superGeneral.descuento = data['descuento']
            superGeneral.estatus = 'A'
            superGeneral.chk = 'N'
            superGeneral.save()

            for det in dataD:
                superDet = cxpSuperDetalle()
                superDet.idRegistro = int(det['id'])
                superDet.fecha = det['fecha']
                superDet.monto = decimal.Decimal(det['totalGeneral'])
                superDet.save()
                superGeneral.detalle.add(superDet)

                invent = InventarioH.objects.get(id=det['id'])
                invent.cxp = 'P'
                invent.save()

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
            for cxpS in cxpSuperGeneral.objects.all():
                data.append({
                    'id': cxpS.id,
                    'suplidorId': cxpS.suplidor.id,
                    'suplidor': cxpS.suplidor.nombre,
                    'fecha': cxpS.fecha,
                    'concepto': cxpS.concepto,
                    'monto': cxpS.monto,
                    'descuento': cxpS.descuento,
                    'estatus': cxpS.estatus,
                    'chk': cxpS.chk,
                    'detalle': [{
                        'id': det.id,
                        'Registro': det.idRegistro,
                        'fecha': det.fecha,
                        'monto': det.monto,
                    }
                    for det in cxpS.detalle.all()],
                    'cuentas': [{
                        'id': cuentas.id,
                        'fecha': cuentas.fecha,
                        'cuenta': cuentas.cuenta.codigo,
                        'referencia': cuentas.referencia,
                        'estatus': cuentas.estatus,
                        'debito': cuentas.debito,
                        'credito': cuentas.credito,
                        }
                        for cuentas in cxpS.cuentas.all()]
                    }
                    )            
            return JsonResponse(data, safe=False)
        except Exception, e:
            return HttpResponse(e)


class CxpView(TemplateView):
    template_name = 'CxpOrden.html'

    def post(self,request):
        try:
            orden = self.request.GET.get('orden')

            regOrdenG = OrdenGeneral.objects.get(id=orden)
            regOrdenG.estatus = 'P'
            regOrdenG.save()

            if regOrdenG.descuento != 0:
                tipoD = TipoDocumento.objects.get(codigo='CXDE')
                dodD = DocumentoCuentas.objects.filter(document = tipoD)
                
                for documentD in dodD:
                    SetCuentaOrden(self,regOrdenG.id,documentD,'CXDE')

            tipo = TipoDocumento.objects.get(codigo='CXPO')
            doc = DocumentoCuentas.objects.filter(documento = tipo)

            for document in doc:
                SetCuentaOrden(self,regOrdenG.id,document,'CXPO')

            return HttpResponse('Ok')
        except Exception, e:
            return HttpResponse(e)


class cxpSuperView(TemplateView):
    template_name = 'CxpOrdenSuper.html'

    def post(self,request):
        try:
            superCxp = self.request.GET.get('super')

            regSuper = cxpSuperGeneral.objects.get(id=superCxp)
            regSuper.estatus = 'P'

            if regSuper.descuento != 0:
                tipoD = TipoDocumento.objects.get(codigo = 'CXDE')
                docD = DocumentoCuentas.objects.filter(documento = tipo)
                for document in docD:
                    SetCuentaSuper(self,regSuper.id,document, 'CXDE')

            tipo = TipoDocumento.objects.get(codigo='CXSS')
            doc = DocumentoCuentas.objects.filter(documento = tipo)

            for document in doc:
                SetCuentaSuper(self,regSuper.id,document,'CXSS')

            regSuper.save()
            
            return HttpResponse('Ok')
        except Exception, e:
            return HttpResponse(e)


class CxpSolicitud(DetailView):
    queryset = OrdenGeneral.objects.all()

    def post(self, request):
        try:
            idOrden = self.request.GET.get('orden')
            orden = OrdenGeneral.objects.get(id=idOrden)


            concepto = "Pago Orden #"+str(orden.id)+" del suplidor "+ str(orden.suplidor.nombre)

            reg = ordenSolicitud(self,timezone.now(), orden.suplidor.id,concepto, orden.monto, orden.id)
            if reg == 'Ok':
                orden.chk = 'R'
                orden.save()
                return HttpResponse(reg)
            else:
                raise Exception(reg)
        except Exception, e:
            return HttpResponse(e.message)


class CxpSuperSolicitud(DetailView):
    queryset = cxpSuperGeneral.objects.all()

    def post(self, request):
        try:
            idSuper = self.request.GET.get('super')
            cxpSuper = cxpSuperGeneral.objects.get(id=idSuper)

            monto = cxpSuper.monto - cxpSuper.descuento

            reg = superSolicitud(self,timezone.now(), cxpSuper.suplidor.id, cxpSuper.concepto, monto, idSuper)

            return HttpResponse(reg)
            if reg =='Ok':
                cxpSuper.chk = 'R'
                cxpSuper.save()
                return HttpResponse('Ok')
            else:
                raise Exception(reg)

        except Exception, e:
            return HttpResponse(e.message)

class cxpImpGeneral(TemplateView):
    template_name = "impCxp.html"
       
        
       

        






import json
import decimal

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets

from cxp.models import OrdenCompra, DetalleOrden, CxpSuperCoop
from cuenta.models import DiarioGeneral, Cuentas, Auxiliares
from administracion.models import Suplidor, Socio, TipoDocumento
from .serializers import OrdenSerializer, DetalleOrdenSerializer


class CxpOrdenView(DetailView):
    queryset = OrdenCompra.objects.all()

    def post(self, request):

        dataT = json.loads(request.body)

        try:
            data = dataT['Orden']
            dataDet = dataT['Detalle']

            if data['id'] is None:
            
                regOrden = OrdenCompra()
                regOrden.suplidor = Suplidor.objects.get(id=data['suplidorId'])
                regOrden.socio = Socio.objects.get(codigo=data['socioId'])
                regOrden.orden = int(data['orden'])
                regOrden.fecha = data['fecha']
                regOrden.monto = decimal.Decimal(data['monto'])
                regOrden.cuotas = int(data['cuotas'])
                regOrden.montocuotas = decimal.Decimal(data['montoCuotas'])
                regOrden.estatus = data['estatus']
                regOrden.save()
            
                for det in dataDet:
                    regDetalle = DetalleOrden()
                    regDetalle.articulo = det['articulo']
                    regDetalle.monto = decimal.Decimal(det['monto'])
                    regDetalle.orden = regOrden.id
                    regDetalle.save()
                    regOrden.detalleOrden.add(regDetalle)

            else:

                OrdenCompra.objects.filter(id=data['id']).update(monto=decimal.Decimal(data['monto']))
                OrdenCompra.objects.filter(id=data['id']).update(cuotas = decimal.Decimal(data['cuotas']))
                OrdenCompra.objects.filter(id=data['id']).update(montocuotas = decimal.Decimal(data['montoCuotas']))
                regOrden = OrdenCompra.objects.filter(id=data['id'])
                for det in dataDet:
                    if det['id'] is None:
                        regDetalle = DetalleOrden()
                        regDetalle.articulo = det['articulo']
                        regDetalle.monto = decimal.Decimal(det['monto'])
                        regDetalle.orden = regOrden.id
                        regDetalle.save()
                        regOrden.detalleOrden.add(regDetalle)
                    else:
                        DetalleOrden.objects.filter(id=det.id).update(articulo = det['articulo'])
                        DetalleOrden.objects.filter(id=det.id).update(monto = decimal.Decimal(det['monto']))
            
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
                'cuotas': ordenes.cuotas,
                'estatus': ordenes.estatus,
                'montoCuotas': ordenes.montocuotas,
                'detalleOrden': [
                    {
                        'id': detalle.id,
                        'articulo': detalle.articulo,
                        'monto': detalle.monto
                    }
                    for detalle in DetalleOrden.objects.filter(orden=ordenes.id)]
            })
        return JsonResponse(data, safe=False)


class CxpSuperCoop(DetailView):
    queryset = CxpSuperCoop.objects.all()

    def post(self, request):
        data = request.body
        dataCuentas = data['cuentas']

        if data['id'] is None:
            cxpSuper = CxpSuperCoop()
            cxpSuper.factura = data['factura']
            cxpSuper.suplidor = Suplidor.objects.filter(id=data['suplidor'])
            cxpSuper.fecha = data['fecha']
            cxpSuper.concepto = data['concepto']
            cxpSuper.descuento = data['descuento']
            cxpSuper.monto = decimal.Decimal(data['monto'])
            cxpSuper.estatus = data['estatus']

            cxpSuper.save()
        else:
            cxpSuper = CxpSuperCoop.objects.filter(id=data['id'])
            cxpSuper.factura = data['factura']
            cxpSuper.suplidor = Suplidor.objects.filter(id=data['suplidor'])
            cxpSuper.fecha = data['fecha']
            cxpSuper.concepto = data['concepto']
            cxpSuper.descuento = data['descuento']
            cxpSuper.monto = data['monto']
            cxpSuper.estatus = data['estatus']
            cxpSuper.save()

            if dataCuentas[0]["diario"] is not None:
                for cuenta in dataCuentas:
                    regCuenta = DiarioGeneral.objects.get(id=cuenta)
                    cxpSuper.detalleCuentas = regCuenta

        return HttpResponse('1')

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
                        'tipoDoc': cuentas.tipoDoc.tipoDoc,
                        'estatus': cuentas.estatus,
                        'debito': cuentas.debito,
                        'credito': cuentas.credito,

                    }
                    for cuentas in DiarioGeneral.objects.filter(reference='CXPS-' + cxpSuper.id)
                ]
            })


# ViewSet de ordenes de compra, listo para API
class OrdenViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.all()
    serializer_class = OrdenSerializer


# ViewSet de Detalles Ordenes
class DetalleOrderViewSet(viewsets.ModelViewSet):
    queryset = DetalleOrden.objects.all()
    serializer_class = DetalleOrdenSerializer


class CxpView(TemplateView):
    template_name = 'CxpOrden.html'

class cxpSuperView(TemplateView):
    template_name = 'CxpOrdenSuper'




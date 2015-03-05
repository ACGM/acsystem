from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView

from .models import OrdenCompra, DetalleOrden, CxpSuperCoop
from cuenta.models import DiarioGeneral, Cuentas, Auxiliares, TipoDocumento
from administracion.models import Suplidor
from .serializers import OrdenSerializer, DetalleOrdenSerializer, CxpSuperCoopSerializer
from rest_framework import viewsets

class CxpOrdenView(DetailView):
    queryset = OrdenCompra.objects.all()

    def post(self, request):
        data = request.body
        dataDet = data['detalle']
        dataCuentas = ['cuentas']

        ordenId = data['id']

        if (ordenId == None):
            regOrden = OrdenCompra()

            regOrden.suplidor = data['suplidor']
            regOrden.socio = data['socio']
            regOrden.orden = data['orden']
            regOrden.fecha = data['fecha']
            regOrden.monto = data['monto']
            regOrden.cuotas = data['cuotas']
            regOrden.montocuotas = data['montoCuotas']
            regOrden.save()

            for det in dataDet:
                regDetalle = DetalleOrden()
                regDetalle.articulo = det['articulo']
                regDetalle.monto = det['monto']
                regDetalle.orden = regOrden.id
                regDetalle.save()
                regOrden.detalleOrden.add(regDetalle)

            for cuenta in dataCuentas:
                regCuenta = DiarioGeneral()
                if cuenta['cuenta'] is not None:
                    regCuenta.cuenta = Cuentas.objects.get(codigo=cuenta['cuenta'])

                if cuenta['auxiliar'] is not None:
                    regCuenta.auxiliar = Auxiliares.objects.get(codigo=cuenta['auxiliar'])

                regCuenta.fecha = cuenta['fecha']
                regCuenta.referencia = 'CXPO-' + regOrden.id
                regCuenta.tipoDoc = TipoDocumento.objects.get(tipoDoc=cuenta['tipoDoc'])
                regCuenta.estatus = cuenta['estatus']
                regCuenta.debito = cuenta['debito']
                regCuenta.credito = cuenta['credito']
                regCuenta.save()
                regDetalle.cuentas.add(regCuenta)
        else:
            regOrden = OrdenCompra.objects.filter(id=ordenId)
            regOrden.monto = data['monto']
            regOrden.cuotas = data['cuotas']
            regOrden.montocuotas = data['montoCuotas']
            regOrden.save()

            for det in dataDet:
                regDetalle = DetalleOrden.objects.filter(id=det.id)
                regDetalle.articulo = det['articulo']
                regDetalle.monto = det['monto']
                regDetalle.save()

            for cuenta in dataCuentas:
                regCuenta = DiarioGeneral.objects.filter(id=cuenta['id'])
                regCuenta.debito = cuenta['debito']
                regCuenta.credito = cuenta['credito']
                regCuenta.save()

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
                'montoCuotas': ordenes.montocuotas,
                'detalleOrden': [
                    {
                        'id': detalle.id,
                        'articulo': detalle.articulo,
                        'monto': detalle.monto
                    }
                    for detalle in DetalleOrden.objects.filter(orden=ordenes.id)],
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
                    for cuentas in DiarioGeneral.objects.filter(reference='CXPO-' + ordenes.id)
                ]
            })
        return JsonResponse(data, safe=False)


class CxpSuperCoop(DetailView):
    queryset = CxpSuperCoop.objects.all()

    def post(self, request):
        data= request.body
        dataCuentas=data['cuentas']

        cxpSuperId=data['id']

        if cxpSuperId == None:
            cxpSuper= CxpSuperCoop()
            cxpSuper.factura=data['factura']
            cxpSuper.suplidor=Suplidor.objects.filter(id=data['suplidor'])
            cxpSuper.fecha= data['fecha']
            cxpSuper.concepto= data['concepto']
            cxpSuper.descuento= data['descuento']
            cxpSuper.monto= data['monto']
            cxpSuper.estatus= data['estatus']

            cxpSuper.save()

            for cuenta in dataCuentas:
                regCuenta = DiarioGeneral()
                if cuenta['cuenta'] is not None:
                    regCuenta.cuenta = Cuentas.objects.get(codigo=cuenta['cuenta'])

                if cuenta['auxiliar'] is not None:
                    regCuenta.auxiliar = Auxiliares.objects.get(codigo=cuenta['auxiliar'])

                regCuenta.fecha = cuenta['fecha']
                regCuenta.referencia = 'CXPS-' + cxpSuper.id
                regCuenta.tipoDoc = TipoDocumento.objects.get(tipoDoc=cuenta['tipoDoc'])
                regCuenta.estatus = cuenta['estatus']
                regCuenta.debito = cuenta['debito']
                regCuenta.credito = cuenta['credito']
                regCuenta.save()
                cxpSuper.detalleCuentas.add(regCuenta)

        else:
            cxpSuper = CxpSuperCoop.objects.filter(id=cxpSuperId)
            cxpSuper.factura=data['factura']
            cxpSuper.suplidor=Suplidor.objects.filter(id=data['suplidor'])
            cxpSuper.fecha= data['fecha']
            cxpSuper.concepto= data['concepto']
            cxpSuper.descuento= data['descuento']
            cxpSuper.monto= data['monto']
            cxpSuper.estatus= data['estatus']
            cxpSuper.save()

            for cuenta in dataCuentas:
                regCuenta= DiarioGeneral.objects.filter(id=dataCuentas['id'])
                if cuenta['cuenta'] is not None:
                    regCuenta.cuenta = Cuentas.objects.get(codigo=cuenta['cuenta'])

                if cuenta['auxiliar'] is not None:
                    regCuenta.auxiliar = Auxiliares.objects.get(codigo=cuenta['auxiliar'])

                regCuenta.fecha = cuenta['fecha']
                regCuenta.referencia = 'CXPS-' + cxpSuper.id
                regCuenta.tipoDoc = TipoDocumento.objects.get(tipoDoc=cuenta['tipoDoc'])
                regCuenta.estatus = cuenta['estatus']
                regCuenta.debito = cuenta['debito']
                regCuenta.credito = cuenta['credito']
                regCuenta.save()

            return HttpResponse('1')

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data= list()

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




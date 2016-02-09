from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets

from django.views.generic import DetailView, TemplateView, View

from django.shortcuts import render

from .models import Cuentas, DiarioGeneral, CuentasControl
from administracion.models import TipoDocumento

from .serializers import CuentasSerializer, DiarioSerializer,  \
    CuentasControlSerializer

import json
import decimal


# Cuentas Busqueda (GENERICO)
def cuentasSearch(request):
    return render(request, 'cuentas_search.html')

class MaestroView(View):

    def get(self, request, *args, **kwargs):

        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()
        Mayor = DiarioGeneral.objects.raw('select di.id\
                                                 ,di.fecha\
                                                 ,c.codigo\
                                                 ,c.descripcion\
                                                 ,sum(di.debito) as debito\
                                                 ,sum(di.credito) as credito \
                                                 from cuenta_diariogeneral as di \
                                                    left join cuenta_cuentas c on c.id = di.cuenta_id\
                                                    where di.cuenta_id is not NULL group by di.fecha, c.codigo order by di.id , c.codigo' )

        for maestro in Mayor:
            data.append({
                'fecha': maestro.fecha,
                'cuenta': maestro.codigo,
                'descripcion': maestro.descripcion,
                'debito': maestro.debito,
                'credito': maestro.credito
            })

        return JsonResponse(data, safe=False)


class CuentasView(DetailView):
    queryset = Cuentas.objects.all()

    def post(self, request):
        DataT = json.loads(request.body)
        Data = DataT['cuenta']

        try:

            if DiarioGeneral.objects.filter(referencia=Data['ref'], cuenta__codigo=Data['codCuenta'], credito=Data['credito']).exists():
                raise Exception('-Este documento fue posteado')

            cta = Cuentas.objects.get(codigo=Data['codCuenta'])
            diario = DiarioGeneral()
            diario.cuenta = cta
            diario.fecha = Data['fecha']
            diario.referencia = Data['ref']
            diario.estatus = Data['estatus']
            diario.debito = Data['debito']
            diario.credito = Data['credito']
            diario.save()

            return HttpResponse(str(diario.id))
        except Exception as ex:
            return HttpResponse(ex)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        format = self.request.GET.get('format')

        if hasattr(self, 'idReg'):
            self.idReg = self.request.Get.get('idReg')
        else:
            self.idReg = None

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        if self.idReg != None:
            regDiario = DiarioGeneral.objects.filter(referencia=self.idReg)

            for item in regDiario:
                data.append({
                    'id': item.id,
                    'cuenta': item.cuenta.codigo if item.cuenta != None else '',
                    'cDescripcion': item.cuenta.descripcion if item.cuenta != None else '',
                    'aDescripcion': item.auxiliar.descripcion if item.auxiliar != None else '',
                    'ref': item.referencia,
                    'fecha': item.fecha,
                    'estatus': item.estatus,
                    'debito': item.debito,
                    'credito': item.credito
                })
        else:
            regDiario = DiarioGeneral.objects.all()

            for item in regDiario:
                data.append({
                    'id': item.id,
                    'cuenta': item.cuenta.codigo if item.cuenta != None else '',
                    'cDescripcion': item.cuenta.descripcion if item.cuenta != None else '',
                    'ref': item.referencia,
                    'fecha': item.fecha,
                    'estatus': item.estatus,
                    'debito': item.debito,
                    'credito': item.credito
                })
        return JsonResponse(data, safe=False)


class CuentasViewSet(viewsets.ModelViewSet):
    queryset = Cuentas.objects.all()
    serializer_class = CuentasSerializer
    

class DiarioViewSet(viewsets.ModelViewSet):
    queryset = DiarioGeneral.objects.all()
    serializer_class = DiarioSerializer


class CuentaControlViewSet(viewsets.ModelViewSet):
    queryset = CuentasControl.objects.all()
    serializer_class = CuentasControlSerializer


class diarioView(TemplateView):
    template_name = 'Diario.html'

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return  self.render_to_response(context)

    def json_to_response(self):
        data = list()

        tipo = TipoDocumento.objects.all()

        for x in tipo:
            data.append({
                    'codigo' : x.codigo,
                    'descripcion' : x.descripcion
                })

        return  JsonResponse(data, safe=False)


class mayorView(TemplateView):
    template_name = 'Mayor.html'


class balanceGeneral(TemplateView):
    template_name = "BalanceGeneral.html"

class EstadoSituacion(TemplateView):
    template_name = "EstadosFinancieros.html"

class EstatoResultado(TemplateView):
    template_name = 'EstadoResultado.html'

    def get(self, request, *arg, **kwargs):
        format = self.request.GET.get('format')
        fechaI = request.GET.get('fechaI')
        fechaF = request.GET.get('fechaF')

        if format == "json":
            return self.json_to_response(fechaI, fechaF)

        context = self.get_context_data()
        return  self.render_to_response(context)


    def json_to_response(self, fechaI, fechaF):
        data = list()
        debito = decimal.Decimal(0)
        credito = decimal.Decimal(0)

        nivel1 = Cuentas.objects.filter(nivel=1)
        nivel2 = Cuentas.objects.filter(nivel=2)
        nivel3 = Cuentas.objects.filter(nivel=3)
        nivel4 = Cuentas.objects.filter(nivel=4)
        nivel5 = Cuentas.objects.filter(nivel=5)
        nivel6 = Cuentas.objects.filter(nivel=6)

        
        for n1 in nivel1:
            try:
                diario = DiarioGeneral.objects.filter(cuenta = n1, fecha__gte = fechaI, fecha__lte =fechaF)
                
                for d1 in diario:
                    debito += d1.debito
                    credito += d1.credito

                data.append({
                    'nivel' : 1,
                    'cuenta' : n1.codigo,
                    'descrip' : n1.descripcion,
                    'debito' : debito,
                    'credito' : credito,
                    'tipo' : n1.tipo,
                    'padre' : n1.cuentaControl.codigoControl if n1.cuentaControl != None else ''
                    })

                diario = None
                debito = decimal.Decimal(0)
                credito = decimal.Decimal(0)
            except Exception, e:
                pass
     
        for n2 in nivel2:
            try:
                diario = DiarioGeneral.objects.filter(cuenta = n2, fecha__gte = fechaI, fecha__lte =fechaF)
                
                for d2 in diario:
                    debito += d2.debito
                    credito += d2.credito

                data.append({
                    'nivel' : 2,
                    'cuenta' : n2.codigo,
                    'descrip' : n2.descripcion,
                    'debito' : debito,
                    'credito' : credito,
                    'tipo' : n2.tipo,
                    'padre' : n2.cuentaControl.codigoControl
                    })

                diario = None
                debito = decimal.Decimal(0)
                credito = decimal.Decimal(0)
            except Exception, e:
                pass

        for n3 in nivel3:
            try:

                diario = DiarioGeneral.objects.filter(cuenta = n3, fecha__gte = fechaI, fecha__lte =fechaF)
                
                for d3 in diario:
                    debito += d3.debito
                    credito += d3.credito

                data.append({
                    'nivel' : 3,
                    'cuenta' : n3.codigo,
                    'descrip' : n3.descripcion,
                    'debito' : debito,
                    'credito' : credito,
                    'tipo' : n3.tipo,
                    'padre' : n3.cuentaControl.codigoControl
                    })

                diario = None
                debito = decimal.Decimal(0)
                credito = decimal.Decimal(0)
            except Exception, e:
                pass

        for n4 in nivel4:
            try:
                diario = DiarioGeneral.objects.filter(cuenta = n4, fecha__gte = fechaI, fecha__lte =fechaF)
                
                for d4 in diario:
                    debito += d4.debito
                    credito += d4.credito

                data.append({
                    'nivel' : 4,
                    'cuenta' : n4.codigo,
                    'descrip' : n4.descripcion,
                    'debito' : debito,
                    'credito' : credito,
                    'tipo' : n4.tipo,
                    'padre' : n4.cuentaControl.codigoControl
                    })

                diario = None
                debito = decimal.Decimal(0)
                credito = decimal.Decimal(0)
            except Exception, e:
                pass

        for n5 in nivel5:
            try:
                diario = DiarioGeneral.objects.filter(cuenta = n5, fecha__gte = fechaI, fecha__lte =fechaF)
                
                for d5 in diario:
                    debito += d5.debito
                    credito += d5.credito

                data.append({
                    'nivel' : 5,
                    'cuenta' : n5.codigo,
                    'descrip' : n5.descripcion,
                    'debito' : debito,
                    'credito' : credito,
                    'tipo' : n5.tipo,
                    'padre' : n5.cuentaControl.codigoControl
                    })

                diario = None
                debito = decimal.Decimal(0)
                credito = decimal.Decimal(0)
            except Exception, e:
                pass

        for n6 in nivel6:
            try:
                diario = DiarioGeneral.objects.filter(cuenta = n6, fecha__gte = fechaI, fecha__lte =fechaF)
               
                for d6 in diario:
                    debito += d6.debito
                    credito += d6.credito

                data.append({
                    'nivel' : 6,
                    'cuenta' : n6.codigo,
                    'descrip' : n6.descripcion,
                    'debito' : debito,
                    'credito' : credito,
                    'tipo' : n6.tipo,
                    'padre' : n6.cuentaControl.codigoControl
                    })

                diario = None
                debito = decimal.Decimal(0)
                credito = decimal.Decimal(0)
            except Exception, e:
                pass        

        return  JsonResponse(data, safe=False) 
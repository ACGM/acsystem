import json
import decimal

from datetime import date
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets
from django.shortcuts import render

from .models import CategoriaActivo, Depresiacion, Activos
from .serializers import CategoriaActivoSerializer, DepresiacionSerializer, ActivosSerializer
from cuenta.models import DiarioGeneral, Auxiliares, Cuentas
from administracion.models import Suplidor, Localidad


# Viewsets Para activos
class CategoriaActivoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaActivo.objects.all()
    serializer_class = CategoriaActivoSerializer


class DepresiacionViewSet(viewsets.ModelViewSet):
    queryset = Depresiacion.objects.all()
    serializer_class = DepresiacionSerializer


class ActivosSerializer(viewsets.ModelViewSet):
    queryset = Activos.objects.all()
    serializer_class = ActivosSerializer


class ActivosTemplate(TemplateView):
    template_name = 'Activos.html'


# Clase busqueda y creacion basica
class ActivosView(DetailView):
    queryset = Activos.objects.all()

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    # Devuelve la estructura de los activos
    def json_to_JsonResponse(self):
        data = list()
        for activo in self.object_list:
            data.append({
                'id': activo.id,
                'descripcion': activo.descripcion,
                'categoriaId': activo.categoria.id,
                'categoria': activo.categoria.descripcion,
                'fechaAdq': activo.fechaAdq,
                'fechaDep': activo.fechaDep,
                'agnosVu': activo.agnosVu,
                'costo': activo.costo,
                'porcentaje': activo.porcentaje,
                'suplidorId': activo.suplidor.id,
                'suplidor': activo.suplidor.nombre,
                'factura': activo.factura,
                'localidadId': activo.localidad.id,
                'depresiacion': [{
                                     'id': depr.id,
                                     'activoId': depr.activoId,
                                     'fecha': depr.fecha,
                                     'dMensual': depr.dMensual,
                                     'dAcumulada': depr.dAcumulada,
                                     'dAgno': depr.dAgno,
                                     'vLibro': depr.vLibro,
                                     'cuentas': [{
                                                     'fecha': dCuenta.fecha,
                                                     'cuentaId': dCuenta.cuenta.codigo,
                                                     'cuenta': dCuenta.cuenta.descripcion,
                                                     'referencia': dCuenta.referencia,
                                                     'auxiliarId': dCuenta.auxiliar.codigo,
                                                     'auxiliar': dCuenta.auxiliar.descripcion,
                                                     'estatus': dCuenta.estatus,
                                                     'debito': dCuenta.debito,
                                                     'credito': dCuenta.credito
                                                 }
                                                 for dCuenta in
                                                 DiarioGeneral.objects.filter(referencia='DPR-' + str(depr.id))],
                                 }
                                 for depr in Depresiacion.objects.filter(activoId=activo.id)],
                'cuentas': [{
                                'fecha': Cuenta.fecha,
                                'cuentaId': Cuenta.cuenta.codigo,
                                'cuenta': Cuenta.cuenta.descripcion,
                                'referencia': Cuenta.referencia,
                                'auxiliarId': Cuenta.auxiliar.codigo,
                                'auxiliar': Cuenta.auxiliar.descripcion,
                                'estatus': Cuenta.estatus,
                                'debito': Cuenta.debito,
                                'credito': Cuenta.credito
                            }
                            for Cuenta in DiarioGeneral.objects.filter(referencia='ACT-' + str(activo.id))]
            })
            return JsonResponse(data, safe=False)


        # Metodo pos que registra el activo en cuestion.

    def post(self, request, *args, **kwargs):
        DataA = json.loads(request.body)
        Data = DataA['regActivo']

        categoria = CategoriaActivo.objects.get(Data['categoria'])
        suplidor = Suplidor.objects.get(Data['suplidor'])
        localidad = Localidad.objects.get(Data['localidad'])

        regActivo = Activos()
        regActivo.descripcion = Data['descripcion']
        regActivo.categoria = categoria
        regActivo.fechaAdd = Data['fechaA']
        regActivo.fechaDep = Data['fechaD']
        regActivo.agnosVu = Data['agnoVu']
        regActivo.costo = Data['costo']
        regActivo.porcentaje = Data['porc']
        regActivo.suplidor = suplidor
        regActivo.factura = Data['factura']
        regActivo.localidad = localidad
        regActivo.save()

        despMensual = (Data['costo'] / 12) * (Data['porc'] / 100)
        regDepresiacion = Depresiacion()
        regDepresiacion.activoId = regActivo.id
        regDepresiacion.fecha = date.today()
        regDepresiacion.dMensual = despMensual
        regDepresiacion.dAcumulada = 0
        regDepresiacion.dAgno = 0
        regDepresiacion.vLibro = 0
        regDepresiacion.save()


# Clase para correr la depresiacion mensual de los activos aun depreciables
class DepresiacionView(TemplateView):
    template_name = 'Depresiacion.html'

    def post(self, request, *args, **kwargs):
        Data = json.loads(request.body)
        Dcuentas = Data['cuentas']
        fechaF = request.GET.get('fechaF')

        activos = Activos.objets.filter(estatus='A')

        for act in activos:
            antDesp = Depresiacion.objects.raw('select * '
                                               'from activofijo_depresiacion '
                                               'where activoId=' + act.id + 'order by fecha desc'
                                                                            'limit 1')

            regDesp = Depresiacion()
            regDesp.activoId = act.id
            regDesp.fecha = fechaF
            regDesp.dMensual = antDesp.dMensual
            regDesp.dAcumulada = antDesp.dAcumulada
            if antDesp.fecha.month == 12:
                regDesp.dAgno = antDesp.dMensual
            else:
                regDesp.dAgno = antDesp.dAgno + antDesp.dMensual
            regDesp.vLibro = antDesp.vLibro + antDesp.dMensual
            regDesp.save()

            for cta in Dcuentas:
                diario = DiarioGeneral()
                diario.fecha = fechaF
                diario.referencia = 'DEP-' + regDesp.id
                if cta['cuenta'] is not None:
                    cuenta = cuenta.objects.get(codigo=cta['cuenta'])
                    diario.cuenta = cuenta
                if cta['aux'] is not None:
                    aux = Auxiliares.objets.get(codigo=cta['aux'])
                    diario.auxiliar = aux
                diario.estatus = 'P'
                diario.debito = cta['debito']
                diario.credito = cta['credito']
                diario.save()

            contDep = Depresiacion.objects.raw('select count(*) '
                                               'from activofijo_depresiacion '
                                               'where activoId=' + act.id)
            vidaUtil = act.agnosVu * 12

            if vidaUtil == contDep:
                act.estatus = 'D'
                act.save()

        return HttpResponse('1')
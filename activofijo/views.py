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
from administracion.models import Suplidor, Localidad, DocumentoCuentas, TipoDocumento


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


class impActivoView(TemplateView):
    template_name = 'impActivos.html'

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()
        for loc in Localidad.objects.all():
            data.append({
                'id': loc.id,
                'descripcion' : loc.descripcion,
                'descripcionLarga' : loc.descripcionLarga
                })
        return JsonResponse(data, safe=False)

# Clase busqueda y creacion basica
class ActivosView(TemplateView):
    template_name = 'Activos.html'

    def setCuentaActivo(self, idActivo, fecha , cta, monto, ref):
        try:
            diario = DiarioGeneral()
            diario.fecha = fecha
            diario.referencia = ref + str(idActivo)
            cuenta = Cuentas.objects.get(codigo=cta.cuenta.codigo)
            diario.cuenta = cuenta
            diario.estatus = 'P'

            if cta.accion == 'D':
                diario.debito = monto
                diario.credito = 0
            else:
                diario.debito = 0
                diario.credito = monto

            diario.save()

            regActivo = Activos.objects.get(id=idActivo)
            regActivo.cuentas.add(diario)
            return diario.id
        except Exception, e:
            return e.message    

    def setCuentaDepresiacion(self, idDepr, fecha , cta, monto, ref):
        try:
            diario = DiarioGeneral()
            diario.fecha = fecha
            diario.referencia = ref + str(idDepr)
            cuenta = Cuentas.objects.get(codigo=cta.cuenta.codigo)
            diario.cuenta = cuenta
            diario.estatus = 'P'
            
            if cta.accion == 'D':
                diario.debito = monto
                diario.credito = 0
            else:
                diario.debito = 0
                diario.credito = monto

            diario.save()

            regDesp = Depresiacion.objects.get(id=idDepr)
            regDesp.cuentas.add(diario)
            return diario.id
        except Exception, e:
            return e.message    

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    # Devuelve la estructura de los activos
    def json_to_response(self):
        data = list()
        for activo in Activos.objects.all():
            data.append({
                'id': activo.id,
                'descripcion': activo.descripcion,
                'categoriaId': activo.categoria.id,
                'categoria': activo.categoria.descripcion,
                'fechaAdq': activo.fechaAdd,
                'fechaDep': activo.fechaDep,
                'agnosVu': activo.agnosVu,
                'costo': activo.costo,
                'porcentaje': activo.porcentaje,
                'suplidorId': activo.suplidor.id,
                'suplidor': activo.suplidor.nombre,
                'factura': activo.factura,
                'localidad' : activo.localidad.descripcion,
                'localidadId': activo.localidad.id,
                'estatus' : activo.estatus,
                'depresiacion': [{
                                     'id': depr.id,
                                     'activoId': depr.activoId,
                                     'fecha': depr.fecha,
                                     'dMensual': depr.dMensual,
                                     'dAcumulada': depr.dAcumulada,
                                     'dAgno': depr.dAgno,
                                     'vLibro': depr.vLibro,
                                 }
                                 for depr in Depresiacion.objects.filter(activoId=activo.id)]
            })
        
        return JsonResponse(data, safe=False)


        # Metodo pos que registra el activo en cuestion.

    def post(self, request, *args, **kwargs):
        DataA = json.loads(request.body)
        Data = DataA['activo']
        try:
            categoria = CategoriaActivo.objects.get(id=Data['categoria'])
            suplidor = Suplidor.objects.get(id=Data['suplidor'])
            localidad = Localidad.objects.get(id=Data['localidad'])

            regActivo = Activos()
            regActivo.descripcion = Data['descripcion']
            regActivo.categoria = categoria
            regActivo.fechaAdd = Data['fechaAdq']
            regActivo.fechaDep = Data['fechaDep']
            regActivo.agnosVu = Data['agnosVu']
            regActivo.costo = Data['costo']
            regActivo.porcentaje = Data['porc']
            regActivo.suplidor = suplidor
            regActivo.factura = Data['factura']
            regActivo.localidad = localidad
            regActivo.estatus = 'A'
            regActivo.save()

            if categoria.id == 1:
                tdoc = 'ACTT'
            elif categoria.id == 2:
                tdoc = 'ACTE'
            elif categoria.id == 3:
                tdoc = 'ACTR'
            else:
                tdoc = 'ACTE'

            tipo = TipoDocumento.objects.get(codigo=tdoc)
            doc = DocumentoCuentas.objects.filter(documento = tipo)

            for docu in doc:
                self.setCuentaActivo(regActivo.id, Data['fechaAdq'] , docu, Data['costo'],tdoc)

            despMensual = (decimal.Decimal(Data['costo']) / 12) * (decimal.Decimal(Data['porc'] )/ 100)
            regDepresiacion = Depresiacion()
            regDepresiacion.activoId = regActivo.id
            regDepresiacion.fecha = date.today()
            regDepresiacion.dMensual = despMensual
            regDepresiacion.dAcumulada = 0
            regDepresiacion.dAgno = 0
            regDepresiacion.vLibro = Data['costo']
            regDepresiacion.save()
            regActivo.depresiacion.add(regDepresiacion)

            if categoria.id == 1:
                ddoc = 'DEPT'
            elif categoria.id == 2:
                ddoc = 'DEPE'
            elif categoria.id == 3:
                ddoc = 'DEPR'
            else:
                ddoc = 'DEPE'

            tipoDo = TipoDocumento.objects.get(codigo=ddoc)
            docDep = DocumentoCuentas.objects.filter(documento = tipo)

            for document in docDep:
                self.setCuentaDepresiacion(regDepresiacion.id, Data['fechaAdq'], document, despMensual, ddoc)


            return HttpResponse(tdoc)
        except Exception, e:
            return HttpResponse(e)


class LocActivoView(DetailView):
    queryset = Localidad.objects.all()

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format =="json":
            return self.json_to_response()
        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        for locate in Localidad.objects.all():
            data.append({
                'id': locate.id,
                'descripcion': locate.descripcion,
                'Ldescripcion': locate.descripcionLarga
                })

        return JsonResponse(data,safe=False)

#clase para facilitar la categoria de los activos
class CategoriaActivoView(DetailView):
    queryset = CategoriaActivo.objects.all()

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()
        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        for cat in CategoriaActivo.objects.all():
            data.append({
                'id': cat.id,
                'descripcion' : cat.descripcion
                })

        return JsonResponse(data, safe=False)

# Clase para correr la depresiacion mensual de los activos aun depreciables
class DepresiacionView(TemplateView):
    template_name = 'Depresiacion.html'

    def depDocument(self, idActivo, fecha, monto):
        activo = Activos.objects.get(id=idActivo)

        if activo.categoria.id == 1:
            ddoc = 'DEPT'
        elif activo.categoria.id == 2:
            ddoc = 'DEPE'
        elif activo.categoria.id == 3:
            ddoc = 'DEPR'
        else:
            ddoc = 'DEPE'

        activo.descripcion = 'no'
        activo.save()

        tipoDo = TipoDocumento.objects.get(codigo=ddoc)
        docDep = DocumentoCuentas.objects.filter(documento = tipoDo)

        for doc in docDep:
            self.setCuenta(idActivo, fecha, doc, monto, activo.categoria.id)

        return activo.id

    def setCuenta(self, idActivo, fecha , cta, monto, ref):
        diario = DiarioGeneral()
        diario.fecha = fecha
        diario.referencia = ref +'-'+ str(idActivo)
        cuenta = Cuentas.objects.get(codigo=cta['cuenta'])
        diario.cuenta = cuenta
        diario.estatus = 'P'
        if cta['accion'] == 'D':
            diario.debito = monto
            diario.credito = 0
        else:
            diario.debito = 0
            diario.credito = monto
        diario.save()

        regDesp = Depresiacion.objects.get(id=idActivo)
        regDesp.cuentas.add(diario)
        return diario.id

    def post(self, request, *args, **kwargs):
        Data = json.loads(request.body)
        fechas =   Data['fechas']

        
        activos = Activos.objects.filter(estatus='A')
    
        for act in activos:
            antDesp = Depresiacion.objects.filter(activoId=act.id).order_by('-fecha').first() 
            regDesp = Depresiacion()
            regDesp.activoId = act.id
            regDesp.fecha = fechas['fechaF']
            regDesp.dMensual = antDesp.dMensual
            regDesp.dAcumulada = antDesp.dAcumulada + antDesp.dMensual
            if antDesp.fecha.month == 12:
                regDesp.dAgno = antDesp.dMensual
            else:
                regDesp.dAgno = antDesp.dAgno + antDesp.dMensual
            regDesp.vLibro = antDesp.vLibro - antDesp.dMensual
            regDesp.save()

            self.depDocument(regDesp.id,fechas['fechaF'] , antDesp.dMensual)

            if regDesp.vLibro == 0:
                act.estatus = 'D'
                act.save()

        return HttpResponse('ok')


class HistoricoActivos(TemplateView):
    template_name = 'historicoActivo.html'

    def get(self, request, *args, **kwargs):
        format =self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()
        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()
        for activo in Activos.objects.all():
            depr = Depresiacion.objects.filter(activoId=activo.id).order_by('-fecha').first() 
            data.append({
                'id': activo.id,
                'descripcion': activo.descripcion,
                'fechaAdq': activo.fechaAdd,
                'costo' : activo.costo,
                'porcentaje': activo.porcentaje, 
                'fecha': depr.fecha if depr != None else '',
                'dMensual': depr.dMensual if depr != None else '',
                'dAcumulada': depr.dAcumulada if depr != None else '',
                'dAgno': depr.dAgno if depr != None else '',
                'vLibro': depr.vLibro if depr != None else ''
                })

        return JsonResponse(data, safe=False)

class ActDepresiados(TemplateView):
    template_name = "ActDepresiados.html"

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == 'json':
            return self.json_to_response()
        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()
        for activo in Activos.objects.filter(estatus='D'):
            depr = Depresiacion.objects.filter(activoId=activo.id).order_by('-fecha').first() 
            data.append({
                'id': activo.id,
                'descripcion': activo.descripcion,
                'fechaAdq': activo.fechaAdd,
                'costo' : activo.costo,
                'porcentaje': activo.porcentaje, 
                'fecha': depr.fecha if depr != None else '',
                'dMensual': depr.dMensual if depr != None else '',
                'dAcumulada': depr.dAcumulada if depr != None else '',
                'dAgno': depr.dAgno if depr != None else '',
                'vLibro': depr.vLibro if depr != None else ''
                })

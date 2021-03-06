import json
import decimal

from datetime import date
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets
from django.shortcuts import render

from cuenta.models import DiarioGeneral, Cuentas
from administracion.models import Socio, CoBeneficiario, Suplidor, TipoDocumento, DocumentoCuentas
from cxp.models import OrdenGeneral, cxpSuperGeneral
from prestamos.viewMaestraPrestamos import getCuentasByPrestamo
from reciboingreso.models import ReciboIngresoNomina


# Local Imports
from .models import SolicitudCheque, ConcCheques, NotaDCConciliacion, NumCheque, ConDeposito, ConPeriodo, ConBanco
from .serializers import solicitudSerializer, chequesSerializer, NotasSerializer, ConBancoSerializer


class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = SolicitudCheque.objects.all()
    serializer_class = solicitudSerializer


class ChequesConsViewSet(viewsets.ModelViewSet):
    queryset = ConcCheques.objects.all()
    serializer_class = chequesSerializer


class NotasConsViewSet(viewsets.ModelViewSet):
    queryset = NotaDCConciliacion.objects.all()
    serializer_class = NotasSerializer


class conBancoViewSet(viewsets.ModelViewSet):
    queryset = ConBanco.objects.all()
    serializer_class = ConBancoSerializer


def prestSolicitud(self, fecha, socio, suplidor, concepto, monto, prestamo):
    try:

        solicitud = SolicitudCheque()
        solicitud.fecha = fecha
        if socio != None:
            soc = Socio.objects.get(codigo=socio)
            solicitud.socio = soc
        if suplidor is not None:
            sup = Suplidor.objects.get(id=suplidor)
            solicitud.suplidor = sup
        solicitud.concepto = concepto
        solicitud.monto = monto
        solicitud.prestamo = prestamo
        solicitud.estatus = 'P'
        solicitud.save()

        return 'Ok'
    except Exception, e:
        return e.message


def ordenSolicitud(self, fecha, suplidor, concepto, monto, orden):
    try:
        regOrden = OrdenGeneral.objects.get(id = orden)

        solicitud = SolicitudCheque()
        solicitud.fecha = fecha
        sup = Suplidor.objects.get(id=suplidor)
        solicitud.suplidor = sup
        solicitud.concepto = concepto
        solicitud.monto = monto
        solicitud.cxpOrden = orden
        solicitud.estatus = 'P'
        solicitud.save()

        for oxd in regOrden.cuentas.all():
            solicitud.cuenta.add(oxd)

        regOrden.chk = 'D'
        regOrden.save()

        return 'Ok'
    except Exception, e:
        return e.message


def superSolicitud(self, fecha, suplidor, concepto, monto, Ssup):
    try:
        regSuper = cxpSuperGeneral.objects.get(id = Ssup)

        solicitud = SolicitudCheque()
        solicitud.fecha = fecha
        sup = Suplidor.objects.get(id=suplidor)
        solicitud.suplidor = sup
        solicitud.concepto = concepto
        solicitud.monto = monto
        solicitud.superOrden = Ssup
        solicitud.estatus = 'P'
        solicitud.save()

        for sup in regSuper.cuentas.all():
            solicitud.cuentas.add(sup)

        regSuper.chk = 'D'
        regSuper.save()

        return 'Ok'
    except Exception, e:
        return e.message


class SolicitudView(TemplateView):
    template_name = 'solicitudCheque.html'

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()
        solicitud = SolicitudCheque.objects.all()

        for sol in solicitud:
            data.append({
                'id': sol.id,
                'fecha': sol.fecha,
                'socioId': sol.socio.codigo if sol.socio != None else '',
                'socio': sol.socio.nombreCompleto if sol.socio != None else '',
                'suplidorId': sol.suplidor.id if sol.suplidor != None else '',
                'suplidor': sol.suplidor.nombre if sol.suplidor != None else '',
                'prestamo': sol.prestamo,
                'cxpOrden': sol.cxpOrden,
                'superOrden': sol.superOrden,
                'concepto': sol.concepto,
                'monto': sol.monto,
                'estatus': sol.estatus,
               
             }
            )

        return JsonResponse(data, safe=False)

    def post(self, request):
        DataT = json.loads(request.body)
        Data = DataT['solicitud']

        if Data['id'] is None:
            solicitud = SolicitudCheque()
            solicitud.fecha = Data['fecha']

            if Data['socioId'] != None:
                socio = Socio.objects.get(codigo=Data['socioId'])
                solicitud.socio = socio
            if Data['suplidorId'] != None:
                suplidor = Suplidor.objects.get(id=Data['suplidorId'])
                solicitud.suplidor = suplidor

            solicitud.concepto = Data['concepto']
            solicitud.prestamo = 0
            solicitud.monto = Data['monto']
            solicitud.estatus = Data['estatus']
            solicitud.save()
        else:
            
            solicitud = SolicitudCheque.objects.get(id=Data['id'])
            solicitud.concepto = Data['concepto']
            solicitud.monto = Data['monto']
            # solicitud.estatus = Data['estatus']
            solicitud.save()

        return HttpResponse('Ok')


class SSolicitud(TemplateView):
    template_name = 'impSolicitud.html'

    def post(self, request):
        dataT = json.loads(request.body)
        data = dataT['solicitud']
        try:
            sol = SolicitudCheque.objects.get(id=data['solId'])
            sol.estatus = data['estatus']
            sol.save()

            return HttpResponse('Ok')
        except Exception, e:
            return HttpResponse(e.message)


class ChequesView(TemplateView):
    template_name = 'ConciliacionCheque.html'

    def regCuentasChk(self, chkId, diario):

        cheque = ConcCheques.objects.get(id=chkId)

        regDiario = DiarioGeneral.objects.get(id=diario)
    
        cheque.cuentas.add(regDiario)
        return 'Ok'

    def setCuentaMaestra(self, chk, cuenta, doc , fecha, debito, credito):
        cheque = ConcCheques.objects.get(id=chk)
        cuenta = Cuentas.objects.get(codigo=cuenta)

        diario = DiarioGeneral()
        diario.fecha = fecha
        diario.referencia = str(doc)+'-'+ str(chk)
        diario.cuenta = cuenta
        diario.estatus = 'P'        
        diario.debito = debito
        diario.credito = credito

        diario.save()


        cheque.cuentas.add(diario)
        return diario.id

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        cheque = ConcCheques.objects.all()

        for chk in cheque:

            data.append({
                'id': chk.id,
                'solicitud': chk.solicitud.id,
                'beneficiario': chk.beneficiario if chk.beneficiario != None else chk.solicitud.socio.nombreCompleto if chk.solicitud.socio != None else chk.solicitud.suplidor.nombre,
                'concepto': chk.concepto if chk.concepto != None else chk.solicitud.concepto,
                'monto': chk.monto if chk.monto !=None else chk.solicitud.monto,
                'noCheque': chk.chequeNo,
                'fecha': chk.fecha,
                'estatus': chk.estatus,
                'cuenta':[{
                    'id': cta.id,
                    'codigoCta': cta.cuenta.codigo,
                    'cuenta': cta.cuenta.descripcion,
                    'debito': cta.debito,
                    'credito': cta.credito
                    }
                   for cta in chk.solicitud.cuentas.all()],
                'cuentasChk':[{
                    'id': cta.id,
                    'codigoCta': cta.cuenta.codigo,
                    'cuenta': cta.cuenta.descripcion,
                    'debito': cta.debito,
                    'credito': cta.credito
                    }
                   for cta in chk.cuentas.all()
                ]
            })
        return JsonResponse(data, safe=False)

    def post(self, request):
        DataT = json.loads(request.body)
        Data = DataT['cheque']
        cheque = ConcCheques()

        try:
            if Data['id'] is None:
                
                if Data['solicitud'] is not None:
                    solicitud = SolicitudCheque.objects.get(id=Data['solicitud'])
                    
                    cuentas = list()

                    if solicitud.cxpOrden != None:
                        orden = OrdenGeneral.objects.get(id = solicitud.cxpOrden) 
                        for orCuentas in orden.cuentas.all():
                            cuentas.append(orCuentas.id)
                    elif solicitud.superOrden != None:
                        cxSuper = cxpSuperGeneral.objects.get(id = solicitud.superOrden)
                        for spCuentas in cxSuper.cuentas.all():
                            cuentas.append(spCuentas.id)
                    elif solicitud.prestamo != None:
                        regCuentas = getCuentasByPrestamo(solicitud.prestamo)
                        
                    else:
                        raise Exception("Documento Origen no esta Posteado")
                else:
                    solicitud = None
                    cheque.monto = Data['monto']
                    cheque.concepto = Data['concepto']
                    cheque.beneficiario = Data['beneficiario']
                    regCuenta = Data['cuenta']


                
                cheque.solicitud = solicitud
                cheque.chequeNo = Data['noCheque']
                cheque.fecha = Data['fecha']
                cheque.estatus = 'R'
                cheque.save()

                if Data['solicitud'] is None:
                    tipo = TipoDocumento.objects.get(codigo='CHKR')
                    doc = DocumentoCuentas.objects.filter(documento = tipo)

                    for cta in regcuenta:
                        self.setCuentaMaestra(cheque.id, cta.cuenta , 'CHKR', Data['fecha'], cta.debito, cta.credito) 
                else:
                    for cta in cuentas:
                        self.regCuentasChk(cheque.id, cta)
                    
                    
                    solicitud.estatus = 'E'
                    solicitud.save()

                noChk = NumCheque.objects.get(id=1)
                noChk.chequeNo = noChk.chequeNo + 1
                noChk.save()
               
            else:
                cheque = ConcCheques.objects.get(id=Data['id'])
                cheque.estatus = Data['estatus']
                cheque.save()

            return HttpResponse('Ok')
        except Exception, e:
            return HttpResponse(e.message)


class SChequeView(TemplateView):
    template_name = "impCheque.html"

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        noChk = NumCheque.objects.get(id=1)

        data.append({
            'id': noChk.id,
            'noCheque': noChk.chequeNo
                })
        return JsonResponse(data, safe=False)


class NotasConciliacionView(TemplateView):
    template_name = 'NotasConciliacion.html'

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        data = list()

        notaConc = NotaDCConciliacion.objects.all()

        for nota in notaConc:
            data.append({
                'id': nota.id,
                'concepto': nota.concepto,
                'fecha': nota.fecha,
                'tipo': nota.tipo,
                'monto': nota.monto,
                'estatus': nota.estatus,
                'cuenta': [{
                               'fecha': ctas.fecha,
                               'cuentaId': ctas.cuenta.codigo,
                               'cuenta': ctas.cuenta.descripcion,
                               'referencia': ctas.referencia,
                               'auxiliarId': ctas.auxiliar.codigo,
                               'auxiliar': ctas.auxiliar.descripcion,
                               'estatus': ctas.estatus,
                               'debito': ctas.debito,
                               'credito': ctas.credito

                           }
                           for ctas in DiarioGeneral.objects.filter(referencia='NCCD-' + str(nota.id))]
            })
        return JsonResponse(data, safe=False)

    def post(self, request):
        DataT = json.loads(request.body)

        Data = DataT['Notas']
        try:
            if Data['id'] is None:
                nota = NotaDCConciliacion()
                nota.fecha = Data['fecha']
                nota.concepto = Data['concepto']
                nota.monto = decimal.Decimal(Data['monto'])
                nota.tipo = Data['tipo']
                nota.estatus = Data['estatus']
                nota.save()
            else:
                nota = NotaDCConciliacion.objects.get(id=1)
                nota.concepto = Data['concepto']
                nota.estatus = Data['estatus']
                nota.save()

            return HttpResponse('Ok')
        except Exception, e:
            return HttpResponse(e.message)


class DepositosView(TemplateView):
    template_name="conDeposito.html"

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        Data = list()

        depositos = ConDeposito.objects.all()

        for banc in depositos:
            Data.append({
                'id': banc.pk,
                'fecha': banc.fecha,
                'descripcion': banc.descripcion,
                'monto': banc.monto,
                'estatus': banc.estatus
            })

        return JsonResponse(Data, safe=False)

    def post(self, request):
        DataT = json.loads(request.body)
        Data = DataT['deposito']

        if Data['id'] is None:
            depositoReg = ConDeposito()
            depositoReg.fecha = Data['fecha']
            depositoReg.descripcion = Data['descripcion']
            depositoReg.monto = Data['monto']
            depositoReg.estatus = Data['estatus']
            depositoReg.save()
        else:
            depositoReg = ConDeposito.objects.get(id=Data['id'])
            depositoReg.fecha = Data['fecha']
            depositoReg.descripcion = Data['descripcion']
            depositoReg.estatus = Data['estatus']
            depositoReg.monto = Data['monto']
            depositoReg.save(())
        return HttpResponse('Ok')


# class ChkTransito(TemplateView):
#     template_name="conChkTransito.html"

#     def get(self, request, *args, **kwargs):
#         format = self.request.GET.get('format')

#         if format == "json":
#             return self.json_to_response()

#         context = self.get_context_data()
#         return self.render_to_response(context)

#     def json_to_response(self):
#         Data = list()

#         chktransito = conChequeTrans.objects.all()

#         for banc in chktransito:
#             Data.append({
#                 'id': banc.pk,
#                 'fecha': banc.fecha,
#                 'descripcion': banc.descripcion,
#                 'monto': banc.monto,
#                 'estatus': banc.estatus
#             })

#         return JsonResponse(Data, safe=False)

#     def post(self, request):
#         DataT = json.loads(request.body)
#         Data = DataT['ChkTransito']

#         if Data['id'] is None:
#             ChktransReg = conChequeTrans()
#             ChktransReg.fecha = Data['fecha']
#             ChktransReg.descripcion = Data['descripcion']
#             ChktransReg.monto = Data['monto']
#             ChktransReg.estatus = Data['estatus']
#             ChktransReg.save()
#         else:
#             ChktransReg = conChequeTrans.objects.get(id=Data['id'])
#             ChktransReg.fecha = Data['fecha']
#             ChktransReg.descripcion = Data['descripcion']
#             ChktransReg.estatus = Data['estatus']
#             ChktransReg.monto = Data['monto']
#             ChktransReg.save(())
#         return HttpResponse('Ok')


class SSNotasView(DetailView):
    queryset = NotaDCConciliacion.objects.all()

    def get(self, request, *args, **kwargs):
        fechaI = request.GET.get('fechaI')
        fechaF = request.GET.get('fechaF')

        return self.json_to_response(fechaI, fechaF)

    def json_to_response(self, fechaI, fechaF):
        Data = list()

        registros = ConBanco.objects.raw('select id, concepto, '
                                         'fecha, tipo, '
                                         'monto, estatus '
                                         'from conciliacion_notadcconciliacion'
                                         'WHERE fecha BETWEEN ' + fechaI + ' AND ' + fechaF)

        for detalle in registros:
            Data.append({
                'id': detalle.id,
                'fecha': detalle.fecha,
                'concepto': detalle.concepto,
                'tipo': detalle.tipo,
                'monto': detalle.monto,
                'estatus': detalle.estatus,
            })

        return JsonResponse(Data, safe=False)

    def post(self, request):
        DataT = json.loads(request.body)
        Data = DataT['cuenta']

        regCuenta = Cuentas.objects.get(codigo=Data['cuenta'])
        regNota = NotaDCConciliacion.objects.get(id=Data['nota'])

        regDiario = DiarioGeneral()
        regDiario.cuenta = regCuenta
        regDiario.fecha = Data[fecha]
        regDiario.referencia = Data['ref']
        regDiario.estatus = 'P'
        regDiario.debito = data['debito']
        regDiario.credito = data['credito']
        regDiario.save()

        regNota.cuentas.add(regDiario)


class ConBancoView(TemplateView):
    template_name = "ConBanco.html"

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')

        if format == "json":
            return self.json_to_response()

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self):
        Data = list()

        bancaria = ConBanco.objects.all()

        for banc in bancaria:
            Data.append({
                'id': banc.pk,
                'fecha': banc.fecha,
                'descripcion': banc.descripcion,
                'monto': banc.monto,
                'estatus': banc.estatus
            })

        return JsonResponse(Data, safe=False)

    def post(self, request):
        DataT = json.loads(request.body)
        Data = DataT['banco']

        if Data['id'] is None:
            banco = ConBanco()
            banco.fecha = Data['fecha']
            banco.descripcion = Data['descripcion']
            banco.monto = Data['monto']
            banco.estatus = Data['estatus']
            banco.save()
        else:
            banco = ConBanco.objects.get(id=Data['id'])
            banco.fecha = Data['fecha']
            banco.descripcion = Data['descripcion']
            banco.estatus = Data['estatus']
            banco.monto = Data['monto']
            banco.save(())
        return HttpResponse('Ok')


class ConBancoLs(DetailView):
    queryset = ConBanco.objects.all()

    def get(self, request, *args, **kwargs):
        fechaI = request.GET.get('fechaI')
        fechaF = request.GET.get('fechaF')

        return self.json_to_response(fechaI, fechaF)

    def json_to_response(self, fechaI, fechaF):
        Data = list()
        
        registros = ConBanco.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF)

        for detalle in registros:
            Data.append({
                'id': detalle.id,
                'fecha': detalle.fecha,
                'descripcion': detalle.descripcion,
                'monto': detalle.monto,
                'estatus': detalle.estatus,
            })

        return JsonResponse(Data, safe=False)


class DepositoLs(DetailView):
    queryset = ConDeposito.objects.all()

    def get(self, request, *args, **kwargs):
        fechaI = request.GET.get('fechaI')
        fechaF = request.GET.get('fechaF')

        return self.json_to_response(fechaI, fechaF)


    def json_to_response(self, fechaI, fechaF):
        Data = list()

        registros = conDeposito.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF)

        for detalle in registros:
            Data.append({
                'id': detalle.id,
                'fecha': detalle.fecha,
                'descripcion': detalle.descripcion,
                'monto': detalle.monto,
                'estatus': detalle.estatus,
            })

        return JsonResponse(Data, safe=False)


# class ChkTransitoLs(DetailView):
#     queryset = conChequeTrans.objects.all()

#     def get(self, request, *args, **kwargs):
#         fechaI = request.GET.get('fechaI')
#         fechaF = request.GET.get('fechaF')

#         return self.json_to_response(fechaI, fechaF)

#     def json_to_response(self, fechaI, fechaF):
#         Data = list()

#         registros = conChequeTrans.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF)

#         for detalle in registros:
#             Data.append({
#                 'id': detalle.id,
#                 'fecha': detalle.fecha,
#                 'descripcion': detalle.descripcion,
#                 'monto': detalle.monto,
#                 'estatus': detalle.estatus,
#             })

#         return JsonResponse(Data, safe=False)


class regGenerico(TemplateView):
    template_name = "ReporteGenerico.html"

class RepConciliacion(TemplateView):
    template_name = "repConciliacion.html"

    def get(self, request, *args, **kwargs):
        format = self.request.GET.get('format')
        fechaI = request.GET.get('fechaI')
        fechaF = request.GET.get('fechaF')

        if format == "json":
            return self.json_to_response(fechaI, fechaF)

        context = self.get_context_data()
        return self.render_to_response(context)

    def json_to_response(self, fechaI, fechaF):
        data = list()

        RegBanco = ConBanco.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF)
        RegDepsR = ConDeposito.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF, estatus= 'R')
        RegDepsT = ConDeposito.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF, estatus= 'T')

        RegChkP = ConcCheques.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF)
        RegChkT = ConcCheques.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF, estatus= 'T')
        RegChkC = ConcCheques.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF, estatus= 'C')
        RegChkD = ConcCheques.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF, estatus= 'D')

        RegNotaC = NotaDCConciliacion.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF, tipo= 'C')
        RegNotaD = NotaDCConciliacion.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF, tipo= 'D')

        RegNotaCT = NotaDCConciliacion.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF, tipo= 'C', estatus='T')
        RegNotaDT = NotaDCConciliacion.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF, tipo= 'D', estatus='T')

        RegConPiodo = ConPeriodo.objects.get(fechaInicio = fechaI, fechaFin = fechaF)
        RegReciboNom =ReciboIngresoNomina.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF, estatus= 'P')

        RegDiario = DiarioGeneral.objects.filter(fecha__gte = fechaI, fecha__lte = fechaF)

        


        BancoMonto = decimal.Decimal(0)
        montoCuentaBanco = decimal.Decimal(0)
        MontosChkEmitido = decimal.Decimal(0)
        MontosChkDevuelto = decimal.Decimal(0)
        MontosChkTrans = decimal.Decimal(0)
        montoDepRec = decimal.Decimal(0)
        montoReciboR = decimal.Decimal(0)
        BancoMonto = decimal.Decimal(0)
        montoCredito = decimal.Decimal(0)
        montoDebito = decimal.Decimal(0)
        montoCreditoTrans = decimal.Decimal(0)
        montoDebitoTrans = decimal.Decimal(0)
        montoDepTr = decimal.Decimal(0)
        bancoDesc = None

        #Cheques registrados
        for chkE in RegChkP:
            if chkE.solicitud != None:
                MontosChkEmitido += chkE.solicitud.monto
            else:
                MontosChkEmitido += chkE.monto

        #Cheques Devueltos
        for chkD in RegChkD:
            if chkD.solicitud != None:
                MontosChkDevuelto += chkD.solicitud.monto
            else:
                MontosChkDevuelto += chkD.monto

        #Cheques en Transito
        for chkT in RegChkT:
            if chkT.solicitud != None:
                MontosChkTrans+= chkT.solicitud.monto
            else:
                MontosChkTrans += chkT.monto
        
        #Cuenta de banco popular
        for cuenta in RegDiario:
            if cuenta.cuenta.codigo == 11010203:
                bancoDesc = cuenta.cuenta.descripcion
                montoCuentaBanco += cuenta.credit

        #Depositos recibidos
        for depR in RegDepsR:
            montoDepRec += depR.monto

        for depT in RegDepsT:
            montoDepTr += depT.monto

        #Captura de nomina
        for nom in RegReciboNom:
            montoReciboR += nom.monto

        #Registros de banco
        for x in RegBanco:
            BancoMonto += x.monto

        #Notas de Creditos Resgitradas
        for NotaC in RegNotaC:
            montoCredito += NotaC.monto
        
        #Notas de Debitos Registradas
        for NotaD in RegNotaD:
            montoDebito += NotaD.monto

        #Notas de Credito en Transito
        for NotaCT in RegNotaCT:
            montoCreditoTrans += NotaCT.monto
        
        #Notas de Debito en Transito
        for NotaDT in RegNotaDT:
            montoDebitoTrans += NotaD.monto

        data.append({
                'descripcion': bancoDesc,
                'cuenta' : 11010203,
                'mesAnt' : RegConPiodo.monto,
                'DepRealizados' : montoDepRec,
                'Creditos' : montoCredito,
                'chkEmitidos': MontosChkEmitido,
                'chkDevueltos': MontosChkDevuelto,
                'OtrosDebitos': montoDebito,
                'Comisiones': 0,
                'Prestamos': 0,
                'Nomina': montoReciboR,
                'Otros': 0 ,
                'BalanceBanco' : BancoMonto,
                'DepTransito' : montoDepTr,
                'CredTransito' : montoCreditoTrans,
                'DebTransito' : montoDebitoTrans,
                'ChkTransito' : MontosChkTrans

            })

        return JsonResponse(data, safe=False)





        


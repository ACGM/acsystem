import json
import decimal

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, DetailView
from rest_framework import viewsets

from .models import InteresesAhorro, MaestraAhorro, AhorroSocio, RetiroAhorro
from cuenta.models import DiarioGeneral, Cuentas, Auxiliares, TipoDocumento
from administracion.models import Socio
from .serializers import interesAhorroSerializer, maestraAhorroSerializer, AhorroSocioSerializer, RetiroAhorroSerializer


class MaestraAhorroView(DetailView):
    queryset = AhorroSocio.objects.all()

    # Metodo Post para el proceso completo
    def post(self, request, *args, **kwargs):

        try:
            dataT = json.loads(request.body)
            dataAh =dataT['AhorroSocio']
            data = dataT['maestra']
            dataAr = dataT['retiro']
            ahorroId = data['ahorro']
            dataCuentas = dataT['cuentas']

            maestraId = data['id']

            # Operacion para registar un retiro de ahorro
            if len(dataAr) > 0:

                if maestraId == None:
                    maestra = MaestraAhorro()
                    listaDiario = []

                    ahorro = AhorroSocio.objects.get(id=ahorroId)

                    # Recalcula el balance y el disponible del socio
                    balanceAc = ahorro.balance
                    disponibleAc = ahorro.disponible

                    balanceAc = balanceAc - decimal.Decimal(data['monto'])
                    disponibleAc = disponibleAc - decimal.Decimal(data['monto'])

                    # Actualiza los cambios en el registro de ahorros
                    ahorro.balance = balanceAc
                    ahorro.disponible = disponibleAc
                    ahorro.save()


                    retiro = RetiroAhorro()
                    retiro.socio = Socio.objects.get(codigo=dataAh['socio'])
                    retiro.ahorro = ahorro
                    retiro.tipoRetiro = dataAr['tipoRetiro']
                    retiro.monto = dataAr['monto']
                    retiro.save()


                    # Registra en el historico de ahorros

                    maestra.ahorro = AhorroSocio.objects.get(id=dataAh['id'])
                    maestra.fecha = data['fecha']
                    maestra.retiro = retiro
                    maestra.monto = data['monto']
                    maestra.interes = InteresesAhorro.objects.get(id=data['interes'])
                    maestra.balance = ahorro.balance
                    maestra.estatus = False
                    maestra.save()

                       # Registra las cuentas afectadas en el Diario General
                    for item in dataCuentas:
                        rsDiario = DiarioGeneral()
                        if item['cuenta'] !=None:
                             rsDiario.cuenta = Cuentas.objects.get(codigo=item['cuenta'])

                        if item['auxiliar'] != None:
                            rsDiario.auxiliar = Auxiliares.objects.get(codigo=item['auxiliar'])

                        rsDiario.fecha = item['fecha']
                        rsDiario.referencia = item['referencia']
                        rsDiario.tipoDoc = TipoDocumento.objects.get(tipoDoc=item['tipoDoc'])
                        rsDiario.estatus = item['estatus']
                        rsDiario.debito = item['debito']
                        rsDiario.credito = item['credito']
                        rsDiario.save()
                        maestra.cuentas.add(rsDiario)
                        listaDiario.append(rsDiario.id)


                    # Actualiza las referencia de la Maestra
                    for item in listaDiario:
                        rsDiarios = DiarioGeneral.objects.get(id=item)
                        rsDiarios.fecha = dataCuentas[0]['fecha']
                        rsDiarios.referencia = 'AH-' + str(maestra.id)
                        rsDiarios.save()

                else:
                    regMaestra = MaestraAhorro.objects.get(id=maestraId)
                    ahorroE = AhorroSocio.objects.get(id=dataAh['id'])
                    retirosE = RetiroAhorro.objects.get(id=dataAr['id'])

                    balanceAnt = regMaestra.monto
                    balanceArE = ahorroE.balance

                    dispoArE = ahorroE.disponible + balanceAnt
                    montoArE = decimal.Decimal(data['monto'])

                    balanceArE = balanceArE + balanceAnt
                    balanceArE = balanceArE - montoArE
                    dispoArE = dispoArE - montoArE

                    for cuentaAhE in dataCuentas:
                        rsDiario = DiarioGeneral.objects.get(id=cuentaAhE['id'])

                        for itemCuenta in dataCuentas:
                            rsDiario.fecha= itemCuenta['fecha']
                            rsDiario.debito = itemCuenta['debito']
                            rsDiario.credito = itemCuenta['credito']
                            rsDiario.save()

                    regMaestra.monto = data['monto']
                    regMaestra.interes = InteresesAhorro.objects.get(id=data['interes'])
                    regMaestra.balance = balanceArE
                    regMaestra.save()

                    retirosE.monto = dataAr['monto']
                    retirosE.save()

                    ahorroE.balance = balanceArE
                    ahorroE.disponible = dispoArE
                    ahorroE.save()

            else:
                # Corre el escenario de edicion o creacion de registro de ingreso de ahorro en la Maestra
                if maestraId != None:
                    regMaestra = MaestraAhorro.objects.get(id=maestraId)
                    ahorroE = AhorroSocio.objects.get(id=dataAh['id'])

                    # Recalcula el Balance y el Disponible
                    balanceAnt = regMaestra.monto
                    balanceArE = ahorroE.balance

                    dispoArE = ahorroE.disponible
                    montoArE = data['monto']

                    # Recalcula el Balance y el Disponible en caso de ser un prestamo o un ahorro

                    balanceAnt = balanceArE + balanceAnt

                    balanceAnt = balanceAnt - montoArE
                    dispoArE = dispoArE + balanceArE
                    dispoArE = dispoArE - montoArE


                    # Edital el registro en de las cuentas o auxiliares en el Diario General
                    for cuentaAhE in regMaestra.cuentas:
                        rsDiario = DiarioGeneral.objects.get(id=cuentaAhE)

                        for itemCuenta in dataCuentas:
                            rsDiario.debito = itemCuenta['debito']
                            rsDiario.credito = itemCuenta['credito']
                            rsDiario.save()

                    # Guarda los cambios de la Maestra Ahorro
                    regMaestra.monto = data['monto']
                    regMaestra.interes = data['interes']
                    regMaestra.save()

                    # En caso de ser una edicion de un retiro Actualiza el monto de retiro.
                    # if 'RET' == 'RTE':
                    retiro = RetiroAhorro.objects.get(ahorro=data['id'])
                    retiro.monto = dataAh['monto']
                    retiro.save()

                    # Actualiza el registro de ahorro
                    ahorroE.balance = balanceAnt
                    ahorroE.disponible = dispoArE
                    ahorroE.save()

                else:
                    # Guarda un registro nuevo en la Maestra
                    regMaestra = MaestraAhorro()
                    ahorroE = AhorroSocio.objects.get(id=dataAh['id'])
                    listaDiario = []

                    balanceAnt = ahorroE.balance
                    dispoAnt = ahorroE.disponible

                    balanceAnt= balanceAnt + decimal.Decimal(data['monto'])
                    dispoAnt = dispoAnt + decimal.Decimal(data['monto'])

                    ahorroE.balance = balanceAnt
                    ahorroE.disponible = dispoAnt
                    ahorroE.save()

                    regMaestra.fecha = data['fecha']
                    regMaestra.ahorro = ahorroE
                    regMaestra.monto = data['monto']
                    regMaestra.interes = InteresesAhorro.objects.get(id=data['interes'])
                    regMaestra.balance = ahorroE.balance
                    regMaestra.estatus = data['estatus']
                    regMaestra.save()

                    # Registra las cuentas y/o auxiliares en el Diario General
                    for item in dataCuentas:
                        rsDiario= DiarioGeneral()
                        rsDiario.fecha = item['fecha']
                        rsDiario.referencia = item['referencia']
                        rsDiario.auxiliar = item['auxiliar']
                        rsDiario.tipoDoc = TipoDocumento.objects.get(tipoDoc=item['tipoDoc'])
                        rsDiario.estatus = item['estatus']
                        rsDiario.debito = item['debito']
                        rsDiario.credito = item['credito']
                        rsDiario.save()
                        listaDiario.append(rsDiario.id)
                        regMaestra.cuentas.add(rsDiario)

                    # Actualiza las referencia de la Maestra
                    for item in listaDiario:
                        rsDiario = DiarioGeneral.objects.get(id=item)
                        rsDiario.fecha = dataCuentas[0]['fecha']
                        rsDiario.referencia = 'AH-' + str(regMaestra.id)
                        rsDiario.save()


            return HttpResponse('1')

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
        if 'AR' == 'AR':
            for ahorro in self.object_list:
                data.append({
                    'id': ahorro.id,
                    'socioId': ahorro.socio.id,
                    'socio': ahorro.socio.nombres + ' ' + ahorro.socio.apellidos,
                    'balance': ahorro.balance,
                    'disponible': ahorro.disponible,
                    'maestra': [
                        {
                            'id': maestra.id,
                            'fecha': maestra.fecha,
                            'monto': maestra.monto,
                            'interes': maestra.interes.porcentaje,
                            'balance': maestra.balance,
                            'estatus': maestra.estatus,
                            'cuentas': [
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
                                for cuentas in DiarioGeneral.objects.filter(referencia=('AH-' + str(maestra.id)))]

                        }
                        for maestra in MaestraAhorro.objects.filter(ahorro=ahorro.id)]
                })
        else:
            for retiro in self.object_list:
                data.append({
                    'id': retiro.id,
                    'socio': retiro.socio.nombres + ' ' + retiro.socio.apellidos,
                    'ahorro': retiro.socio.id,
                    'tipoRetiro': retiro.tipoRetiro,
                    'monto': retiro.monto
                })

        return JsonResponse(data, safe=False)


class InteresAhorroViewSet(viewsets.ModelViewSet):
    queryset = InteresesAhorro.objects.all()
    serializer_class = interesAhorroSerializer


class MaestraAhorroViewSet(viewsets.ModelViewSet):
    queryset = MaestraAhorro.objects.all()
    serializer_class = maestraAhorroSerializer


class AhorroViewSet(viewsets.ModelViewSet):
    queryset = AhorroSocio.objects.all()
    serializer_class = AhorroSocioSerializer


class RetirosAhorroViewSet(viewsets.ModelViewSet):
    queryset = RetiroAhorro.objects.all()
    serializer_class = RetiroAhorroSerializer


class AhorroView(TemplateView):
    template_name = 'ahorro.html'




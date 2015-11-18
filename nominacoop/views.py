# VIEWS de Nomina

from django.conf import settings
from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, View, DetailView
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import NominasGeneradasSerializer, TiposNominasSerializer, NominaGeneradaDetalleSerializer

from .models import NominaCoopH, NominaCoopD, EmpleadoCoop, TipoNomina, NominaPrestamosAhorros, CuotasPrestamosEmpresa, \
    CuotasAhorrosEmpresa
from administracion.models import Socio
from prestamos.models import MaestraPrestamo

from prestamos.viewMaestraPrestamos import getBalancesPrestamos
from prestamos.views import guardarPagoCuotaPrestamo
from acgm.views import LoginRequiredMixin
from ahorro.views import insMaestra, getSocioAhorro

from datetime import datetime

import json
import decimal


# Vista Principal de Nomina
class NominaView(LoginRequiredMixin, TemplateView):
    template_name = 'nomina.html'


# Vista Descuentos Prestamos/Ahorros
class NominaDescuentosView(LoginRequiredMixin, TemplateView):
    template_name = 'nomdescuentos.html'


# Reporte Nomina Quincenal
class rptNominaQuincenal(LoginRequiredMixin, TemplateView):
    template_name = 'rpt_nomina.html'


# Reporte Nomina Descuentos por Ahorros
class rptNominaDescAhorros(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_DescAhorros.html'


# Reporte Nomina Descuentos por Prestamos
class rptNominaDescPrestamos(LoginRequiredMixin, TemplateView):

	template_name = 'rpt_DescPrestamos.html'


# Listado de Nominas Generadas
class ListadoNominasGeneradasViewSet(viewsets.ModelViewSet):
    queryset = NominaCoopH.objects.all()
    serializer_class = NominasGeneradasSerializer


# Listado de Nominas Generadas
class DetalleNominaGeneradaAPIView(APIView):
    serializer_class = NominaGeneradaDetalleSerializer

    def get(self, request, nomina=None):
        if nomina != None:
            detalleNomina = NominaCoopD.objects.filter(nomina__fechaNomina=nomina)
        else:
            detalleNomina = NominaCoopD.objects.all()

        response = self.serializer_class(detalleNomina, many=True)
        return Response(response.data)


# Listado de Tipos de Nominas
class ListadoTiposNominasViewSet(viewsets.ModelViewSet):
    queryset = TipoNomina.objects.all()
    serializer_class = TiposNominasSerializer


# *********************************************************
#														 *
# Generar nomina a partir de la fecha y tipo 			 *
#														 *
#*********************************************************
class generaNominaView(View):
    def post(self, request, *args, **kwargs):

        try:

            # Tomar los parametros enviados por el Post en JSON
            data = json.loads(request.body)

            #Paso 1: Traer todos los empleados que estaran en el proceso de nomina (activo=True)
            empleados = EmpleadoCoop.objects.filter(activo=True)

            #Paso 2: Crear la cabecera de nomina
            nominaH = NominaCoopH()
            nominaH.fechaNomina = data['fechaNomina']
            nominaH.tipoNomina = TipoNomina.objects.get(id=data['tipoNomina'])
            nominaH.quincena = int(data['quincena'])
            nominaH.nota = data['nota']
            nominaH.userLog = User.objects.get(id=request.user.id)
            nominaH.save()

            #Paso 3: Crear el detalle de nomina por cada empleado
            for empleado in empleados:
                nominaD = NominaCoopD()
                nominaD.nomina = nominaH
                nominaD.empleado = empleado
                nominaD.salario = (empleado.sueldoActual / 2)
                nominaD.isr = decimal.Decimal(empleado.sueldoActual / 2) * decimal.Decimal(0.02)
                nominaD.afp = decimal.Decimal(empleado.sueldoActual / 2) * decimal.Decimal(0.032)
                nominaD.ars = decimal.Decimal(empleado.sueldoActual / 2) * decimal.Decimal(0.087)
                nominaD.cafeteria = 0
                nominaD.vacaciones = 0
                nominaD.otrosingresos = 0

                try:
                    if nominaH.quincena == 1:
                        montoAhorro = empleado.socio.cuotaAhorroQ1
                    else:
                        montoAhorro = empleado.socio.cuotaAhorroQ2

                except socio.DoesNotExist:
                    raise Exception("Este empleado aun no es socio activo de la cooperativa.")

                nominaD.descAhorros = montoAhorro

                #Buscar prestamos asociados al socio
                cuotaPrestamo = 0

                try:
                    prestamos = CuotasPrestamosEmpresa.objects.filter(socio=empleado.socio, estatus='P')

                    for p in prestamos:
                        cuotaPrestamo += p.montoTotal

                except CuotasPrestamosEmpresa.DoesNotExist:
                    cuotaPrestamo = 0

                except Exception as e:
                    raise Exception(e)

                nominaD.descPrestamos = cuotaPrestamo
                nominaD.save()

            return HttpResponse(nominaH.id)

        except IntegrityError as ie:
            return HttpResponse(-1)

        except Exception as e:
            return HttpResponse(e)


# Guardar Cambios en Detalle de Empleado (nomina generada)
class guardarDetalleEmpleado(View):
    def post(self, request, *args, **kwargs):

        try:
            # Tomar los parametros enviados por el Post en JSON
            data = json.loads(request.body)

            detalle = data['detalle']
            nomina = data['nomina']
            tipoNomina = data['tipoNomina']

            #Paso 1: Tomar la nomina que se esta trabajando
            nominaH = NominaCoopH.objects.get(fechaNomina=nomina, tipoNomina__descripcion=tipoNomina)

            #Paso 2: Tomar el empleado que sera modificado en dicha nomina
            emp = EmpleadoCoop.objects.get(socio__codigo=detalle['codigo'])

            #Paso 3: Tomar el detalle del empleado que sera modificado
            nominaD = NominaCoopD.objects.get(nomina=nominaH, empleado=emp)
            nominaD.salario = detalle['salario'].replace(',', '')
            nominaD.isr = detalle['isr'].replace(',', '') if detalle['isr'] != None else 0
            nominaD.afp = detalle['afp'].replace(',', '') if detalle['afp'] != None else 0
            nominaD.ars = detalle['ars'].replace(',', '') if detalle['ars'] != None else 0
            nominaD.cafeteria = detalle['cafeteria'].replace(',', '') if detalle['cafeteria'] != None else 0
            nominaD.vacaciones = detalle['vacaciones'].replace(',', '') if detalle['vacaciones'] != None else 0
            nominaD.otrosingresos = detalle['otrosIngresos'].replace(',', '') if detalle['otrosIngresos'] != None else 0
            nominaD.horasExtras = detalle['horasExtras'].replace(',', '') if detalle['horasExtras'] != None else 0
            nominaD.save()

            return HttpResponse(detalle['codigo'])

        except IntegrityError as ie:
            return HttpResponse(-1)

        except Exception as e:
            return HttpResponse(e)


# Eliminar nomina
class EliminarNominaView(View):
    def post(self, request, *args, **kwargs):

        try:

            data = json.loads(request.body)

            nomina = data['fechaNomina']
            tipoNomina = data['tipoNomina']

            nominaH = NominaCoopH.objects.filter(fechaNomina=nomina, tipoNomina__descripcion=tipoNomina)
            NominaCoopD.objects.filter(nomina=nominaH).delete()
            nominaH.delete()

            return HttpResponse(1)

        except Exception as e:
            return HttpResponse(e)


# ************ NOMINA PRESTAMOS Y AHORROS ***************

# Para obtener las dos nominas de un mes y asi proceder 
# con el posteo de cierre de mes.
class nominasPrestamosCierreMesView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):

        mes = self.request.GET.get('mes')

        if mes == None:
            nominas = NominaPrestamosAhorros.objects.all()
        else:
            nominas = NominaPrestamosAhorros.objects.filter(nomina__month=mes, tipo='PR', infoTipo='0015', estatus='PO', posteadaFecha=None)

        data = list()

        for nomina in nominas:

            data.append({
                'nomina': nomina.nomina,
                'tipo': nomina.tipo,
                'infoTipo': nomina.infoTipo,
                'estatus': nomina.estatus
            })

        return JsonResponse(data, safe=False)


# Guardar cambios de estatus para posteo de nomina de descuentos
class PosteoNominaPrestamosAhorro(LoginRequiredMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        pass
        

# Consultar si existe una nomina en especifico
class NominaPrestamosAhorrosView(LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):

        nomina = self.request.GET.get('nomina')
        tipoPrestamo = self.request.GET.get('tipoPrestamo')

        # Buscar la nomina para verificar si fue procesada (posteada)
        N = NominaPrestamosAhorros.objects.filter(nomina=nomina, estatus='PO').first()

        # PRESTAMOS PARA LA NOMINA ESPECIFICADA
        try:
            infoTipo = getInfoTipo(tipoPrestamo)
            nomP = NominaPrestamosAhorros.objects.get(nomina=nomina, infoTipo=infoTipo, tipo='PR')
            prestamos = 1
        except NominaPrestamosAhorros.DoesNotExist:
            prestamos = 0

        # AHORROS PARA LA NOMINA ESPECIFICADA
        try:
            nomA = NominaPrestamosAhorros.objects.get(nomina=nomina, tipo='AH')
            ahorros = 1
        except NominaPrestamosAhorros.DoesNotExist:
            ahorros = 0

        # BALANCES DE PRESTAMOS PARA LA NOMINA ESPECIFICADA
        try:
            Balances = NominaPrestamosAhorros.objects.get(nomina=nomina, infoTipo='2018', tipo='BP')
            balancesPrestamos = 1
        except NominaPrestamosAhorros.DoesNotExist:
            balancesPrestamos = 0

        # BALANCES DE AHORROS PARA LA NOMINA ESPECIFICADA
        try:
            Balances = NominaPrestamosAhorros.objects.get(nomina=nomina, infoTipo='2017', tipo='BA')
            balancesAhorros = 1
        except NominaPrestamosAhorros.DoesNotExist:
            balancesAhorros = 0

        # NOMINA PRESTAMOS APLICADOS
        try:
            prAplicados = NominaPrestamosAhorros.objects.get(nomina=nomina, infoTipo=infoTipo, tipo='PR', estatus='PO')
            prestamosAplicados = 1
        except NominaPrestamosAhorros.DoesNotExist:
            prestamosAplicados = 0

        # NOMINA AHORROS APLICADOS
        try:
            ahAplicados = NominaPrestamosAhorros.objects.get(nomina=nomina, tipo='AH', estatus='PO')
            ahorrosAplicados = 1
        except NominaPrestamosAhorros.DoesNotExist:
            ahorrosAplicados = 0

        data = list()

        data.append({
            'ahorros': ahorros,
            'prestamos': prestamos,
            'balancesPrestamos': balancesPrestamos,
            'balancesAhorros': balancesAhorros,
            'prestamosAplicados': prestamosAplicados,
            'ahorrosAplicados': ahorrosAplicados,
            'estatusNomina': N.estatus if N != None else ''
        })

        return JsonResponse(data, safe=False)


# Prestamos Regulares Sumarizados
# SELECT para obtener el listado de prestamos (Sumarizados por socio) que seran generados en el archivo.
def getPrestamosResumidos(self, fechaNomina):
    fecha = '{0}-{1:0>2}-{2:0>2}'.format(fechaNomina.year, fechaNomina.month, fechaNomina.day)

    registros = CuotasPrestamosEmpresa.objects.raw('SELECT \
											c.id, \
											s.codigo codigoSocioQ, \
											s.nombreCompleto, \
											SUM(c.valorCapital) montoCapital, \
											SUM(c.valorInteres) + SUM(c.valorInteresAh) montoInteres, \
											SUM(c.valorCapital) + SUM(c.valorInteres) + SUM(c.valorInteresAh) montoTotalQ \
										FROM nominacoop_cuotasprestamosempresa c \
										LEFT JOIN administracion_socio s ON c.socio_id = s.id \
										GROUP BY c.nomina, c.socio_id \
										HAVING c.nomina = \'' + fecha + '\' \
										AND c.infoTipoPrestamo = \'0015\' \
										ORDER BY c.socio_id \
										')
    return registros


# Guardar relacion del archivo de Pago de Nomina COOP con Nomina
def relacionArchivoBancoConNomina(request):
    data = json.loads(request.body)

    NominaCoopH.objects.filter(fechaNomina=data['fechaNomina'],
                               tipoNomina=TipoNomina.objects.get(descripcion=data['tipoNomina'])).update(
        archivoBanco=data['archivoBanco'])

    return HttpResponse(1)


# Generar archivo balance de prestamos
class GenerarArchivoPrestamosBalance(View):
    def post(self, request, *args, **kwargs):

        try:
            data = json.loads(request.body)

            nomina = datetime.strptime(data['fechaNomina'], '%Y%m%d')
            InfoTipo = data['infoTipo']  # 0015, entre otros
            fechanominaSAP = '{0:0>2}.{1:0>2}.{2}'.format(nomina.day, nomina.month,
                                                          nomina.year)  #Fecha con formato para SAP.
            fechaNomina = '{0}-{1:0>2}-{2:0>2}'.format(nomina.year, nomina.month, nomina.day)

            nominaH, created = NominaPrestamosAhorros.objects.get_or_create(nomina=fechaNomina, tipo='BP',
                                                                            infoTipo=InfoTipo)

            # Preparar archivo .TXT
            nombreArchivoFinal = 'PA{0}.TXT'.format(InfoTipo)
            pathFile = open(settings.ARCHIVOS_NOMINA + nombreArchivoFinal, 'wb+')
            sysFile = File(pathFile)
            sysFile.write('PERNR\tSUBTY\tBEGDA\tBETRG\n')  # Escribir Cabecera de archivo -- Columnas de header

            prestamos = getBalancesPrestamos(self)

            # Escribir cada linea de prestamo en el archivo
            for prestamo in prestamos:
                if prestamo.socio.estatus == 'S':  #Escribir en el archivo solo los Socios (ni Empleados Cooperativa ni Inactivos)
                    socioPago = CuotasPrestamosEmpresa.objects.raw('SELECT id, \
                                                                    SUM(valorCapital) + SUM(valorInteres) + SUM(valorInteresAh) TotalG \
                                                                    FROM nominacoop_cuotasprestamosempresa WHERE estatus = \'P\' \
                                                                    and socio_id = ' + str(prestamo.socio.id))
                    if socioPago[0].TotalG != None:
                        montoTotal = prestamo.balance - socioPago[0].TotalG

                        lineaFile = '{0}\t{1}\t{2}\t{3:0>13.2f}\n'.format(prestamo.codigoSocio, InfoTipo, fechanominaSAP,
                                                                          montoTotal)
                        sysFile.write(lineaFile)

            sysFile.close()

            return HttpResponse(1)

        except Exception as e:
            return HttpResponse(e)


# Generar archivo balance de ahorros
class GenerarArchivoAhorrosBalance(View):

    def post(self, request, *args, **kwargs):

        try:
            data = json.loads(request.body)

            nomina = datetime.strptime(data['fechaNomina'], '%Y%m%d')
            InfoTipo = data['infoTipo']
            fechanominaSAP = '{0:0>2}.{1:0>2}.{2}'.format(nomina.day, nomina.month, nomina.year) #Fecha con formato para SAP.
            fechaNomina = '{0}-{1:0>2}-{2:0>2}'.format(nomina.year, nomina.month, nomina.day)

            nominaH, created = NominaPrestamosAhorros.objects.get_or_create(nomina=fechaNomina, tipo='BA', infoTipo=InfoTipo)

            # Preparar archivo .TXT
            nombreArchivoFinal = 'PA{0}.TXT'.format(InfoTipo)
            pathFile = open(settings.ARCHIVOS_NOMINA + nombreArchivoFinal, 'wb+')
            sysFile = File(pathFile)
            sysFile.write('PERNR\tSUBTY\tBEGDA\tBETRG\n') # Escribir Cabecera de archivo -- Columnas de header

            socios = Socio.objects.filter(estatus='S').values('codigo', 'id')

            # Escribir cada linea de prestamo en el archivo
            for socio in socios:
                ahorro = getSocioAhorro(self, socio['id'])
                mQ = CuotasAhorrosEmpresa.objects.get(nomina=fechaNomina, estatus='P', socio__codigo=socio['codigo'])
                montoTotal = ahorro[0].balance + mQ.valorAhorro

                lineaFile = '{0}\t{1}\t{2}\t{3:0>13.2f}\n'.format(socio['codigo'], InfoTipo, fechanominaSAP, montoTotal)
                sysFile.write(lineaFile)

            sysFile.close()

            return HttpResponse(1)

        except Exception as e:
            return HttpResponse(e)


# Aplicar ahorros -- incrementar el balance de ahorro con la cuota actual
class AplicarAhorros(View):
    def post(self, request, *args, **kwargs):

        try:
            data = json.loads(request.body)

            nomina = data['nomina']
            cuotas = CuotasAhorrosEmpresa.objects.filter(nomina=nomina, estatus='P')

            for cuota in cuotas:
                insMaestra(self, cuota.socio.codigo, nomina, cuota.valorAhorro)

            # Actualizar los estatus de la tabla CuotasAhorrosEmpresa y NominaAhorrosAhorros para que no esten pendiente.
            cuotas.update(estatus='A')
            NominaPrestamosAhorros.objects.filter(nomina=nomina, infoTipo='0014', tipo='AH', estatus='PE').update(
                estatus='PO')
            NominaPrestamosAhorros.objects.filter(nomina=nomina, infoTipo='2017', tipo='BA', estatus='PE').update(
                estatus='PO')

            return HttpResponse(1)

        except Exception as e:
            return HttpResponse(e)


# Generar archivo para prestamos (Regulares, Bonificacion, Vacaciones, ...)
class GenerarArchivoPrestamos(View):
    def post(self, request, *args, **kwargs):

        try:
            data = json.loads(request.body)

            prestamos = data['prestamos']
            nomina = datetime.strptime(data['fechaNomina'], '%Y%m%d')
            InfoTipo = data['infoTipo']  # 0015, entre otros
            fechanominaSAP = '{0:0>2}.{1:0>2}.{2}'.format(nomina.day, nomina.month,
                                                          nomina.year)  #Fecha con formato para SAP.
            fechaNomina = '{0}-{1:0>2}-{2:0>2}'.format(nomina.year, nomina.month, nomina.day)

            nominaH, created = NominaPrestamosAhorros.objects.get_or_create(nomina=fechaNomina, tipo='PR',
                                                                            infoTipo=InfoTipo)

            # Preparar archivo .TXT
            nombreArchivoFinal = 'PA{0}.TXT'.format(InfoTipo)
            pathFile = open(settings.ARCHIVOS_NOMINA + nombreArchivoFinal, 'wb+')
            sysFile = File(pathFile)
            sysFile.write('PERNR\tSUBTY\tBEGDA\tBETRG\n')  # Escribir Cabecera de archivo -- Columnas de header

            # Agregar cada prestamo en la tabla de CuotasPrestamosEmpresa
            if created == False:
                CuotasPrestamosEmpresa.objects.filter(nomina=fechaNomina, infoTipoPrestamo=InfoTipo,
                                                      estatus='P').delete()

            for prestamo in prestamos:
                p = CuotasPrestamosEmpresa()
                p.socio = Socio.objects.get(codigo=prestamo['codigoSocio'])
                p.noPrestamo = MaestraPrestamo.objects.get(noPrestamo=prestamo['noPrestamo'])
                p.valorCapital = prestamo['montoCuotaQ']
                p.valorInteres = prestamo['cuotaInteresQ']
                p.valorInteresAh = prestamo['cuotaInteresAhQ']
                p.nomina = nomina
                p.infoTipoPrestamo = InfoTipo
                p.userLog = request.user
                p.save()

            #*******************************************************************************************************************
            # Aplicacion accion dependiendo del tipo de Prestamos de Nomina (Regulares, Bonificacion, Vacaciones, Regalia, Rifa)
            #*******************************************************************************************************************

            # PARA PRESTAMOS REGULARES
            if InfoTipo == '0015':
                prestamosParaArchivo = getPrestamosResumidos(self, nomina)
            else:
                # PARA PRESTAMOS TIPO BONIFICACION, VACACIONES, REGALIAS, RIFAS
                prestamosParaArchivo = CuotasPrestamosEmpresa.objects.filter(nomina=nomina, infoTipoPrestamo=InfoTipo)

            # Escribir cada linea de prestamo en el archivo
            for prestamo in prestamosParaArchivo:
                if prestamo.socio.estatus == 'S':  #Escribir en el archivo solo los Socios (ni Empleados Cooperativa ni Inactivos)

                    montoTotal = prestamo.montoTotalQ if InfoTipo == '0015' else prestamo.montoTotal

                    lineaFile = '{0}\t{1}\t{2}\t{3:0>13.2f}\n'.format(prestamo.codigoSocio, InfoTipo, fechanominaSAP,
                                                                      montoTotal)
                    sysFile.write(lineaFile)

            sysFile.close()

            return HttpResponse(1)

        except Exception as e:
            return HttpResponse(e)


# Generar archivo para ahorros
class GenerarArchivoAhorros(View):
    def post(self, request, *args, **kwargs):

        try:
            data = json.loads(request.body)

            ahorros = data['ahorros']
            nomina = datetime.strptime(data['fechaNomina'], '%Y%m%d')

            fechanominaSAP = '{0:0>2}.{1:0>2}.{2}'.format(nomina.day, nomina.month,
                                                          nomina.year)  #Fecha con formato para SAP.

            nominaH, created = NominaPrestamosAhorros.objects.get_or_create(nomina=nomina, tipo='AH', infoTipo='0014')

            # Preparar archivo .TXT
            nombreArchivoFinal = 'PA0014.TXT'
            pathFile = open(settings.ARCHIVOS_NOMINA + nombreArchivoFinal, 'wb+')
            sysFile = File(pathFile)
            sysFile.write('PERNR\tSUBTY\tBEGDA\tBETRG\n')  # Escribir Cabecera de archivo -- Columnas de header

            # Agregar cada ahorro en la tabla de CuotasAhorrosEmpresa
            if created:
                for ahorro in ahorros:
                    a = CuotasAhorrosEmpresa()
                    a.socio = Socio.objects.get(codigo=ahorro['codigo'])
                    a.valorAhorro = ahorro['cuotaAhorro']
                    a.nomina = nomina
                    a.userLog = request.user
                    a.save()

            # Recorrer los registros de ahorros generados para archivo .txt
            for ahorro in CuotasAhorrosEmpresa.objects.filter(nomina=nomina):
                if ahorro.socio.estatus == 'S':  #Escribir en el archivo solo los Socios (ni Empleados Cooperativa ni Inactivos)

                    lineaFile = '{0}\t{1}\t{2}\t{3:0>13.2f}\n'.format(ahorro.socio.codigo, '0014', fechanominaSAP,
                                                                      ahorro.valorAhorro)
                    sysFile.write(lineaFile)

            sysFile.close()

            return HttpResponse(1)

        except Exception as e:
            return HttpResponse(e)


#Funcion para retornar el infoTipo dependiendo del Tipo de Prestamo
def getInfoTipo(tipoPrestamo):
    if tipoPrestamo == 'RE':
        infoTipoP = '0015'
    elif tipoPrestamo == 'VA':
        infoTipoP = '2010'
    elif tipoPrestamo == 'BO':
        infoTipoP = '2012'
    elif tipoPrestamo == 'RG':
        infoTipoP = '2008'
    elif tipoPrestamo == 'RI':
        infoTipoP = '2012'

    return infoTipoP


# Aplicar prestamos -- actualiza balance de prestamos
class AplicarPrestamos(View):
    def post(self, request, *args, **kwargs):

        try:

            data = json.loads(request.body)

            nomina = data['nomina']
            tipoPrestamo = data['tipoPrestamo']

            infoTipo = getInfoTipo(tipoPrestamo)

            cuotas = CuotasPrestamosEmpresa.objects.filter(nomina=nomina, infoTipoPrestamo=infoTipo, estatus='P')

            for cuota in cuotas:
                prestamoMaestra = MaestraPrestamo.objects.get(noPrestamo=cuota.noPrestamo.noPrestamo)
                guardarPagoCuotaPrestamo(self, cuota.noPrestamo.noPrestamo, cuota.valorCapital, cuota.valorInteres,  \
                                            cuota.valorInteresAh, '{0}{1}'.format('NDCT', cuota.id), 'NM')
                
            # Actualizar los estatus de la tabla CuotasPrestamosEmpresa y NominaPrestamosAhorros para que no esten pendiente.
            cuotas.update(estatus='A')
            NominaPrestamosAhorros.objects.filter(nomina=nomina, infoTipo=infoTipo, tipo='PR', estatus='PE').update(
                estatus='PO')
            NominaPrestamosAhorros.objects.filter(nomina=nomina, infoTipo='2018', tipo='BP', estatus='PE').update(
                estatus='PO')

            return HttpResponse(1)

        except Exception as e:
            return HttpResponse(e)


# Postear Nomina Cooperativa
class PostearNominaCoopView(View):
    
    def post(self, request, *args, **kwargs):

        try:
            data = json.loads(request.body)

            NominaCoop = data['nomina']
            
            # Marcar nomina de los empleados de la cooperativa con posteada
            for nm in NominaCoop:
                nmcoop = NominaCoopH.objects.get(id=nm['id'])
                nmcoop.estatus = 'P'
                nmcoop.posteada = 'S'
                nmcoop.posteoUsr = request.user
                nmcoop.fechaPosteo = datetime.now()
                nmcoop.save()

            return HttpResponse(1)

        except Exception as e:
            return HttpResponse(e)
	
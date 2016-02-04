from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

#Vistas 
from acgm.views import InformacionGeneral
from fondoscajas.views import DesembolsoView, DesembolsoByCheque, ImprimirDesembolsoView
from nominacoop.views import NominaView, generaNominaView, EliminarNominaView, guardarDetalleEmpleado, NominaDescuentosView, \
                                GenerarArchivoPrestamos, GenerarArchivoAhorros, NominaPrestamosAhorrosView, AplicarPrestamos, \
                                AplicarAhorros, GenerarArchivoPrestamosBalance, rptNominaQuincenal, relacionArchivoBancoConNomina, \
                                GenerarArchivoAhorrosBalance, rptNominaDescAhorros, rptNominaDescPrestamos, PostearNominaCoopView, \
                                nominasPrestamosCierreMesView

from inventario.views import InventarioView, InventarioSalidaView, AjusteInvView, TransferenciaInvView, EntradaInventarioById, \
                                ImprimirEntradaInventarioView, RPTAjusteInventarioView, RPTMovimientoArticuloView, \
                                RPTExistenciaArticuloView, ListadoAjustesInvView, AjusteInventarioById, TransferenciaInvView, \
                                ListadoTransfInvView, ListadoSalidasInvView, SalidaInventarioById, InventarioEliminarView, \
                                InventarioSalidaEliminarView, RPTConteoFisicoArticuloView, getExistenciaConteoFisicoRPT, \
                                ProcesarAjusteInvView, EntradasInvBySuplidorRangoFecha, PostearDocumentosINV

from facturacion.views import FacturacionView, FacturaById, ImprimirFacturaView, RPTUtilidades, RPTUtilidadesView, RPTVentasDiariasView, \
                                RPTVentasResumidoView, RPTResumenVentas, FacturaEliminarView, PostearDocumentosFACT

from prestamos.views import NotaDeDebitoView, NotaDeCreditoView, validarAutorizadorView, \
                            DesembolsoPrestamosView, SolicitudPrestamoView, NotaDeCreditoEspView, \
                            SolicitudesPrestamosAPIViewByCodigoNombre, SolicitudPrestamoById, \
                            AprobarRechazarSolicitudesPrestamosView, PrestamosDesembolsoElectronico, \
                            ImprimirRecibidoConformeView, ImprimirSolicitudPView, MarcarPrestamoComoDCView, \
                            PostearPrestamosODView, rptSolPrestamosEmitidas, SolicitudesPrestamosAPIViewByRangoFecha, \
                            rptPrestamos, relacionArchivoBancoConDesembolsoElectronico, DistribucionInteresesView, \
                            PrestamosAPIViewByRangoFecha, PostearNotaDebitoView, PostearNotaCreditoView, TablaAmortizacionView, \
                            EstadoCuentaView, EstadoCuentaBySocio, ResumenEstadoSociosView


from prestamos.viewSolicitudOD import SolicitudOrdenDespachoView, SolicitudesODAPIView, AprobarRechazarSolicitudesODView, \
                                        SolicitudesODAPIViewByCodigoNombre, SolicitudODById, SolicitudOrdenDespachoDetalleView, \
                                        ImprimirODView, SolicitudesODAPIViewByCodigoSuplidor, rptSolicitudesBySuplidorRangoFecha

from prestamos.viewMaestraPrestamos import MaestraPrestamosView, PrestamoById, guardarCambiosPrestamo, PrestamosBySocioAPIView, \
                                            BalancePrestamosBySocioAPIView

from prestamos.viewNotaDebito import ListadoNDViewSet, guardarNotaDebito, NotaDeDebitoById
from prestamos.viewNotaCredito import ListadoNCViewSet, ListadoNCEViewSet, guardarNotaCredito, NotaDeCreditoById

from ahorro.views import AhorroView, MaestraAhorroView, impRetiroAHorro, generarInteres, DocumentosAhorro,historicoAHView
from cuenta.views import CuentasView, diarioView, mayorView, MaestroView
from cxp.views import CxpView, cxpSuperView, CxpSolicitud, CxpSuperSolicitud, cxpImpGeneral

from activofijo.views import ActivosView, DepresiacionView, CategoriaActivoView, impActivoView, LocActivoView, HistoricoActivos, ActDepresiados

from conciliacion.views import SolicitudView, ChequesView, NotasConciliacionView, ConBancoView, SSNotasView, SChequeView, DepositosView,  DepositoLs , regGenerico

#ViewSets (API)

from cuenta.views import DiarioViewSet

from administracion.views import ListadoCategoriasPrestamosViewSet

from ahorro.views import MaestraAhorroViewSet, AhorroViewSet, InteresAhorroViewSet, generarAhorro
from conciliacion.views import SolicitudViewSet, ChequesConsViewSet, NotasConsViewSet, ConBancoLs, SSolicitud, RepConciliacion
from facturacion.views import ListadoFacturasViewSet
from cuenta.views import CuentasViewSet

from cxp.views import CxpOrdenView, CxpSuperCoopView, cxpOrdenEdit, cxpSuperEdit

from reciboingreso.views import reciboTemplateView, reciboPost, reciboNominaTemplateView, reciboPrint

from administracion.views import SuplidorViewSet, SocioViewSet, DepartamentoViewSet, \
                                SuplidorTipoViewSet, ProductoViewSet,CoBeneficiarioViewSet, \
                                AutorizadoresViewSet, EmpresasViewSet, RepresentantesViewSet, \
                                CategoriaProductoViewSet, GenerarArchivoBancoView

from fondoscajas.views import ListadoDesembolsosViewSet
from nominacoop.views import ListadoNominasGeneradasViewSet, ListadoTiposNominasViewSet
from prestamos.views import InteresPrestamosBaseAhorroView


#APIView (API)
from administracion.views import CantidadCuotasPrestamosView, CantidadCuotasODView, CategoriaPrestamoByDescrpView,\
                                SuplidorByNombreView, ProductoByDescrpView, DocumentoCuentasView, SocioByCodigoView

from inventario.views import ListadoEntradasInvView, ListadoAlmacenesView, getExistenciaByProductoView, \
                                getExistenciaRPT, RPTMovimientoProductoAPIView

from nominacoop.views import DetalleNominaGeneradaAPIView
from prestamos.views import SolicitudesPrestamosAPIView, PagoCuotasPrestamoAPIViewByNoPrestamo, PrestamosAPIViewByCategoria
from prestamos.viewMaestraPrestamos import MaestraPrestamosAPIView

admin.site.site_header = 'COOPERATIVA'
router=routers.DefaultRouter()

#Cuentas
router.register(r'cuentas', CuentasViewSet)
router.register(r'diario', DiarioViewSet)


#ahorro
router.register(r'ahorro',AhorroViewSet)
router.register(r'InteresAhorro',InteresAhorroViewSet)

#administracion
router.register(r'categoriasPrestamos', ListadoCategoriasPrestamosViewSet)
router.register(r'suplidor', SuplidorViewSet)
router.register(r'tipoSuplidor', SuplidorTipoViewSet)
router.register(r'socio', SocioViewSet)
router.register(r'departamento', DepartamentoViewSet)
router.register(r'CoBeneficiario', CoBeneficiarioViewSet)
router.register(r'autorizador', AutorizadoresViewSet)
router.register(r'empresa', EmpresasViewSet)
router.register(r'representante', RepresentantesViewSet)
router.register(r'categoriasProductos', CategoriaProductoViewSet)

#conciliacion
router.register(r'Solicitud_Cheque',SolicitudViewSet)
router.register(r'cheques',ChequesConsViewSet)
router.register(r'notas_Conciliacion',NotasConsViewSet)

#inventario
router.register(r'inventario', ListadoEntradasInvView)
router.register(r'inventariosalidas', ListadoSalidasInvView)
router.register(r'almacenes', ListadoAlmacenesView)
router.register(r'ajustesInventario', ListadoAjustesInvView)
router.register(r'transfAlmacenes', ListadoTransfInvView)
router.register(r'producto', ProductoViewSet)

#facturacion
router.register(r'facturas', ListadoFacturasViewSet)

#fondos de cajas
router.register(r'desembolsos', ListadoDesembolsosViewSet)

#nomina
router.register(r'nominasgeneradas', ListadoNominasGeneradasViewSet)
router.register(r'tiposnomina', ListadoTiposNominasViewSet)

#prestamos
router.register(r'notasdebito', ListadoNDViewSet)
router.register(r'notascredito', ListadoNCViewSet)
router.register(r'notascreditoespecial', ListadoNCEViewSet)
router.register(r'interesPrestamosBaseAhorro', InteresPrestamosBaseAhorroView)


urlpatterns = patterns('',
    url(r'^$', 'acgm.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'acgm.views.login', name='login'),
    url(r'^mensajeError/$', 'acgm.views.mensajeError', name='error'),
    url(r'^mensajeInfo/$', 'acgm.views.mensajeInfo', name='info'),
    url(r'^informacionGeneral/$', InformacionGeneral.as_view(), name='informacion_general'),
    
    #Administracion
    url(r'^productosSearch/$', 'administracion.views.productosSearch', name='productos_search'),
    url(r'^productosSearch2/$', 'administracion.views.productosSearch2', name='productos_search2'),
    url(r'^cuentasSearch/$', 'cuenta.views.cuentasSearch', name='cuentas_search'),

    url(r'^api/cantidadCuotasPrestamos/(?P<monto>[\d\.]+)/$', CantidadCuotasPrestamosView.as_view(), name='cantidad_cuotas_prestamos'),
    url(r'^api/cantidadCuotasOD/(?P<monto>[\d\.]+)/$', CantidadCuotasODView.as_view(), name='cantidad_cuotas_OD'),
    url(r'^api/categoriasPrestamos/(?P<descrp>[\w\s]+)/$', CategoriaPrestamoByDescrpView.as_view(), name='categorias_prestamos_descrp'),
    url(r'^api/suplidor/nombre/(?P<nombre>[\w\s]+)/$', SuplidorByNombreView.as_view(), name='suplidor_by_nombre'),
    url(r'^api/producto/descripcion/(?P<descrp>[\w\s]+)/$', ProductoByDescrpView.as_view(), name='producto_by_descrp'),
    url(r'^api/documentoCuentas/(?P<doc>[\w]+)/$', DocumentoCuentasView.as_view(), name='documento_cuentas_by_codigo'),
    url(r'^api/socio/(?P<codigo>[\d]+)/$', SocioByCodigoView.as_view(), name='socio_by_codigo'),

    url(r'^generarArchivoBanco/$', GenerarArchivoBancoView.as_view(), name='generar_archivo_banco'),

    #Fondos de Cajas (Desembolsos)
    url(r'^desembolso/$', DesembolsoView.as_view(), name='Desembolso'),
    url(r'^desembolsojson/$', DesembolsoByCheque.as_view(), name='Desembolso_json'),
    
    #Fondos de Cajas (Desembolsos) # Imprimir
    url(r'^desembolso/print/(?P<desembolso>[\d]+)/$', ImprimirDesembolsoView.as_view(), name='desembolso_print'),

    #Nomina
    url(r'^nomina/$', NominaView.as_view(), name='Nomina'),
    url(r'^nomina/descuentos/$', NominaDescuentosView.as_view(), name='Nomina_Descuentos'),
    url(r'^nomina/descuentos/ahorros/reporte/$', rptNominaDescAhorros.as_view(), name='Nomina_Descuentos_Ahorros_Reporte'),
    url(r'^nomina/descuentos/prestamos/reporte/$', rptNominaDescPrestamos.as_view(), name='Nomina_Descuentos_Prestamos_Reporte'),
    url(r'^nomina/descuentos/aplicar/prestamos/$', AplicarPrestamos.as_view(), name='Aplicar_prestamos'),
    url(r'^nomina/descuentos/aplicar/ahorros/$', AplicarAhorros.as_view(), name='Aplicar_ahorros'),
    url(r'^nomina/descuentos/nominas/cierre/$', nominasPrestamosCierreMesView.as_view(), name='Nominas_Mes_Para_Cierre'),
    
    url(r'^nomina/generar/$', generaNominaView.as_view(), name='Generar_Nomina'),
    url(r'^nomina/eliminar/$', EliminarNominaView.as_view(), name='eliminar_nomina'),
    url(r'^nomina/guardarDE/$', guardarDetalleEmpleado.as_view(), name='guardar_detalle_nomina'),
    url(r'^nomina/verificarExistencia/$', NominaPrestamosAhorrosView.as_view(), name='verificar_existencia_nomina'),
    
    url(r'^nomina/archivos/prestamos/$', GenerarArchivoPrestamos.as_view(), name='nomina_archivo_prestamos'),
    url(r'^nomina/archivos/ahorros/$', GenerarArchivoAhorros.as_view(), name='nomina_archivo_ahorros'),
    url(r'^nomina/archivos/prestamos/balance/$', GenerarArchivoPrestamosBalance.as_view(), name='nomina_archivo_ahorros_balance'),
    url(r'^nomina/archivos/ahorros/balance/$', GenerarArchivoAhorrosBalance.as_view(), name='nomina_archivo_prestamos_balance'),
    url(r'^nomina/archivo-banco/set/$', relacionArchivoBancoConNomina, name='nomina_archivo_banco'),
    
    url(r'^api/nomina/detalle/$', DetalleNominaGeneradaAPIView.as_view(), name='detalle_nomina'),
    url(r'^api/nomina/detalle/(?P<nomina>[\w\-]+)/$', DetalleNominaGeneradaAPIView.as_view(), name='detalle_nomina2'),
    url(r'^nomina/reporte/quincena/$', rptNominaQuincenal.as_view(), name='reporte_nomina_quincena'),
    url(r'^nomina/coop/postear/$', PostearNominaCoopView.as_view(), name='nomina_cooperativa_postear'),

    #Inventario
    url(r'^inventario/$', InventarioView.as_view(), name='Inventario'),
    url(r'^inventario/salida/$', InventarioSalidaView.as_view(), name='Inventario_salida'),
    url(r'^inventariojson/$', EntradaInventarioById.as_view(), name='InventarioById'),
    url(r'^inventariosalidajson/$', SalidaInventarioById.as_view(), name='Inventario_SalidaById'),
    url(r'^inventario/ajuste/$', AjusteInvView.as_view(), name='AjusteInventario'),
    url(r'^inventario/ajustejson/$', AjusteInventarioById.as_view(), name='AjusteInventarioById'),
    url(r'^inventario/transferencia/$', TransferenciaInvView.as_view(), name='TransferenciaInventario'),
    url(r'^inventario/eliminar/$', InventarioEliminarView.as_view(), name='Inventario_eliminar'),
    url(r'^inventario/salida/eliminar/$', InventarioSalidaEliminarView.as_view(), name='Inventario_salida_eliminar'),
    url(r'^inventario/procesarAjuste/$', ProcesarAjusteInvView.as_view(), name='Inventario_procesar_ajuste'),
    url(r'^api/producto/existencia/(?P<codProd>[\w\s]+)/(?P<almacen>[\d]+)/$', getExistenciaByProductoView.as_view(), name='existencia_by_producto'),
    url(r'^api/inventario/entradas/(?P<suplidor>[\d]+)/(?P<fechaInicio>[\w\-]+)/(?P<fechaFin>[\w\-]+)/$', EntradasInvBySuplidorRangoFecha.as_view(), \
                                                                                                            name='Entradas_por_suplidor_y_rangoFecha'),
    url(r'^inventario/postear-registros/$', PostearDocumentosINV.as_view(), name='Inventario_postear_registros'),

    
    #Inventario#Imprimir
    url(r'^inventario/print/(?P<entrada>[\d]+)/$', ImprimirEntradaInventarioView.as_view(), name='Inventario_print'),
    #Inventario#Reportes
    url(r'^inventario/reportes/existenciaArticulo/$', RPTExistenciaArticuloView.as_view(), name='Inventario_reporte_existencia'),
    url(r'^inventario/reportes/conteoFisico/$', RPTConteoFisicoArticuloView.as_view(), name='Inventario_reporte_conteoFisico'),
    url(r'^inventario/reportes/histMovArt/$', RPTMovimientoArticuloView.as_view(), name='Inventario_reporte_historico'),
    url(r'^inventario/reportes/ajuste/$', RPTAjusteInventarioView.as_view(), name='Inventario_reporte_ajuste'),
    url(r'^inventario/api/reportes/existencia/$', getExistenciaRPT.as_view(), name='existencia_api'),
    url(r'^inventario/api/reportes/existencia/conteoFisico/$', getExistenciaConteoFisicoRPT.as_view(), name='existencia_conteoFisico_api'),
    url(r'^api/inventario/movimiento/(?P<codProd>[\w\s]+)/(?P<fechaInicio>[\w\-]+)/(?P<fechaFin>[\w\-]+)/(?P<almacen>[\d]+)/$', RPTMovimientoProductoAPIView.as_view(), name='mov_producto_api'),

    #Facturacion    
    url(r'^facturajson/$', FacturaById.as_view(), name='FacturaById'),
    url(r'^facturacion/$', FacturacionView.as_view(), name='Facturacion'),
    url(r'^facturacion/eliminar/$', FacturaEliminarView.as_view(), name='Facturacion_eliminar'),
    url(r'^facturacion/postear-registros/$', PostearDocumentosFACT.as_view(), name='Facturacion_postear_registros'),
    
    #Factura#Imprimir
    url(r'^facturacion/print/(?P<factura>[\d]+)/$', ImprimirFacturaView.as_view(), name='factura_print'),
    #Facturacion#Reportes
    url(r'^facturacion/reportes/utilidades/$', RPTUtilidades.as_view(), name='Reporte_Utilidades'),
    url(r'^facturacion/reportes/utilidades/vista/$', RPTUtilidadesView.as_view(), name='Reporte_Utilidades_vista'),
    url(r'^facturacion/reportes/ventasDiarias/$', RPTVentasDiariasView.as_view(), name='Reporte_ventasDiarias'),
    url(r'^facturacion/reportes/ventasResumido/$', RPTVentasResumidoView.as_view(), name='Reporte_ventasResumido'),
    url(r'^facturacion/reportes/ventasResumido/json/$', RPTResumenVentas.as_view(), name='Reporte_ventasResumido_json'),

    #Prestamos
    url(r'^prestamosSearch/$', 'prestamos.views.prestamosSearch', name='prestamos_search'),
    url(r'^pagoCuotasSearch/$', 'prestamos.views.pagoCuotasSearch', name='pago_cuotas_search'),
    url(r'^prestamos/nd/$', NotaDeDebitoView.as_view(), name='Nota_de_Debito'),
    url(r'^prestamos/nc/$', NotaDeCreditoView.as_view(), name='Nota_de_Credito'),
    url(r'^prestamos/nce/$', NotaDeCreditoEspView.as_view(), name='Nota_de_Credito_Especial'),
    url(r'^prestamos/maestra/$', MaestraPrestamosView.as_view(), name='Maestra_Prestamos'),
    url(r'^prestamos/desembolso/$', DesembolsoPrestamosView.as_view(), name='Desembolso_Prestamos'),
    url(r'^prestamos/solicitudP/$', SolicitudPrestamoView.as_view(), name='Solicitud_de_Prestamo'),
    url(r'^prestamos/solicitudOD/$', SolicitudOrdenDespachoView.as_view(), name='Solicitud_de_Orden_Despacho'),
    url(r'^prestamos/solicitudOD/detalle/$', SolicitudOrdenDespachoDetalleView.as_view(), name='Solicitud_de_Orden_Despacho_Detalle'),
    url(r'^prestamosDesembolsoElectronicojson/$', PrestamosDesembolsoElectronico.as_view(), name='prestamos_desembolso_electronico'),
    url(r'^prestamos/validaAutorizador/$', validarAutorizadorView.as_view(), name='valida_autorizador'),
    url(r'^prestamos/maestra/marcarcomo/$', MarcarPrestamoComoDCView.as_view(), name='marcar_prestamo_como'),
    url(r'^prestamos/maestra/cambios/$', guardarCambiosPrestamo.as_view(), name='Maestra_Prestamos_cambios'),
    url(r'^prestamos/archivo-banco/set/$', relacionArchivoBancoConDesembolsoElectronico, name='prestamos_archivo_banco'),
    url(r'^prestamos/pago-cuotas/$', PagoCuotasPrestamoAPIViewByNoPrestamo.as_view(), name='pago_cuotas'),
    url(r'^prestamos/pago-cuotas/(?P<noPrestamo>[\d]+)/$', PagoCuotasPrestamoAPIViewByNoPrestamo.as_view(), name='pago_cuotas'),
    url(r'^prestamos/tabla-amortizacion/$', TablaAmortizacionView.as_view(), name='tabla_amortizacion'),
    url(r'^prestamos/estado-cuenta/$', EstadoCuentaView.as_view(), name='estado_cuenta'),
    url(r'^prestamos/resumen-estado-socios/$', ResumenEstadoSociosView.as_view(), name='resumen_estado_socios'),

    #Prestamos#Imprimir
    url(r'^prestamos/print/solicitudP/$', ImprimirSolicitudPView.as_view(), name='Solicitud_de_Prestamo_print'),
    url(r'^prestamos/print/recibidoconforme/$', ImprimirRecibidoConformeView.as_view(), name='Recibido_Conforme_print'),

    #Prestamos#Reportes
    url(r'^prestamos/reportes/solicitudesPrestamos/$', rptSolPrestamosEmitidas.as_view(), name='solicitudes_prestamos_emitidas'),
    url(r'^prestamos/reportes/prestamos/$', rptPrestamos.as_view(), name='reporte_prestamos'),
    url(r'^prestamos/reportes/prestamos/(?P<fechaI>[\d]+)/$', SolicitudesPrestamosAPIViewByCodigoNombre.as_view(), \
                                                                                name='solicitud_prestamos_api_byCodigo'),
    url(r'^prestamos/reportes/consultaPrestamos/(?P<fechaI>[\w\-]+)/(?P<fechaF>[\w\-]+)/(?P<estatus>[\w]+)/$', PrestamosAPIViewByRangoFecha.as_view(), 
                                                                                name='consultar_prestamos'),
    url(r'^prestamos/reportes/consultaPrestamos/agrupadosPorCategoria/$', PrestamosAPIViewByCategoria.as_view(), \
                                                                        name='consultar_prestamos_agrupados_por_categoria'),

    #Prestamos -- Solicitudes Prestamos
    url(r'^prestamos/solicitudP/AprobarRechazar/$', AprobarRechazarSolicitudesPrestamosView.as_view(), name='Solicitud_de_Prestamo_accion'),
    url(r'^api/prestamos/solicitudes/prestamos/codigo/(?P<codigo>[\d]+)/$', SolicitudesPrestamosAPIViewByCodigoNombre.as_view(), \
                                                                                name='solicitud_prestamos_api_byCodigo'),
    url(r'^api/prestamos/solicitudes/prestamos/nombre/(?P<nombre>[\w\s]+)/$', SolicitudesPrestamosAPIViewByCodigoNombre.as_view(), \
                                                                                name='solicitud_prestamos_api_ByNombre'),
    url(r'^api/prestamos/solicitudes/prestamos/(?P<solicitud>[\d]+)/$', SolicitudesPrestamosAPIView.as_view(), name='solicitud_prestamos_api'),
    url(r'^api/prestamos/solicitudes/prestamos/$', SolicitudesPrestamosAPIView.as_view(), name='solicitud_prestamos_api'),
    url(r'^api/prestamos/solicitudes/prestamos/emitidos/(?P<fechaInicio>[\w\-]+)/(?P<fechaFin>[\w\-]+)/$', SolicitudesPrestamosAPIViewByRangoFecha.as_view(), \
                                                                                                            name='solicitud_prestamos_api_ByRangoFecha'),
    url(r'^solicitudPjson/$', SolicitudPrestamoById.as_view(), name='Solicitud_PrestamoById'),
    url(r'^estadoCuentajson/$', EstadoCuentaBySocio.as_view(), name='Estado_CuentaBySocio'),
 
    #Prestamos -- Solicitudes Orden Despacho
    url(r'^prestamos/solicitudOD/AprobarRechazar/$', AprobarRechazarSolicitudesODView.as_view(), name='Solicitud_de_OD_accion'),
    url(r'^api/prestamos/solicitudes/od/codigo/(?P<codigo>[\d]+)/$', SolicitudesODAPIViewByCodigoNombre.as_view(), name='solicitud_prestamos_api_byCodigo'),
    url(r'^api/prestamos/solicitudes/od/nombre/(?P<nombre>[\w\s]+)/$', SolicitudesODAPIViewByCodigoNombre.as_view(), name='solicitud_prestamos_api_ByNombre'),
    url(r'^api/prestamos/solicitudes/od/suplidor/(?P<suplidor>[\d]+)/(?P<fechaInicio>[\w\-]+)/(?P<fechaFin>[\w\-]+)/$', SolicitudesODAPIViewByCodigoSuplidor.as_view(), \
                                                                                                            name='solicitud_od_api_BySuplidorRangoFecha'),
    url(r'^api/prestamos/solicitudes/od/fecha/(?P<fechaInicio>[\w\-]+)/(?P<fechaFin>[\w\-]+)/$', SolicitudesODAPIViewByCodigoSuplidor.as_view(), \
                                                                                                    name='solicitudes_by_rangoFecha'),
    url(r'^api/prestamos/solicitudes/od/$', SolicitudesODAPIView.as_view(), name='solicitud_orden_despacho_api'),
    url(r'^solicitudODjson/$', SolicitudODById.as_view(), name='Solicitud_ODById'),
    url(r'^solicitudOD/print/(?P<noSolicitud>[\d]+)/$', ImprimirODView.as_view(), name='ordendespacho_print'),
    url(r'^prestamos/reportes/solicitudesOD/$', rptSolicitudesBySuplidorRangoFecha.as_view(), name='solicitudes_orden_despacho_reporte'),

    #Maestra Prestamos    
    url(r'^maestraPrestamojson/$', PrestamoById.as_view(), name='Maestra_Prestamo'),
    url(r'^maestraPrestamos/prestamosOD/postear/$', PostearPrestamosODView.as_view(), name='postear_prestamosOD'),
    url(r'^api/prestamos/maestra/listado/$', MaestraPrestamosAPIView.as_view(), name='maestra_prestamos_listado'),
    url(r'^api/prestamos/maestra/listado/(?P<prestamo>[\d]+)/$', MaestraPrestamosAPIView.as_view(), name='maestra_prestamos_byNo'),
    url(r'^api/prestamos/maestra/socio/detalle/(?P<socio>[\d]+)/$', PrestamosBySocioAPIView.as_view(), name='prestamos_by_socio_detalle'),
    url(r'^api/prestamos/maestra/socio/balance/(?P<socio>[\d]+)/$', BalancePrestamosBySocioAPIView.as_view(), name='prestamos_by_socio_balance'),
    url(r'^api/prestamos/maestra/socio/balance/$', BalancePrestamosBySocioAPIView.as_view(), name='prestamos_by_socio_balance'),
    
    #Nota de Debito
    url(r'^prestamos/nota-de-debito/guardar/$', guardarNotaDebito.as_view(), name='guardar_nota_de_debito'),
    url(r'^notadedebitojson/$', NotaDeDebitoById.as_view(), name='notadedebitoById'),
    url(r'^prestamos/nota-de-debito/postear/$', PostearNotaDebitoView.as_view(), name='postear_nota_de_debito'),


    #Nota de Credito
    url(r'^prestamos/nota-de-credito/guardar/$', guardarNotaCredito.as_view(), name='guardar_nota_de_credito'),
    url(r'^notadecreditojson/$', NotaDeCreditoById.as_view(), name='notadecreditoById'),
    url(r'^prestamos/nota-de-credito/postear/$', PostearNotaCreditoView.as_view(), name='postear_nota_de_credito'),


    #Distribucion de Intereses
    url(r'^prestamos/distribucion-intereses/$', DistribucionInteresesView.as_view(), name='distribucion-intereses'),


    #Ahorro
    url(r'^ahorro/$', AhorroView.as_view(), name='Ahorro'),
    url(r'^ahorrojson/$', MaestraAhorroView.as_view(), name='Maestra_Ahorro'),
    url(r'^impAhorro/$', impRetiroAHorro.as_view(), name='Imprimir_ahorro'),
    url(r'^generarAhorro/$',generarAhorro.as_view(), name='generar_ahorro'),
    url(r'^generarInteres/$', generarInteres.as_view(), name='generar_interes'),
    url(r'^documentoCuenta/$', DocumentosAhorro.as_view(), name='documentoCuenta'),
    url(r'^impHyAhorro/$', historicoAHView.as_view(), name='historico_ahorro'),

    #Cuentas
    url(r'^cuentasJson/$', CuentasView.as_view(), name='cuentas_diario'),
    url(r'^contabilidad/Maestro_json/$', MaestroView.as_view(), name='maestro_json'),
    url(r'^contabilidad/DiarioGeneral/$', diarioView.as_view(), name='diario_general'),
    url(r'^contabilidad/MayorGeneral/$', mayorView.as_view(), name='mayor_general'),
    url(r'^contabilidad/RegDiario/$', CuentasView.as_view(), name='reg_diario'),


    #CXP
    url(r'^cxp/cxpOrden/$', CxpView.as_view(), name='Cxp_Ordenes'),
    url(r'^cxpOrdenJson/$', CxpOrdenView.as_view(), name='Cxp_Ordenes_api'),
    url(r'^cxp/edit/$', cxpOrdenEdit.as_view(), name='Cxp_Orden_Edit'),
    url(r'^cxpSuper/edit/$', cxpSuperEdit.as_view(), name='cxp_Super_edit'),
    url(r'^cxpSuperJson/$', CxpSuperCoopView.as_view(), name='Cxp_SuperCoop_api'),
    url(r'^cxp/superOrden/$', cxpSuperView.as_view(), name='cxp_Super'),
    url(r'^cxp/solicitud/supercoop/$', CxpSuperSolicitud.as_view(), name='Solicitud_Cheques_super'),
    url(r'^cxp/solicitud/ordenCompra/$',CxpSolicitud.as_view(), name='solicitud_orden'),
    url(r'^cxp/imp/$',cxpImpGeneral.as_view(), name='imprimir_registro'),

    #ActivoFijo
    url(r'^activos/$', ActivosView.as_view(), name='ActivoFijo'),
    url(r'^depresiacion/$', DepresiacionView.as_view(), name='Depresiacion'),
    url(r'^categoriaActivo/$', CategoriaActivoView.as_view(), name='Categiria_activo'),
    url(r'^impActivo/$', impActivoView.as_view(), name='Imp_Activo'),
    url(r'^historicoAct/$',HistoricoActivos.as_view(), name="historico_act"),
    url(r'^activosDepresiados/$',ActDepresiados.as_view(), name='activosDepresiados'),
    url(r'^localidades/$', LocActivoView.as_view(), name='Localidad'),

    #Conciliacion Bancaria
    url(r'^conciliacion/Solicitudcheque$', SolicitudView.as_view(), name='Solicitud_Cheques'),
    url(r'^conciliacion/Cheques$', ChequesView.as_view(), name='Cheques_Conciliacion'),
    url(r'^conciliacion/Cheques/im$',SChequeView.as_view(), name='ImpCheque'),
    url(r'^conciliacion/notas$', NotasConciliacionView.as_view(), name='Notas_Conciliacion'),
    url(r'^conciliacion/notas/rg',SSNotasView.as_view(), name='Notas_Fechas' ),
    url(r'^conciliacion/banco$', ConBancoView.as_view(), name='Banco'),
    url(r'^conciliacion/banco/rg$', ConBancoLs.as_view(), name='Banco_Fechas'),
    url(r'^conciliacion/deposito/rg$', DepositoLs.as_view(), name='Deposito_fecha'),
    url(r'^conciliacion/Solicitudcheque/rg$',SSolicitud.as_view(), name='ImpSolicitud'),
    url(r'^conciliacion/depositos$', DepositosView.as_view(), name='Conciliacion_Deposito'),
    url(r'^conciliacion/registros$', RepConciliacion.as_view(), name='Reporte_Conciliacion'),
    url(r'^conciliacion/salida$', regGenerico.as_view(), name='Reporte_salida'),

    url(r'^reciboIngreso$',reciboTemplateView.as_view(), name='recibo_ingreso'),
    url(r'^postearRecibo$',reciboPost.as_view(), name='postear_recibo'), 
    url(r'^reciboNom$',reciboNominaTemplateView.as_view(), name="recibo_nomina"),
    url(r'^ImpRecibo$',reciboPrint.as_view(), name="Imprecibo_nomina"),
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),

)

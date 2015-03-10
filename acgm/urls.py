from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

#Vistas 
from fondoscajas.views import DesembolsoView, DesembolsoByCheque, ImprimirDesembolsoView
from nominacoop.views import NominaView, generaNominaView, EliminarNominaView, guardarDetalleEmpleado

from inventario.views import InventarioView, InventarioSalidaView, AjusteInvView, TransferenciaInvView, EntradaInventarioById, \
                                ImprimirEntradaInventarioView, RPTAjusteInventarioView, RPTMovimientoArticuloView, \
                                RPTExistenciaArticuloView, ListadoAjustesInvView, AjusteInventarioById, TransferenciaInvView, \
                                ListadoTransfInvView, ListadoSalidasInvView, SalidaInventarioById, InventarioEliminarView, \
                                InventarioSalidaEliminarView, RPTConteoFisicoArticuloView, getExistenciaConteoFisicoRPT, \
                                ProcesarAjusteInvView

from facturacion.views import FacturacionView, FacturaById, ImprimirFacturaView, RPTUtilidades, RPTUtilidadesView

from prestamos.views import NotaDeDebitoView, NotaDeCreditoView, validarAutorizadorView, \
                            DesembolsoPrestamosView, SolicitudPrestamoView, NotaDeCreditoEspView, \
                            SolicitudesPrestamosAPIViewByCodigoNombre, SolicitudPrestamoById, \
                            AprobarRechazarSolicitudesPrestamosView, PrestamosDesembolsoElectronico, \
                            ImprimirRecibidoConformeView, ImprimirSolicitudPView, MarcarPrestamoComoDCView

from prestamos.viewSolicitudOD import SolicitudOrdenDespachoView, SolicitudesODAPIView, AprobarRechazarSolicitudesODView, \
                                        SolicitudesODAPIViewByCodigoNombre, SolicitudODById, SolicitudOrdenDespachoDetalleView

from prestamos.viewMaestraPrestamos import MaestraPrestamosView, PrestamoById

from ahorro.views import AhorroView, MaestraAhorroView
from cuenta.views import CuentasView, diarioView, mayorView, MaestroView
from cxp.views import CxpView

#ViewSets (API)

from cuenta.views import DiarioViewSet, TipoDocViewSet

from administracion.views import ListadoCategoriasPrestamosViewSet

from ahorro.views import MaestraAhorroViewSet, AhorroViewSet, RetirosAhorroViewSet, InteresAhorroViewSet
from conciliacion.views import SolicitudViewSet, ChequesConsViewSet, NotasConsViewSet
from facturacion.views import ListadoFacturasViewSet
from cuenta.views import CuentasViewSet, AuxiliarViewSet

from cxp.views import OrdenViewSet, DetalleOrderViewSet, CxpOrdenView, CxpSuperCoop


from administracion.views import SuplidorViewSet, SocioViewSet, DepartamentoViewSet, \
                                SuplidorTipoViewSet, ProductoViewSet,CoBeneficiarioViewSet, \
                                AutorizadoresViewSet, EmpresasViewSet, RepresentantesViewSet, \
                                CategoriaProductoViewSet, GenerarArchivoBancoView

from fondoscajas.views import ListadoDesembolsosViewSet
from nominacoop.views import ListadoNominasGeneradasViewSet, ListadoTiposNominasViewSet


#APIView (API)
from administracion.views import CantidadCuotasPrestamosView, CantidadCuotasODView, CategoriaPrestamoByDescrpView,\
                                SuplidorByNombreView, ProductoByDescrpView, DocumentoCuentasView

from inventario.views import ListadoEntradasInvView, ListadoAlmacenesView, getExistenciaByProductoView, \
                                getExistenciaRPT, RPTMovimientoProductoAPIView

from nominacoop.views import DetalleNominaGeneradaAPIView
from prestamos.views import SolicitudesPrestamosAPIView
from prestamos.viewMaestraPrestamos import MaestraPrestamosAPIView
from facturacion.views import DetalleFacturasView


admin.site.site_header = 'COOPERATIVA'

router=routers.DefaultRouter()

#Cuentas
router.register(r'cuentas', CuentasViewSet)
router.register(r'auxiliar', AuxiliarViewSet)
router.register(r'diario', DiarioViewSet)
router.register(r'tipoDocDiario',TipoDocViewSet)

#CXP

router.register(r'ordenCompra',OrdenViewSet)
router.register(r'detalleOrder',DetalleOrderViewSet)


#ahorro
router.register(r'MaestraAhorros',MaestraAhorroViewSet)
router.register(r'ahorro',AhorroViewSet)
router.register(r'retiroAhorro',RetirosAhorroViewSet)
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
# router.register(r'maestraprestamos', PrestamosEnMaestraView)

urlpatterns = patterns('',

    url(r'^$', 'acgm.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'acgm.views.login', name='login'),
    url(r'^mensajeError/$', 'acgm.views.mensajeError', name='error'),
    url(r'^mensajeInfo/$', 'acgm.views.mensajeInfo', name='info'),
    
    #Administracion
    url(r'^productosSearch/$', 'administracion.views.productosSearch', name='productos_search'),
    url(r'^cuentasSearch/$', 'cuenta.views.cuentasSearch', name='cuentas_search'),

    url(r'^api/cantidadCuotasPrestamos/(?P<monto>[\d\.]+)/$', CantidadCuotasPrestamosView.as_view(), name='cantidad_cuotas_prestamos'),
    url(r'^api/categoriasPrestamos/(?P<descrp>[\w\s]+)/$', CategoriaPrestamoByDescrpView.as_view(), name='categorias_prestamos_descrp'),
    url(r'^api/suplidor/nombre/(?P<nombre>[\w\s]+)/$', SuplidorByNombreView.as_view(), name='suplidor_by_nombre'),
    url(r'^api/producto/descripcion/(?P<descrp>[\w\s]+)/$', ProductoByDescrpView.as_view(), name='producto_by_descrp'),
    url(r'^api/documentoCuentas/(?P<doc>[\w]+)/$', DocumentoCuentasView.as_view(), name='documento_cuentas_by_codigo'),
    
    url(r'^generarArchivoBanco/$', GenerarArchivoBancoView.as_view(), name='generar_archivo_banco'),

    #Fondos de Cajas (Desembolsos)
    url(r'^desembolso/$', DesembolsoView.as_view(), name='Desembolso'),
    url(r'^desembolsojson/$', DesembolsoByCheque.as_view(), name='Desembolso_json'),
    #Fondos de Cajas (Desembolsos) # Imprimir
    url(r'^desembolso/print/(?P<desembolso>[\d]+)/$', ImprimirDesembolsoView.as_view(), name='desembolso_print'),

    
    #Nomina
    url(r'^nomina/$', NominaView.as_view(), name='Nomina'),
    url(r'^nomina/generar/$', generaNominaView.as_view(), name='Generar_Nomina'),
    url(r'^nomina/eliminar/$', EliminarNominaView.as_view(), name='eliminar_nomina'),
    url(r'^nomina/guardarDE/$', guardarDetalleEmpleado.as_view(), name='guardar_detalle_nomina'),
    url(r'^api/nomina/detalle/$', DetalleNominaGeneradaAPIView.as_view(), name='detalle_nomina'),
    url(r'^api/nomina/detalle/(?P<nomina>[\w\-]+)/$', DetalleNominaGeneradaAPIView.as_view(), name='detalle_nomina2'),

    #Inventario
    url(r'^inventario/$', InventarioView.as_view(), name='Inventario'),
    url(r'^inventario/salida/$', InventarioSalidaView.as_view(), name='Inventario_salida'),
    url(r'^inventariojson/$', EntradaInventarioById.as_view(), name='InventarioById'),
    url(r'^inventariosalidajson/$', SalidaInventarioById.as_view(), name='Inventario_SalidaById'),
    url(r'^inventario/ajuste/$', AjusteInvView.as_view(), name='AjusteInventario'),
    url(r'^inventario/ajustejson/$', AjusteInventarioById.as_view(), name='AjusteInventarioById'),
    url(r'^inventario/transferencia/$', TransferenciaInvView.as_view(), name='TransferenciaInventario'),
    url(r'^api/producto/existencia/(?P<codProd>[\w\s]+)/(?P<almacen>[\d]+)/$', getExistenciaByProductoView.as_view(), name='existencia_by_producto'),
    url(r'^inventario/eliminar/$', InventarioEliminarView.as_view(), name='Inventario_eliminar'),
    url(r'^inventario/salida/eliminar/$', InventarioSalidaEliminarView.as_view(), name='Inventario_salida_eliminar'),
    url(r'^inventario/procesarAjuste/$', ProcesarAjusteInvView.as_view(), name='Inventario_procesar_ajuste'),
    
    #Inventario#Imprimir
    url(r'^inventario/print/(?P<entrada>[\d]+)/$', ImprimirEntradaInventarioView.as_view(), name='Inventario_print'),
    #Inventario#Reportes
    url(r'^inventario/reportes/existenciaArticulo/$', RPTExistenciaArticuloView.as_view(), name='Inventario_reporte_existencia'),
    url(r'^inventario/reportes/conteoFisico/$', RPTConteoFisicoArticuloView.as_view(), name='Inventario_reporte_conteoFisico'),
    url(r'^inventario/reportes/histMovArt/$', RPTMovimientoArticuloView.as_view(), name='Inventario_reporte_historico'),
    
    url(r'^inventario/reportes/ajuste/$', RPTAjusteInventarioView.as_view(), name='Inventario_reporte_ajuste'), #CONTRUCCION

    url(r'^inventario/api/reportes/existencia/$', getExistenciaRPT.as_view(), name='existencia_api'),
    url(r'^inventario/api/reportes/existencia/conteoFisico/$', getExistenciaConteoFisicoRPT.as_view(), name='existencia_conteoFisico_api'),
    
    url(r'^api/inventario/movimiento/(?P<codProd>[\w\s]+)/(?P<fechaInicio>[\w\-]+)/(?P<fechaFin>[\w\-]+)/(?P<almacen>[\d]+)/$', RPTMovimientoProductoAPIView.as_view(), name='mov_producto_api'),
    

    #Facturacion    
    url(r'^facturajson/$', FacturaById.as_view(), name='FacturaById'),
    url(r'^facturacion/$', FacturacionView.as_view(), name='Facturacion'),
    url(r'^api/facturacion/detalle/(?P<fechaInicio>[\w\-]+)/(?P<fechaFin>[\w\-]+)/$', DetalleFacturasView.as_view(), name='detalle_facturas'),

    #Factura#Imprimir
    url(r'^facturacion/print/(?P<factura>[\d]+)/$', ImprimirFacturaView.as_view(), name='factura_print'),

    #Facturacion#Reportes
    url(r'^facturacion/reportes/utilidades/$', RPTUtilidades.as_view(), name='Reporte_Utilidades'),
    url(r'^facturacion/reportes/utilidades/vista/$', RPTUtilidadesView.as_view(), name='Reporte_Utilidades_vista'),
    

    #Prestamos
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
    
    #Prestamos#Imprimir
    url(r'^prestamos/print/solicitudP/$', ImprimirSolicitudPView.as_view(), name='Solicitud_de_Prestamo_print'),
    url(r'^prestamos/print/recibidoconforme/$', ImprimirRecibidoConformeView.as_view(), name='Recibido_Conforme_print'),


    #Prestamos -- Solicitudes Prestamos
    url(r'^prestamos/solicitudP/AprobarRechazar/$', AprobarRechazarSolicitudesPrestamosView.as_view(), name='Solicitud_de_Prestamo_accion'),
    url(r'^api/prestamos/solicitudes/prestamos/codigo/(?P<codigo>[\d]+)/$', SolicitudesPrestamosAPIViewByCodigoNombre.as_view(), name='solicitud_prestamos_api_byCodigo'),
    url(r'^api/prestamos/solicitudes/prestamos/nombre/(?P<nombre>[\w\s]+)/$', SolicitudesPrestamosAPIViewByCodigoNombre.as_view(), name='solicitud_prestamos_api_ByNombre'),
    url(r'^api/prestamos/solicitudes/prestamos/(?P<solicitud>[\d]+)/$', SolicitudesPrestamosAPIView.as_view(), name='solicitud_prestamos_api'),
    url(r'^api/prestamos/solicitudes/prestamos/$', SolicitudesPrestamosAPIView.as_view(), name='solicitud_prestamos_api'),
    url(r'^solicitudPjson/$', SolicitudPrestamoById.as_view(), name='Solicitud_PrestamoById'),
    
    #Prestamos -- Solicitudes Orden Despacho
    url(r'^prestamos/solicitudOD/AprobarRechazar/$', AprobarRechazarSolicitudesODView.as_view(), name='Solicitud_de_OD_accion'),
    url(r'^api/prestamos/solicitudes/od/codigo/(?P<codigo>[\d]+)/$', SolicitudesODAPIViewByCodigoNombre.as_view(), name='solicitud_prestamos_api_byCodigo'),
    url(r'^api/prestamos/solicitudes/od/nombre/(?P<nombre>[\w\s]+)/$', SolicitudesODAPIViewByCodigoNombre.as_view(), name='solicitud_prestamos_api_ByNombre'),
    # url(r'^api/prestamos/solicitudes/od/(?P<solicitud>[\d]+)/$', SolicitudODById.as_view(), name='solicitud_od_api'),
    url(r'^api/prestamos/solicitudes/od/$', SolicitudesODAPIView.as_view(), name='solicitud_od_api'),
    url(r'^solicitudODjson/$', SolicitudODById.as_view(), name='Solicitud_ODById'),

    #Maestra Prestamos    
    url(r'^api/prestamos/maestra/listado/$', MaestraPrestamosAPIView.as_view(), name='maestra_prestamos_listado'),
    url(r'^api/prestamos/maestra/listado/(?P<prestamo>[\d]+)/$', MaestraPrestamosAPIView.as_view(), name='maestra_prestamos_byNo'),
    url(r'^maestraPrestamojson/$', PrestamoById.as_view(), name='Maestra_Prestamo'),

    


    #Ahorro
    url(r'^ahorro/$', AhorroView.as_view(), name='Ahorro'),
    url(r'^ahorrojson/$', MaestraAhorroView.as_view(), name='Maestra_Ahorro'),

    #Cuentas
    url(r'^cuentasJson/$', CuentasView.as_view(), name='cuentas_diario'),
    url(r'^contabilidad/Maestro_json/$', MaestroView.as_view(), name='maestro_json'),
    url(r'^contabilidad/DiarioGeneral/$', diarioView.as_view(), name='diario_general'),
    url(r'^contabilidad/MayorGeneral/$', mayorView.as_view(), name='mayor_general'),

    #CXP
    url(r'^cxp/cxpOrden/$', CxpView.as_view(), name='Cxp_Ordenes'),
    url(r'^cxpOrdenJson/$', CxpOrdenView.as_view(), name='Cxp_Ordenes_api'),
    url(r'^cxpSuperJson/$', CxpSuperCoop.as_view(), name='Cxp_SuperCoop_api'),

    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),

)

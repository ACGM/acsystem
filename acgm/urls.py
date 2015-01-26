from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

#Vistas 
from fondoscajas.views import DesembolsoView, DesembolsoByCheque
from nominacoop.views import NominaView, generaNominaView, EliminarNominaView, guardarDetalleEmpleado
from inventario.views import InventarioView, TransferenciaInvView, EntradaInventarioById
from facturacion.views import FacturacionView, FacturaById, OrdenDespachoSPView
from prestamos.views import NotaDeDebitoView, NotaDeCreditoView, MaestraPrestamosView, \
                            DesembolsoPrestamosView, SolicitudPrestamoView, NotaDeCreditoEspView, \
                            SolicitudOrdenDespachoView, SolicitudesPrestamosAPIViewByCodigoNombre, \
                            SolicitudPrestamoById, AprobarRechazarSolicitudesPrestamosView

from ahorro.views import AhorroView, MaestraAhorroView
from cuenta.views import DiarioGeneralView

#ViewSets (API)
from cuenta.views import CuentasViewSet, AuxiliarViewSet, DiarioViewSet, TipoDocViewSet
from cxp.views import OrdenViewSet, DetalleOrderViewSet, CxpSuperViewSet
from administracion.views import SuplidorViewSet, SocioViewSet, DepartamentoViewSet, SuplidorTipoViewSet,\
                                ListadoCategoriasPrestamosViewSet
from ahorro.views import MaestraAhorroViewSet, AhorroViewSet, RetirosAhorroViewSet, InteresAhorroViewSet
from conciliacion.views import SolicitudViewSet, ChequesConsViewSet, NotasConsViewSet
from facturacion.views import ListadoFacturasViewSet
from cuenta.views import CuentasViewSet, AuxiliarViewSet
from cxp.views import OrdenViewSet, DetalleOrderViewSet #, DetalleCuentaViewSet
from administracion.views import SuplidorViewSet, SocioViewSet, DepartamentoViewSet, \
                                SuplidorTipoViewSet, ProductoViewSet,CoBeneficiarioViewSet
from fondoscajas.views import ListadoDesembolsosViewSet
from nominacoop.views import ListadoNominasGeneradasViewSet, ListadoTiposNominasViewSet


#APIView (API)
from administracion.views import CantidadCuotasPrestamosView
from inventario.views import ListadoEntradasInvView, ListadoAlmacenesView
from nominacoop.views import DetalleNominaGeneradaAPIView
from prestamos.views import SolicitudesPrestamosAPIView


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
router.register(r'CxpSuperCoop',CxpSuperViewSet)

#ahorro
router.register(r'MaestraAhorros',MaestraAhorroViewSet)
router.register(r'ahorro',AhorroViewSet)
router.register(r'retiroAhorro',RetirosAhorroViewSet)
router.register(r'InteresAhorro',InteresAhorroViewSet)

#administracion
router.register(r'categoriasPrestamos', ListadoCategoriasPrestamosViewSet)
router.register(r'suplidor',SuplidorViewSet)
router.register(r'tipoSuplidor',SuplidorTipoViewSet)
router.register(r'socio',SocioViewSet)
router.register(r'departamento', DepartamentoViewSet)
router.register(r'CoBeneficiario',CoBeneficiarioViewSet)

#conciliacion
router.register(r'Solicitud_Cheque',SolicitudViewSet)
router.register(r'cheques',ChequesConsViewSet)
router.register(r'notas_Conciliacion',NotasConsViewSet)

#inventario
router.register(r'inventario', ListadoEntradasInvView)
router.register(r'almacenes', ListadoAlmacenesView)
router.register(r'producto', ProductoViewSet)

#facturacion
router.register(r'facturas', ListadoFacturasViewSet)

#fondos de cajas
router.register(r'desembolsos', ListadoDesembolsosViewSet)

#nomina
router.register(r'nominasgeneradas', ListadoNominasGeneradasViewSet)
router.register(r'tiposnomina', ListadoTiposNominasViewSet)

#prestamos
# router.register(r'solicitudesprestamos', SolicitudesPrestamosView)

urlpatterns = patterns('',

    url(r'^$', 'acgm.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mensajeError/$', 'acgm.views.mensajeError', name='error'),
    url(r'^mensajeInfo/$', 'acgm.views.mensajeInfo', name='info'),
    
    #Administracion
    url(r'^api/cantidadCuotasPrestamos/(?P<monto>[\d\.]+)/$', CantidadCuotasPrestamosView.as_view(), name='cantidad_cuotas_prestamos'),

    
    #Fondos de Cajas (Desembolsos)
    url(r'^desembolso/$', DesembolsoView.as_view(), name='Desembolso'),
    url(r'^desembolsojson/$', DesembolsoByCheque.as_view(), name='Desembolso_json'),
    
    #Nomina
    url(r'^nomina/$', NominaView.as_view(), name='Nomina'),
    url(r'^nomina/generar/$', generaNominaView.as_view(), name='Generar_Nomina'),
    url(r'^nomina/eliminar/$', EliminarNominaView.as_view(), name='eliminar_nomina'),
    url(r'^nomina/guardarDE/$', guardarDetalleEmpleado.as_view(), name='guardar_detalle_nomina'),
    url(r'^api/nomina/detalle/$', DetalleNominaGeneradaAPIView.as_view(), name='detalle_nomina'),
    url(r'^api/nomina/detalle/(?P<nomina>[\w\-]+)/$', DetalleNominaGeneradaAPIView.as_view(), name='detalle_nomina2'),

    
    #Inventario
    url(r'^inventario/$', InventarioView.as_view(), name='Inventario'),
    url(r'^inventariojson/$', EntradaInventarioById.as_view(), name='InventarioById'),
    url(r'^inventario/transferencia$', TransferenciaInvView.as_view(), name='TransferenciaInventario'),

    #Facturacion    
    url(r'^facturajson/$', FacturaById.as_view(), name='FacturaById'),
    url(r'^ordenSuperCoop/$', OrdenDespachoSPView.as_view(), name='Orden_de_Compra'),
    url(r'^facturacion/$', FacturacionView.as_view(), name='Facturacion'),
    
    # url(r'^categoriasPrestamos/(?P<id>[\d]+)/$', ListadoCategoriasPrestamosViewSet, name='CategoriaPrestamo'),
    # url(r'^inventariojson/$', EntradaInventarioById.as_view(), name='InventarioByIdo'),

    #Prestamos
    url(r'^prestamos/nd/$', NotaDeDebitoView.as_view(), name='Nota_de_Debito'),
    url(r'^prestamos/nc/$', NotaDeCreditoView.as_view(), name='Nota_de_Credito'),
    url(r'^prestamos/nce/$', NotaDeCreditoEspView.as_view(), name='Nota_de_Credito_Especial'),
    url(r'^prestamos/maestra/$', MaestraPrestamosView.as_view(), name='Maestra_Prestamos'),
    url(r'^prestamos/desembolso/$', DesembolsoPrestamosView.as_view(), name='Desembolso_Prestamos'),
    url(r'^prestamos/solicitudP/$', SolicitudPrestamoView.as_view(), name='Solicitud_de_Prestamo'),
    url(r'^prestamos/solicitudOD/$', SolicitudOrdenDespachoView.as_view(), name='Solicitud_de_Orden_Despacho'),
    
    url(r'^prestamos/solicitudP/AprobarRechazar$', AprobarRechazarSolicitudesPrestamosView.as_view(), name='Solicitud_de_Prestamo_accion'),

    url(r'^solicitudPjson/$', SolicitudPrestamoById.as_view(), name='Solicitud_PrestamoById'),

    url(r'^api/prestamos/solicitudes/prestamos/codigo/(?P<codigo>[\d]+)/$', SolicitudesPrestamosAPIViewByCodigoNombre.as_view(), name='solicitud_prestamos_api_byCodigo'),
    url(r'^api/prestamos/solicitudes/prestamos/nombre/(?P<nombre>[\w\s]+)/$', SolicitudesPrestamosAPIViewByCodigoNombre.as_view(), name='solicitud_prestamos_api_ByNombre'),
    url(r'^api/prestamos/solicitudes/prestamos/(?P<solicitud>[\d]+)/$', SolicitudesPrestamosAPIView.as_view(), name='solicitud_prestamos_api'),
    url(r'^api/prestamos/solicitudes/prestamos/$', SolicitudesPrestamosAPIView.as_view(), name='solicitud_prestamos_api'),

    


    #Ahorro
    url(r'^ahorro/$', AhorroView.as_view(), name='Ahorro'),
    url(r'^ahorrojson/$', MaestraAhorroView.as_view(), name='Maestra_Ahorro'),

    #Cuentas
    url(r'^cuentasJson/$', DiarioGeneralView.as_view(), name='cuentas_diario'),         

    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/',include(router.urls)),

)

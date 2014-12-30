from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

#Vistas 
from fondoscajas.views import DesembolsoView
from nominacoop.views import NominaView
from inventario.views import InventarioView, TransferenciaInvView
from facturacion.views import FacturacionView
from prestamos.views import NotaDeDebitoView, NotaDeCreditoView, MaestraPrestamosView, \
                            DesembolsoPrestamosView, SolicitudPrestamoView, NotaDeCreditoEspView

#ViewSets (API)
from cuenta.views import CuentasViewSet, AuxiliarViewSet
from cxp.views import OrdenViewSet, DetalleOrderViewSet, DetalleCuentaViewSet
from administracion.views import SuplidorViewSet, SocioViewSet, DepartamentoViewSet, \
                                SuplidorTipoViewSet, ProductoViewSet

#APIView (API)
from inventario.views import ListadoEntradasInvView

admin.site.site_header = 'COOPERATIVA'

router=routers.DefaultRouter()
router.register(r'cuentas', CuentasViewSet)
router.register(r'auxiliar', AuxiliarViewSet)
router.register(r'ordenCompra',OrdenViewSet)
router.register(r'detalleOrder',DetalleOrderViewSet)
router.register(r'detalleCuenta',DetalleCuentaViewSet)
router.register(r'suplidor',SuplidorViewSet)
router.register(r'tipoSuplidor',SuplidorTipoViewSet)
router.register(r'socio',SocioViewSet)
router.register(r'departamento', DepartamentoViewSet)
router.register(r'inventario', ListadoEntradasInvView)
router.register(r'producto', ProductoViewSet)


urlpatterns = patterns('',

    url(r'^$', 'acgm.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^desembolso/$', DesembolsoView.as_view(), name='Desembolso'),
    url(r'^nomina/$', NominaView.as_view(), name='Nomina'),
    url(r'^inventario/$', InventarioView.as_view(), name='Inventario'),
    url(r'^inventario/transferencia$', TransferenciaInvView.as_view(), name='Transferencia Inventario'),
    url(r'^facturacion/$', FacturacionView.as_view(), name='Facturacion'),
    url(r'^prestamos/nd/$', NotaDeDebitoView.as_view(), name='Nota de Debito'),
    url(r'^prestamos/nc/$', NotaDeCreditoView.as_view(), name='Nota de Credito'),
    url(r'^prestamos/nce/$', NotaDeCreditoEspView.as_view(), name='Nota de Credito Especial'),
    url(r'^prestamos/maestra/$', MaestraPrestamosView.as_view(), name='Maestra Prestamos'),
    url(r'^prestamos/desembolso/$', DesembolsoPrestamosView.as_view(), name='Desembolso Prestamos'),
    url(r'^prestamos/solicitudP/$', SolicitudPrestamoView.as_view(), name='Solicitud de Prestamo'),
    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/',include(router.urls)),

)

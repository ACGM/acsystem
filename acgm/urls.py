from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from fondoscajas.views import DesembolsoView
from nominacoop.views import NominaView
from cuenta.views import CuentasViewSet

admin.site.site_header = 'COOPERATIVA'

router=routers.DefaultRouter()
router.register(r'cuentas', CuentasViewSet)


urlpatterns = patterns('',

    url(r'^$', 'acgm.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^desembolso/$', DesembolsoView.as_view(), name='Desembolso'),
    url(r'^nomina/$', NominaView.as_view(), name='Nomina'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/',include(router.urls)),

)

from django.conf.urls import patterns, include, url
from django.contrib import admin

from fondoscajas.views import DesembolsoView
from nominacoop.views import NominaView


admin.site.site_header = 'COOPERATIVA'

urlpatterns = patterns('',

    url(r'^$', 'acgm.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^desembolso/$', DesembolsoView.as_view(), name='Desembolso'),
    url(r'^nomina/$', NominaView.as_view(), name='Nomina'),

)

from django.contrib import admin

from .models import SolicitudPrestamo, SolicitudOrdenDespachoH, SolicitudOrdenDespachoD, DesembolsoElectronico, \
					MaestraPrestamo, PrestamoUnificado, CuotasPrestamo, NotaDeCreditoPrestamo, NotaDeCreditoEspecial, \
					NotaDeDebitoPrestamo, DistribucionExcedente

@admin.register(SolicitudPrestamo)
class SolicitudPrestamoAdmin(admin.ModelAdmin):

	list_display = ['id', 'noSolicitud', 'fechaSolicitud', 'socio', 'salarioSocio', 'representante', 'cobrador', 'autorizadoPor', \
					'montoSolicitado', 'valorGarantizado', 'netoDesembolsar', 'categoriaPrestamo']

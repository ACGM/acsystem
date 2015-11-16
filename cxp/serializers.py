from rest_framework import serializers

# from .models import OrdenCompra, CxpSuperCoop

# # Serializador para el ViewSet de Ordenes de compra
# class OrdenSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = OrdenCompra
#         many = True
#         fields = (
#             'orden', 'suplidor', 'socio', 'fecha', 'monto', 'cuotas', 'montocuotas', 'detalleCuentas')


# #Serializador para ViewSet de CxpSuperCoop
# class CxpSuperCoopSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = CxpSuperCoop
#         many = True
#         fields = ('id', 'suplidor', 'factura', 'fecha', 'concepto', 'monto', 'descuento', 'detalleCuentas')
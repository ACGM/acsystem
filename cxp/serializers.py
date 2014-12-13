
from rest_framework import serializers
from .models import CxpSuperCoop, CxpSuperCoopDetalleCuentas, OrdenCompra, DetalleOrden, DetalleCuentasOrden

class OrdenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=OrdenCompra
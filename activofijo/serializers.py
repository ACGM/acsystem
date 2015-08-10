from rest_framework import serializers

from .models import CategoriaActivo, Depresiacion, Activos


class CategoriaActivoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CategoriaActivo
        many = False
        fields = ('id', 'descripcion')


class DepresiacionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Depresiacion
        many = True
        fields = ('id', 'dMensual', 'dAcumulada', 'dAgno', 'vLibro', 'cuentas')


class ActivosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Activos
        many = False
        fields = (
            'id', 'descripcion', 'categoria', 'fechaAdd', 'fechaDep', 'agnosVu', 'costo', 'porcentaje', 'suplidor',
            'factura', 'localidad', 'depresiacion', 'cuentas')
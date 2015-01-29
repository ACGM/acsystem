from django.shortcuts import render

from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ProductoSerializer, SuplidorTipoSerializer, SuplidorSerializer, \
						SocioSerializer, DepartamentoSerializer, CoBeneficiarioSerializer, \
						ListadoCategoriaPrestamoSerializer, CantidadCuotasPrestamosSerializer

from .models import Producto, Suplidor, TipoSuplidor, Socio, Departamento, CoBeneficiario, \
					CategoriaPrestamo, CuotaPrestamo


class ProductoViewSet(viewsets.ModelViewSet):
	queryset=Producto.objects.all().order_by('descripcion')
	serializer_class=ProductoSerializer


class SuplidorTipoViewSet(viewsets.ModelViewSet):
	queryset=TipoSuplidor.objects.all()
	serializer_class=SuplidorTipoSerializer


class SuplidorViewSet(viewsets.ModelViewSet):
	queryset=Suplidor.objects.all().order_by('nombre')
	serializer_class=SuplidorSerializer


class SocioViewSet(viewsets.ModelViewSet):
	queryset=Socio.objects.all().order_by('nombreCompleto')
	serializer_class=SocioSerializer


class DepartamentoViewSet(viewsets.ModelViewSet):
	queryset=Departamento.objects.all()
	serializer_class=DepartamentoSerializer


class CoBeneficiarioViewSet(viewsets.ModelViewSet):
	queryset=CoBeneficiario.objects.all()
	serializer_class=CoBeneficiarioSerializer


# Categorias de Prestamos
class ListadoCategoriasPrestamosViewSet(viewsets.ModelViewSet):

	queryset = CategoriaPrestamo.objects.all()
	serializer_class = ListadoCategoriaPrestamoSerializer


# Categoria de Prestamo por Descripcion
class CategoriaPrestamoByDescrpView(APIView):

	serializer_class = ListadoCategoriaPrestamoSerializer

	def get(self, request, descrp=None):
		
		categorias = CategoriaPrestamo.objects.filter(descripcion__contains=descrp)

		response = self.serializer_class(categorias, many=True)
		return Response(response.data)


# Cantidad de Cuotas (parametro: Monto)
class CantidadCuotasPrestamosView(APIView):

	serializer_class = CantidadCuotasPrestamosSerializer

	def get(self, request, monto=None):
		
		monto = CuotaPrestamo.objects.filter(montoDesde__lte=monto, montoHasta__gte=monto)

		response = self.serializer_class(monto, many=True)
		return Response(response.data)


# Suplidor por Nombre
class SuplidorByNombreView(APIView):

	serializer_class = SuplidorSerializer

	def get(self, request, nombre=None):
		if nombre != None:
			suplidores = Suplidor.objects.filter(nombre__contains=nombre, estatus='A').order_by('nombre')
		else:
			suplidores = Suplidor.objects.filter(estatus='A')

		response = self.serializer_class(suplidores, many=True)
		return Response(response.data)


# Producto por Descripcion
class ProductoByDescrpView(APIView):

	serializer_class = ProductoSerializer

	def get(self, request, descrp=None):
		if descrp != None:
			productos = Producto.objects.filter(descripcion__contains=descrp).order_by('descripcion')
		else:
			productos = Producto.objects.all()

		response = self.serializer_class(productos, many=True)
		return Response(response.data)

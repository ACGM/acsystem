from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, ListView, DetailView

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import MaestraAhorro, AhorroSocio, RetiroAhorro
from administracion.models import Socio, CoBeneficiario
from .serializers import maestraAhorroSerializer, AhorroSocioSerializer, RetiroAhorroSerializer

class MaestraAhorroViewSet(viewsets.ModelViewSet):
	queryset=MaestraAhorro.objects.all()
	serializer_class=maestraAhorroSerializer

class AhorroViewSet(viewsets.ModelViewSet):
	queryset=AhorroSocio.objects.all()
	serializer_class=AhorroSocioSerializer

class RetirosAhorroViewSet(viewsets.ModelViewSet):
	queryset=RetiroAhorro.objects.all()
	serializer_class=RetiroAhorroSerializer

class AhorroView(TemplateView):
	template_name = 'ahorro.html'




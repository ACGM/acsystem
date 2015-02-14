from django.shortcuts import render
from rest_framework import viewsets

# Local Imports
from .models import SolicitudCheque, ConcCheques, NotaDCConciliacion
from .serializers import solicitudSerializer, chequesSerializer, NotasSerializer


class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = SolicitudCheque.objects.all()
    serializer_class = solicitudSerializer


class ChequesConsViewSet(viewsets.ModelViewSet):
    queryset = ConcCheques.objects.all()
    serializer_class = chequesSerializer


class NotasConsViewSet(viewsets.ModelViewSet):
    queryset = NotaDCConciliacion.objects.all()
    serializer_class = NotasSerializer

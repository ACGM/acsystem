from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, View
from django.http import HttpResponse, JsonResponse


from rest_framework import viewsets

from .models import BalanzaComprobacion, MayorGeneral
from cuenta.models import DiarioGeneral, Cuentas, Auxiliares
from administracion.models import Socio

from acgm.views import LoginRequiredMixin

import json
import math
import decimal

class MayorView(DetailView):

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return self.render_to_response()






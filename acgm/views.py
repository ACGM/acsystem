from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
	return render(request, 'base.html')


# Mensaje de Error (GENERICO)
def mensajeError(request):
	return render(request, 'mensajeError.html')


# Mensaje de Informacion (GENERICO)
def mensajeInfo(request):
	return render(request, 'mensajeInfo.html')
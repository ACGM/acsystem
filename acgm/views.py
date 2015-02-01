from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

@login_required
def home(request):
	request.session.empresa = 'EMPRESA EJEMPLO'
	return render(request, 'homepage.html')

def login(request):

	return HttpResponseRedirect('/admin/login/')

# Mensaje de Error (GENERICO)
def mensajeError(request):
	return render(request, 'mensajeError.html')


# Mensaje de Informacion (GENERICO)
def mensajeInfo(request):
	return render(request, 'mensajeInfo.html')
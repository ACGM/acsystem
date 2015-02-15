from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from administracion.models import UserExtra

#Mixin for login_required
class LoginRequiredMixin(object):

	@classmethod
	def as_view(cls):
		return login_required(super(LoginRequiredMixin, cls).as_view())


#Pagina HOME -- principal		
@login_required
def home(request):
	localidad = UserExtra.objects.filter(usuario__username=request.user.username).values('localidad__descripcion')
	request.session['localidad'] = localidad[0]['localidad__descripcion']


	return render(request, 'homepage.html')

def login(request):

	return HttpResponseRedirect('/admin/login/')

# Mensaje de Error (GENERICO)
def mensajeError(request):
	return render(request, 'mensajeError.html')


# Mensaje de Informacion (GENERICO)
def mensajeInfo(request):
	return render(request, 'mensajeInfo.html')
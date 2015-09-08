from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import DetailView, View
from administracion.models import UserExtra, Empresa

#Mixin for login_required
class LoginRequiredMixin(object):

	@classmethod
	def as_view(cls):
		return login_required(super(LoginRequiredMixin, cls).as_view())


# Pagina HOME -- principal		
@login_required
def home(request):
	try:
		localidad = UserExtra.objects.filter(usuario__username=request.user.username).values('localidad__descripcion')
		request.session['localidad'] = localidad[0]['localidad__descripcion']

		request.session['XX'] = 'RRRAAAAA!!!!!'
		
	except Exception as e:
		return render(request, '404.html', {'mensaje': 'No tiene una localidad asignada.'})

	return render(request, 'homepage.html')

# Pagina de login de usuario
def login(request):

	return HttpResponseRedirect('/admin/login/')


# Mensaje de Error (GENERICO)
def mensajeError(request):
	return render(request, 'mensajeError.html')


# Mensaje de Informacion (GENERICO)
def mensajeInfo(request):
	return render(request, 'mensajeInfo.html')


# View para traer toda la informacion general de la Empresa
class InformacionGeneral(LoginRequiredMixin, DetailView):

	queryset = Empresa.objects.all()

	def get(self, request, *args, **kwargs):

		self.object_list = self.get_queryset()

		return self.json_to_response()

	def json_to_response(self):
		data = list()

		for infoG in self.object_list:
			usr = UserExtra.objects.get(usuario=self.request.user)

			data.append({
				'nombre': infoG.nombre,
				'rnc': infoG.rnc,
				'telefono': infoG.telefono,
				'localidadS': usr.localidad.descripcion,
				'localidadL': usr.localidad.descripcionLarga,
				})

		return JsonResponse(data, safe=False)

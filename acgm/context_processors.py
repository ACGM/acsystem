from django.contrib.auth.models import User
from django.http import JsonResponse

from administracion.models import UserExtra, Perfil, Opcion


# Esta funciona habilita/deshabilita las opciones de menu
# amarrados a un perfil de usuario.
def menu(request):
	
	try:
		loc = request.session.get('localidad')
		usuario = UserExtra.objects.get(usuario__username=request.user.username)
		perfilusr = Perfil.objects.get(perfilCod=usuario.perfil.perfilCod)

		opciones = Opcion.objects.filter(perfil=perfilusr)

		data = {'localidad': loc}

		for op in opciones:
			data[op.descripcion] = op.valor

		return data
		
	except Exception as e:
		if request.get_full_path()[:7] == '/admin/':
			return {'localidad': 'None'}
		pass

	# if request.user != 'AnonymousUser':

	# 	if request.user.username == 'coop':
	# 		return {'valor': 'true'}


		# import ipdb; ipdb.set_trace()

		
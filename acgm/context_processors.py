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

		return {
			'localidad': loc,
			opciones[0].descripcion : opciones[0].valor,
			opciones[1].descripcion : opciones[1].valor,
			opciones[2].descripcion : opciones[2].valor,
			opciones[3].descripcion : opciones[3].valor,
			opciones[4].descripcion : opciones[4].valor,
			opciones[5].descripcion : opciones[5].valor,
			opciones[6].descripcion : opciones[6].valor,
			opciones[7].descripcion : opciones[7].valor,
			opciones[8].descripcion : opciones[8].valor,
			opciones[9].descripcion : opciones[9].valor,
			opciones[10].descripcion : opciones[10].valor,
			opciones[11].descripcion : opciones[11].valor,
			opciones[12].descripcion : opciones[12].valor,
			opciones[13].descripcion : opciones[13].valor,
			opciones[14].descripcion : opciones[14].valor,
			opciones[15].descripcion : opciones[15].valor,
		} 
	except Exception as e:
		if request.get_full_path()[:7] == '/admin/':
			return {'localidad': 'None'}
		pass

	# if request.user != 'AnonymousUser':

	# 	if request.user.username == 'coop':
	# 		return {'valor': 'true'}


		# import ipdb; ipdb.set_trace()

		
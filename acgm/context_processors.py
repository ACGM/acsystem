from django.contrib.auth.models import User

def menu(request):
	
	loc = request.session.get('localidad')

	return {'valor': request.user, 'localidad': loc}

	# if request.user != 'AnonymousUser':

	# 	if request.user.username == 'coop':
	# 		return {'valor': 'true'}


		# import ipdb; ipdb.set_trace()

		
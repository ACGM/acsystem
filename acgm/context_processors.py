from django.contrib.auth.models import User

def menu(request):

	pass
	return {'valor': request.user}

	# if request.user != 'AnonymousUser':

	# 	if request.user.username == 'coop':
	# 		return {'valor': 'true'}


		# import ipdb; ipdb.set_trace()

		
from django.contrib.auth import authenticate
user = authenticate(username = 'john', password = 'secret')
if user is not None:
	if user.is_active:
		print("User is valid active and authenticated")
	else:
		print("The user is valid but is not active")
else:
	print("The username and password were incorrect")
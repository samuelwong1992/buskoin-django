from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from api.models import Profile, Payment
from api.serializers import ProfileSerializer, PaymentSerializer
import time

class BuskoinCustomAuthentication(ObtainAuthToken): 
	def post(self, request, *args, **kwargs):
		email = request.data.get("username", "")
		password = request.data.get("password", "")

		if not email :
			return Response({'error' : 'The email field is missing.'}, status=status.HTTP_200_OK )
		if not password :
			return Response({'error' : 'The password field is missing.'}, status=status.HTTP_200_OK )

		serializer = self.serializer_class(data=request.data, context={'request': request}) 
		try :
			serializer.is_valid(raise_exception=True)
		except :
			return Response({ 'error': 'We couldn\'t log you in with those credentials.' } )
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)

		return Response({ 'token': token.key }, status=status.HTTP_200_OK)

@api_view(('POST',))
def create_account(request) :
	stripe.api_key = "sk_test_51IXzZ1HfGkYzo1kqoRTIZ6a7frvG4gODZP5Hodeshw5jvWuWlo10eRRvK1sNUmypzYNjqmX9KxjwIV9cZYHVNL6o00f8YZV6QC"

	email = request.data.get("email", "")
	password = request.data.get("password", "")

	if not email :
		return Response({'error' : 'The email field is missing.'}, status=status.HTTP_200_OK )
	if not password :
		return Response({'error' : 'The password field is missing.'}, status=status.HTTP_200_OK )

	user = User.objects.filter(username = email)
	if user.exists() :
		return Response({'error' : 'The profile already exists.'}, status=status.HTTP_200_OK )

	account = stripe.Account.create(
		type='express',
		email=email,
		business_type='individual',
	)

	user = User.objects.create_user(username=email, password=password)

	profile = Profile()
	profile.user = user
	profile.stripe_id = account.id
	profile.save()

	account_links = stripe.AccountLink.create(
		account=account.id,
		refresh_url=settings.BASE_URL + "login/" + email + "/",
		return_url=settings.BASE_URL + "login/" + email + "/",
		type='account_onboarding',
		)

	return Response({'url' : account_links.url}, status=status.HTTP_200_OK )

@api_view(('POST',))
def create_payment_intent(request) :
	stripe.api_key = "sk_test_51IXzZ1HfGkYzo1kqoRTIZ6a7frvG4gODZP5Hodeshw5jvWuWlo10eRRvK1sNUmypzYNjqmX9KxjwIV9cZYHVNL6o00f8YZV6QC"

	value = request.POST.get("value", None)
	if not value :
		return Response({'error' : 'Value must exist.'}, status=status.HTTP_200_OK )

	value = int(value)*100

	if value < 1 :
		return Response({'error' : 'Value must be greater than  or equal to 1.'}, status=status.HTTP_200_OK )

	uuid = request.POST.get("user", None)
	if not uuid :
		return Response({'error' : 'ID must exist.'}, status=status.HTTP_200_OK )
	
	profile = Profile.objects.filter(uuid=uuid)
	if not profile :
		return Response({'error' : 'This profile doesn\'t exist.'}, status=status.HTTP_200_OK )
	profile = profile.first()

	payment = Payment()
	payment.entertainer = profile
	payment.save()

	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'name': 'Donation to ' + profile.entertainer_name,
			'amount': value,
			'currency': 'aud',
			'quantity': 1,
			'description': 'Thank you for your donation to ' + profile.entertainer_name,
			'images': ["{0}{1}{2}".format(settings.BASE_API_URL, settings.MEDIA_URL, profile.logo)],
		}],
		payment_intent_data={
			'application_fee_amount': 0,
			'transfer_data': {
				'destination': profile.stripe_id,
			},
		},
		success_url=settings.BASE_URL + 'confirmation/' + str(payment.uuid),
		cancel_url=settings.BASE_URL + 'tip-user/' + str(profile.uuid),
	)

	payment.stripe_id = session.payment_intent
	payment.save()
	
	return Response({'client_secret' : session}, status=status.HTTP_200_OK )

@api_view(('GET',))
def create_stripe_login(request) :
	stripe.api_key = "sk_test_51IXzZ1HfGkYzo1kqoRTIZ6a7frvG4gODZP5Hodeshw5jvWuWlo10eRRvK1sNUmypzYNjqmX9KxjwIV9cZYHVNL6o00f8YZV6QC"

	if not request.user.is_authenticated:
		return Response({'error' : 'Unathenticated.'}, status=status.HTTP_200_OK )
	
	profile = Profile.objects.filter(user=request.user)
	if not profile.exists() :
		return Response({'error' : 'Profile doesn\'t exist.'}, status=status.HTTP_200_OK )

	try :
		session = stripe.Account.create_login_link(
			profile.first().stripe_id,
		)
	except stripe.error.InvalidRequestError :
		session = stripe.AccountLink.create(
			account=profile.first().stripe_id,
			refresh_url=settings.BASE_URL + "profile/",
			return_url=settings.BASE_URL + "profile/",
			type='account_onboarding',
		)

	return Response({'client_secret' : session}, status=status.HTTP_200_OK )

@api_view(('GET', 'PATCH'))
def profile(request) :
	if not request.user.is_authenticated:
		return Response({'error' : 'Unathenticated.'}, status=status.HTTP_200_OK )
	
	profile = Profile.objects.filter(user=request.user)
	if not profile.exists() :
		return Response({'error' : 'Profile doesn\'t exist.'}, status=status.HTTP_200_OK )
	
	if request.method == 'GET' :
		serializer = ProfileSerializer(profile.first(), many = False, context={'request': request})
		return Response({'profile' : serializer.data}, status=status.HTTP_200_OK )
	elif request.method == 'PATCH' :
		serializer = ProfileSerializer(profile.first(), data=request.data, partial=True, context={'request': request})
		try :
			serializer.is_valid(raise_exception=True)
		except :
			return Response({ 'error': str(serializer.errors) }, status=status.HTTP_400_BAD_REQUEST )
		serializer.save()
		return Response({'profile' : serializer.data}, status=status.HTTP_200_OK )

@api_view(('GET',))
def fetch_profile(request, pk) :
	profile = Profile.objects.filter(uuid=pk)
	if not profile.exists() :
		return Response({'error' : 'Profile doesn\'t exist.'}, status=status.HTTP_200_OK )
	
	if request.method == 'GET' :
		serializer = ProfileSerializer(profile.first(), many = False, context={'request': request})
		return Response({'profile' : serializer.data}, status=status.HTTP_200_OK )
	elif request.method == 'PATCH' :
		serializer = ProfileSerializer(profile.first(), data=request.data, partial=True, context={'request': request})
		try :
			serializer.is_valid(raise_exception=True)
		except :
			return Response({ 'error': str(serializer.errors) }, status=status.HTTP_400_BAD_REQUEST )
		serializer.save()
		return Response({'profile' : serializer.data}, status=status.HTTP_200_OK )

@api_view(('GET',))
def fetch_payment(request, pk) :
	payment = Payment.objects.filter(uuid=pk)
	if not payment.exists() :
		return Response({'error' : 'Payment doesn\'t exist.'}, status=status.HTTP_200_OK )

	stripe.api_key = "sk_test_51IXzZ1HfGkYzo1kqoRTIZ6a7frvG4gODZP5Hodeshw5jvWuWlo10eRRvK1sNUmypzYNjqmX9KxjwIV9cZYHVNL6o00f8YZV6QC"
	payment = payment.first()

	pi = stripe.PaymentIntent.retrieve(payment.stripe_id,)
	serializer = ProfileSerializer(payment.entertainer, many = False, context={'request': request})
	if pi.status == 'succeeded' :
		return Response({'success': True, 'entertainer': serializer.data, 'value': pi.amount_received/100}, status=status.HTTP_200_OK )
	else :
		return Response({'error' : 'Payment was never completed', 'entertainer': serializer.data, 'code' : 1}, status=status.HTTP_200_OK )

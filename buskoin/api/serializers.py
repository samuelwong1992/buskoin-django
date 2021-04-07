from rest_framework import serializers
from django.conf import settings

from api.models import Profile, Payment

class ProfileSerializer(serializers.ModelSerializer) :
	class Meta: 
		model = Profile
		fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer) :
	profile = ProfileSerializer(many=False, read_only=True)

	class Meta: 
		model = Payment
		fields = '__all__'
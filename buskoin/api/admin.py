from django.contrib import admin

from api.models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin) :
	list_display = ('__str__',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin) :
	list_display = ('__str__',)
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from os.path import splitext
import uuid

def images_handler(instance, filename):
	today = datetime.today()

	return '{year}-{week}-{name}{ext}'.format(
		year=today.year,
		week=today.isocalendar()[1],
		name=today.strftime('%m%d%H%M%S%f'),
		ext=splitext(filename)[1].lower())

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	stripe_id = models.CharField(max_length=50)
	entertainer_name = models.CharField(max_length=50, blank=True)
	headline = models.CharField(max_length=500, blank=True)
	bio = models.TextField(blank=True)
	facebook_url = models.CharField(max_length=50, blank=True)
	insta_url = models.CharField(max_length=50, blank=True)
	youtube_url = models.CharField(max_length=50, blank=True)
	twitter_url = models.CharField(max_length=50, blank=True)
	snapchat_url = models.CharField(max_length=50, blank=True)
	logo = models.ImageField(upload_to=images_handler, blank=True)

	class Meta:
		verbose_name = 'Profile'
		verbose_name_plural = 'Profiles'

	def __str__(self):
		return self.user.username

class Payment(models.Model) :
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	entertainer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='payments')
	stripe_id = models.CharField(max_length=50)
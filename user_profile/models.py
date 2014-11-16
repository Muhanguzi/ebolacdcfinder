from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime 

def profile_picture_folder(instance, filename):
	return "profile_pictures/%s" % (filename)


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	about_me = models.CharField("About me", max_length=350, blank=True)

	activation_key = models.CharField(max_length=40, blank=True)
	key_expires = models.DateTimeField(default=datetime.today())
	
	profile_picture = models.ImageField(upload_to=profile_picture_folder, blank=True)    
	
	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name_plural=u'User profiles'


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

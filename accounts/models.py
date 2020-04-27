from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.db.models.signals import post_save, post_delete, post_init
from django.dispatch import receiver
from django.conf import settings
import os
from chat.models import Online
# Create your models here.
class UserType(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE,)
    About = models.CharField(max_length = 100, )
    phone = models.CharField(max_length = 100, )
    whatapp_number = models.CharField(max_length = 100, )
    Business_Name = models.CharField(max_length = 100, )
    Employment_status = models.CharField(max_length = 100, )
    Facebook_link = models.CharField(max_length = 100, )
    Successfully_trans = models.IntegerField(default=0,)
    role = models.CharField(max_length = 100, )
    img = models.FileField(upload_to = "gallery/profile/")
    # url = models.URLField("Website", blank=True)
    

    def __unicode__(self):
        return self.role

    def save(self, *args, **kwargs):
        if not self.img:
            self.img = 'U'
        return super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        if os.path.join(settings.MEDIA_ROOT, self.img.name) == os.path.join(settings.MEDIA_ROOT, 'U'):
            print('first time')
        else:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.img.name))
        


@receiver(post_save, sender= settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        UserType.objects.create(user=instance)
        
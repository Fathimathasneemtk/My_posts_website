from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from django.dispatch import receiver
from django.db.models.signals import post_save
class Profile(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    first_name=models.CharField( max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    username=models.CharField(max_length=150, blank=True)
    password=models.CharField(max_length=150, blank=True)
    image=ImageField(upload_to='profiles')
    def __str__(self):
        return self.user.username 
    
    @receiver(post_save,sender=User)
    def create_user_profile(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)

    

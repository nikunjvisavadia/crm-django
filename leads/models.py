from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save

class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    

class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)
    
    def __str__(self): 
        return f"{self.first_name} {self.last_name}"    

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email
    
    

def post_user_created_signal(sender, instance, created, **kwargs):    # this function is called when a new user has been created and saved to the database. This signal will be sent after all of the fields have been filled out by the user.
    # print(instance, created)
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User)
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # User details
    username = models.CharField(blank=True, max_length=50, unique=True)
    email = models.EmailField(blank=False, unique=True,
                              max_length=254, verbose_name='email address')


# profile model for each user
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='media/profile_pictures', default='default.png')
    bio = models.TextField()
    about = models.CharField(max_length=200)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    professions = models.CharField(max_length=300, blank=True)
    verified_user = models.BooleanField(default=False)
    address = models.CharField(max_length=250, unique=False)

    def __str__(self):
        return f'{self.user}'

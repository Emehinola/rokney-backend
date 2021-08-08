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

    def save(self, *args, **kwargs):
        # coverts all usernames to lowercase before saving to the database
        self.username = self.username.lower()
        super().save(*args, **kwargs)

# profile model for each user


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pictures', default='default.png')
    image_url = models.CharField(blank=True, max_length=300)
    bio = models.TextField(blank=True, default="my bio here...")
    about = models.CharField(max_length=200, blank=True,
                             default="about me here...")
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    professions = models.CharField(max_length=300, blank=True)
    verified_user = models.BooleanField(default=False)
    address = models.CharField(
        max_length=250, blank=True, default="Address: None")

    def save(self, *args, **kwargs):
        self.image_url = self.profile_pic
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}'

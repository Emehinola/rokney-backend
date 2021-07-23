from django.db.models.signals import post_save
from . models import CustomUser, Profile
from django.dispatch import receiver

# function get called to create profile whenever a new user is created


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            bio='My bio not updated',
            about='about me',
            followers=0,
            following=0,
            professions='',
            verified_user=False,
            address='My address here'

        )

        profile.save()

    else:
        pass


# post_save.connect(create_profile, sender=CustomUser) # does same work as the receiver decorator

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


User._meta.get_field('email')._unique = True

GENDER_CHOICES = [
    ('F', 'Female'),
    ('M', 'Male')
]

NOTIFICATION_TYPES = [
    ('W', 'Warning'),
    ('I', 'info'),
    ('D', 'danger'),
    ('S', 'Success')
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    gender = models.CharField(default="", max_length=1,
                              choices=GENDER_CHOICES,
                              null=True, blank=True)

    profile_image = models.ImageField(default='default.png',
                                      upload_to='users/',
                                      null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile data"


class Notifications(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    kind = models.CharField(default="", max_length=1,
                            choices=NOTIFICATION_TYPES,
                            null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_welcome_message(sender, **kwargs):
    if kwargs.get('created', False):
        Notifications.objects.create(user=kwargs.get('instance'),
                                     kind='S',
                                     title="Welcome to Roll Industries.",
                                     message="You've made it this far... Hooray!! But this is just the begining.")

        Notifications.objects.create(user=kwargs.get('instance'),
                                     kind='I',
                                     title="Blogging Services...",
                                     message="Blogging services coming soon to RI Members. Blogging services are offered for free.")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

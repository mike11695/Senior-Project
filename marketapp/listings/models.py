from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

#Extends the user model to added extra needed fields for the site
class User(AbstractUser):
    #added fields for the User class
    email = models.EmailField(max_length=100, unique=True)
    paypalEmail = models.EmailField(max_length=100,
        verbose_name="Paypal Email",
        help_text="E-mail that is connected to your PayPal account",
        unique=True)
    invitesOpen = models.BooleanField(default=True,
        verbose_name="Allow Invites for Events",
        help_text="Leave this field checked if you are interested in being invited to events.")
    inquiriesOpen = models.BooleanField(default=True,
        verbose_name="Allow Users to Contact You Through Profile",
        help_text="Leave this field checked if you are interested in being contacted by users through your profile.  If unchecked, users will only be able to contact you after you accept their offer or bid or you contact them.")

#Admin class that will be responsible for the site running smoothly
#Admins will be in charge of different responsiblities
"""class Admin(User):
    #potential extra fields will be added here
    warnUser = models.BooleanField(default=False)
    banUser = models.BooleanField(default=False)
    superAdmin = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True, verbose_text="Biography",
        help_text="A biography for your profile so others can know you better.")
    name = models.TextField(max_length=50, verbose_text="Full Name")
    country = models.TextField(max_length=50) #ideally should be obtained when the user shares ther location
    state = models.TextField(max_length=50) #ideally should be obtained when the user shares ther location
    city = models.TextField(max_length=50) #ideally should be obtained when the user shares ther location
    zip = models.TextField(max_length=10) #ideally should be obtained when the user shares ther location
    address = models.TextField(max_length=100)
    delivery = models.BooleanField(help_text="Check this if you are able to deliver items.")
    deliveryAddress = models.TextField(max_length=100, help_text="Submit an delivery address that you pick up items from if it differs from your home adress.")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_absolute_url(self):
        Returns the url to access a particular instance of Profile.
        return reverse('profile-detail', args=[str(self.id)])

    def __str__(self):
        String for representing the Profile object.
        return self.user"""

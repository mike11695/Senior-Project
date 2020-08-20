from django.db import models
from django.contrib.auth.models import AbstractUser, User
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
class Admin(User):
    #potential extra fields will be added here
    superAdmin = models.BooleanField(default=False, verbose_name="Super Admin",
        help_text="Admin that is able to set, remove and configure other Admin accounts.")
    handleListings = models.BooleanField(default=False,
        verbose_name="Can Handle Listings",
        help_text="Admin is able to manage user listings.")
    handleEvents = models.BooleanField(default=False,
        verbose_name="Can Handle Events",
        help_text="Admin is able to manage user events.")
    handleWishlists = models.BooleanField(default=False,
        verbose_name="Can Handle Wishlists",
        help_text="Admin is able to manage user wishlists.")
    handleImages = models.BooleanField(default=False,
        verbose_name="Can Handle Images",
        help_text="Admin is able to manage user images.")
    handleRatings = models.BooleanField(default=False,
        verbose_name="Can Handle Ratings",
        help_text="Admin is able to manage user ratings.")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True, verbose_name="Biography",
        help_text="A biography for your profile so others can know you better.", default="None")
    name = models.TextField(max_length=50, verbose_name="Full Name", default="None")
    country = models.TextField(max_length=50, default="None") #ideally should be obtained when the user shares ther location
    state = models.TextField(max_length=50, default="None") #ideally should be obtained when the user shares ther location
    city = models.TextField(max_length=50, default="None") #ideally should be obtained when the user shares ther location
    zipCode = models.TextField(max_length=10, verbose_name="Zip Code", default="None") #ideally should be obtained when the user shares ther location
    delivery = models.BooleanField(help_text="Check this if you are able to deliver items.", default=False)
    deliveryAddress = models.TextField(max_length=100, verbose_name="Delivery Address",
        help_text="Submit an delivery address that you pick up items from.",
        default="None")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_absolute_url(self):
        """Returns the url to access a particular instance of Profile."""
        return reverse('profile-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Profile object."""
        return f'{self.user}, "s Profile"'

class Rating(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    reviewer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="reviewer")
    ratingValue = models.IntegerField(default=1,
        verbose_name="Rating",
        help_text="Rating for user from 1 to 5, 5 being the best.")
    feedback = models.TextField(max_length=500,
        help_text="Leave feedback for the user you're rating.")

    def get_absolute_url(self):
        """Returns the url to access a particular instance of Rating."""
        return reverse('rating-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Rating object."""
        return f'"Feedback from ", {self.reviewer}'

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from listings.models import User, Image, Tag, Item, Listing, OfferListing, AuctionListing
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=100, help_text='Enter a valid e-mail address')
    paypalEmail = forms.EmailField(max_length=100, label="Paypal Email",
        help_text='Enter a valid Paypal e-mail address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'paypalEmail', 'password1', 'password2', )

class AddImageForm(ModelForm):
    def clean_image(self):
        clean_image = self.cleaned_data.get('image', False)

        #check image size to ensure it meets the limit
        if clean_image:
            width, height = get_image_dimensions(clean_image)
            if width > 1250 or height > 1250:
                raise ValidationError("Height or Width is larger than limit allowed.")
            return clean_image
        else:
            raise ValidationError("No image found")

    name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Image
        fields = ['image', 'name', 'tags']
        exclude = ['owner']
        help_texts = {'image': "Image must not be larger than 1250x1250."}

class AddItemForm(ModelForm):
    images = forms.ModelMultipleChoiceField(queryset=None, help_text="An image is required.")
    name = forms.CharField(max_length=50, required=True, help_text="Name for item is required.")

    class Meta:
        model = Item
        fields = ['images', 'name', 'description']
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       super(AddItemForm, self).__init__(*args, **kwargs)
       self.fields['images'].queryset = Image.objects.filter(owner=self.user)

class CreateOfferListingForm(ModelForm):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), help_text="An item is required.")
    name = forms.CharField(max_length=50, required=True, help_text="Name for listing is required.")

    class Meta:
        model = OfferListing
        fields = ['name', 'description', 'items', 'endTimeChoices', 'openToMoneyOffers',
            'minRange', 'maxRange', 'notes']
        exclude = ['owner', 'endTime', 'listingEnded']

    def __init__(self, *args, **kwargs):
       self.user = kwargs.pop('user')
       super(CreateOfferListingForm, self).__init__(*args, **kwargs)
       self.fields['items'].queryset = Item.objects.filter(owner=self.user)

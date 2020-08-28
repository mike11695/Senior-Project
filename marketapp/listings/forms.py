from django import forms
from django.contrib.auth.forms import UserCreationForm
from listings.models import User, Image, Tag

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=100, help_text='Enter a valid e-mail address')
    paypalEmail = forms.EmailField(max_length=100, label="Paypal Email",
        help_text='Enter a valid Paypal e-mail address')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'paypalEmail', 'password1', 'password2', )

"""class AddImageForm(forms.Form):
    image = forms.ImageField(required=True, help_text="Images must not be bigger than 2000x2000")
    name = forms.CharField(max_length=50, required=True)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Image
        fields = ('owner', 'image', 'name', 'tags')"""

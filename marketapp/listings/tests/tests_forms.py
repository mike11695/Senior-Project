from django.test import TestCase
from listings.forms import SignUpForm

# Create your tests here.
class SignUpFormTest(TestCase):
    def test_valid_signup(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "exampleEmail@gmail.com"
        paypalEmail = "examplePaypalEmail@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        data = {
            'username': username,
            'password1': password1,
            'password2': password2,
            'email': email,
            'paypalEmail': paypalEmail,
            'first_name': first_name,
            'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())

    def test_valid_paypal_email(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "example@gmail.com"
        paypalEmail = "examplegmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        data = {
            'username': username,
            'password1': password1,
            'password2': password2,
            'email': email,
            'paypalEmail': paypalEmail,
            'first_name': first_name,
            'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_valid_email(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "examplegmail.com"
        paypalEmail = "example@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        data = {
            'username': username,
            'password1': password1,
            'password2': password2,
            'email': email,
            'paypalEmail': paypalEmail,
            'first_name': first_name,
            'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_valid_paypal_email_length(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "example@gmail.com"
        paypalEmail = "exampleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        data = {
            'username': username,
            'password1': password1,
            'password2': password2,
            'email': email,
            'paypalEmail': paypalEmail,
            'first_name': first_name,
            'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_valid_email_length(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "exampleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee@gmail.com"
        paypalEmail = "example@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        data = {
            'username': username,
            'password1': password1,
            'password2': password2,
            'email': email,
            'paypalEmail': paypalEmail,
            'first_name': first_name,
            'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_first_name_required(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "exampleEmail@gmail.com"
        paypalEmail = "examplePaypalEmail@gmail.com"
        last_name = "Lopez"
        data = {
            'username': username,
            'password1': password1,
            'password2': password2,
            'email': email,
            'paypalEmail': paypalEmail,
            'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_last_name_required(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8265"
        email = "exampleEmail@gmail.com"
        paypalEmail = "examplePaypalEmail@gmail.com"
        first_name = "Michael"
        data = {
            'username': username,
            'password1': password1,
            'password2': password2,
            'email': email,
            'paypalEmail': paypalEmail,
            'first_name': first_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_passwords_must_match(self):
        username = "Mikael"
        password1 = "examplepassword8265"
        password2 = "examplepassword8266"
        email = "exampleEmail@gmail.com"
        paypalEmail = "examplePaypalEmail@gmail.com"
        first_name = "Michael"
        last_name = "Lopez"
        data = {
            'username': username,
            'password1': password1,
            'password2': password2,
            'email': email,
            'paypalEmail': paypalEmail,
            'first_name': first_name,
            'last_name': last_name
        }
        form = SignUpForm(data)
        self.assertFalse(form.is_valid())

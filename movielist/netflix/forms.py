from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    firstname = forms.CharField(label="First name")
    lastname = forms.CharField(label="Last name")
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password_conf = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

def clean(self):
        super(RegisterForm, self).clean()

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password_conf = self.cleaned_data.get('password_conf')

        if password != password_conf:
            self._errors['password_conf'] = self.error_class([
                "wrong confirmation"
            ])

        if User.objects.filter(username=email).exists():
            self._errors['email'] = self.error_class(['Email already exist'])

        return self.cleaned_data

class LoginForm(forms.Form):

    email = forms.EmailField(label="Email Address")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class SearchForm(forms.Form):
    search_text = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search'})
    )


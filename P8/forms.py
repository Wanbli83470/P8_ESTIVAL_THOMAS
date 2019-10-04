"""the Django forms class is used to automatically generate HTML forms with the right parameters"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )



class ConnexionForm(forms.Form):
    """Creating the form class for the user login"""
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class SearchForm(forms.Form):
    """Creating the form class for the search field"""
    Recherche = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'placeholder': 'Je remplace...'}))
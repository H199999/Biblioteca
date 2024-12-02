from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username' : 'Nombre',
            'password1' : 'Contraseña',  
            'password2' : 'Confirmar contraseña',
        }

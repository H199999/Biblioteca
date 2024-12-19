from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from prestamos.models import CustomUser, Rol
class CustomUserCreationForm(UserCreationForm):
    rol = forms.ChoiceField(
        choices=Rol.ROL_CHOICES,
        label="Rol",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'last_name', 'rut', 'phone', 'mail', 'password1', 'password2', 'rol']
        widgets = {
           'username': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '9',
                'pattern': '[0-9]{9}',
                'title': 'El RUT debe contener exactamente 9 dígitos numéricos.'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '15',
                'pattern': '[0-9]{8,15}', 
                'title': 'El número de teléfono debe tener entre 8 y 15 dígitos.'
            }),
            'mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("El número de teléfono debe contener solo dígitos.")
        if len(phone) < 8 or len(phone) > 15:
            raise forms.ValidationError("El número de teléfono debe tener entre 8 y 15 dígitos.")
        return phone
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not rut.isdigit() or len(rut) != 9:
            raise forms.ValidationError("El RUT debe tener exactamente 9 dígitos numéricos.")
        return rut

    def save(self, commit=True):
        user = super().save(commit=False)
        rol_seleccionado = self.cleaned_data.get('rol')
        rol = Rol.objects.get_or_create(rut=user.rut, rol=rol_seleccionado)[0]
        user.rol = rol
        if commit:
            user.save()
        return user
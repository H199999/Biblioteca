from django import forms
from .models import Prestamo,Book,Author,Renovacion,Editor,PerfilCliente
from datetime import date

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['book', 'date_devolucion']  
        widgets = {
            'date_devolucion': forms.DateInput(attrs={'type': 'date'}),
            'devuelto': forms.RadioSelect(choices=[(True, 'Sí'), (False, 'No')]),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = PerfilCliente
        fields = ['rut','name','last_name','phone', 'mail']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'year', 'description', 'category', 'editor','estado', 'stock', 'image']
        widgets = {
            'stock': forms.NumberInput(attrs={'min': 1, 'max': 20}),
            'year': forms.NumberInput(attrs={'min': 1000, 'max': date.today().year}),
            'estado': forms.RadioSelect(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [ 'title', 'author', 'year', 'description', 'category', 'editor','estado', 'stock', 'image']
        widgets = {
            'stock': forms.NumberInput(attrs={'min': 1, 'max': 20}),
            'year': forms.NumberInput(attrs={'min': 1000, 'max': date.today().year}),
            'estado': forms.RadioSelect(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'date_birth']
        widgets = {
            'date_birth': forms.DateInput(attrs={'type': 'date'})
        }
    
class RenovForm(forms.ModelForm):
    class Meta:
        model = Renovacion
        fields = ['date_redevolucion','day_devolucion']
        widgets = {
            'date_devolucion': forms.DateInput(attrs={'type': 'date'}),
            'day_devolucion': forms.CheckboxSelectMultiple()
        }

class EditorForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = ['name']
        widgets = {
            'editor': forms.CheckboxSelectMultiple()}
 


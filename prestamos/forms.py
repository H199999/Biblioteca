from django import forms
from .models import Prestamo,Book,Author,Renovacion,Editor

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['book', 'user','date_devolucion', 'devuelto']
        widgets = {
            'date_devolucion': forms.DateInput(attrs={'type': 'date'}),
            'devuelto': forms.CheckboxSelectMultiple()
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'year', 'description', 'category', 'image']
        widgets = {
            'category': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['isbn'].disabled = True 
        
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
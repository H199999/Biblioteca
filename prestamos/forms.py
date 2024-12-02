from django import forms
from .models import Prestamo, Book,Author

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['book', 'user','date_devolucion']
        widgets = {
            'date_devolucion': forms.DateInput(attrs={'type': 'date'})
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
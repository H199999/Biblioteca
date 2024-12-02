from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")

    def __str__(self):
        return self.name

class Author(models.Model):
    name= models.CharField(max_length=100, verbose_name="Nombre")
    date_birth= models.DateField(verbose_name="Año de nacimiento",null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    isbn= models.CharField(max_length=100, primary_key=True)
    title= models.CharField(max_length=100, verbose_name="Titulo")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, verbose_name="Autor")
    year = models.PositiveIntegerField(verbose_name="Año de publicación")
    description=models.TextField(verbose_name="Descripcion")
    category = models.ManyToManyField(Category, verbose_name="Categorías")
    image = models.ImageField(upload_to='books/')

    def __str__(self):
        return self.title

class Prestamo(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    date_prestamo = models.DateField(auto_now_add=True, verbose_name="Fecha de prestamo")
    date_devolucion = models.DateField( verbose_name="Fecha de devolución")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Usuario")
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return self.book.title

class editor(models.Model):
    pass


from django.db import models
from django.contrib.auth.models import User

class Trabajador(models.Model):
    rut=models.IntegerField(max_length=8, primary_key=True)
    rol=models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return rol

class User(models.Model):
    rut= models.IntegerField(max_length=8, primary_key=True)
    name= models.CharField(max_length=100, verbose_name="Nombres")
    last_name= models.CharField(max_length=100, verbose_name="Apellidos")
    phone= models.IntegerField(max_length=9,verbose_name="Numero de telefono")
    mail= models.CharField(max_length=100, verbose_name="Correo")
    trabajador= models.ForeignKey(Trabajador,verbose_name="Rol", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return rut

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")

    def __str__(self):
        return self.name

class Author(models.Model):
    name= models.CharField(max_length=100, verbose_name="Nombre")
    date_birth= models.DateField(verbose_name="Año de nacimiento",null=True)

    def __str__(self):
        return self.name

class Editor(models.Model):
    name= models.CharField(max_length=50,verbose_name="Editor")

    def __str__(self):
        return self.name

class Book(models.Model):
    isbn= models.CharField(max_length=100, primary_key=True)
    title= models.CharField(max_length=100, verbose_name="Titulo")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, verbose_name="Autor")
    year = models.PositiveIntegerField(verbose_name="Año de publicación")
    description=models.TextField(verbose_name="Descripcion")
    category = models.ManyToManyField(Category, verbose_name="Categorías")
    estado= models.BooleanField()
    stock= models.IntegerField()
    editor = models.ForeignKey(Editor,verbose_name="Editor", on_delete=models.SET_NULL)
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
        return self.book.user

class Renovacion():
    date_renovacion= models.DateField(auto_now_add=True, verbose_name="Fecha de renovacion")
    date_redevolucion= models.DateField(verbose_name="Fecha de devolucion renovacion")
    day_devolucion= models.BooleanField(default=False)

class Catalogo():
    ejemplares= models.BooleanField(default=False)

class Multa(models.Model):
    atraso= models.BooleanField(default=False)
    monto= models.IntegerField()
    cobro= models.BooleanField(default=False)

class Reportes():
    date_reporte= models.IntegerField()

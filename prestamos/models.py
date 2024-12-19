from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Rol(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('trabajador', 'Trabajador'),
    ]
    rut = models.CharField(max_length=9, primary_key=True, unique=True)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='trabajador', verbose_name="Rol")

    def __str__(self):
        return f"{self.rut} - {self.get_rol_display()}"

class CustomUser(AbstractUser):
    rut = models.CharField(max_length=9, primary_key=True)
    username = models.CharField(max_length=100, verbose_name="Nombres", unique=True)
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    phone = models.CharField(max_length= 15,verbose_name="Número de teléfono")
    mail = models.EmailField(max_length=100, verbose_name='Correo')
    rol = models.ForeignKey(Rol, verbose_name="Rol", on_delete=models.SET_NULL, null=True)

    def clean(self):
        super().clean()
        if not self.phone.isdigit():
            raise ValidationError("El número de teléfono debe contener solo dígitos.")
        if len(self.phone) < 8 or len(self.phone) > 15:
            raise ValidationError("El número de teléfono debe tener entre 8 y 15 dígitos.")
    def __str__(self):
        return self.username

    def is_admin(self):
        return self.rol and self.rol.rol == 'admin'

    def is_trabajador(self):
        return self.rol and self.rol.rol == 'trabajador'

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
    name= models.CharField(max_length=50,verbose_name="Editor",default='Default Editor Name')

    def __str__(self):
        return self.name

class Book(models.Model):
    isbn= models.CharField(max_length=13, unique=True, verbose_name="ISBN",primary_key=True)
    title= models.CharField(max_length=100, verbose_name="Titulo")
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, verbose_name="Autor")
    year = models.PositiveIntegerField(verbose_name="Año de publicación")
    description=models.TextField(verbose_name="Descripcion")
    category = models.ManyToManyField(Category, verbose_name="Categorías")
    estado= models.BooleanField(default=False, verbose_name="Estado (Disponible)")
    stock= models.PositiveIntegerField(default= 0, verbose_name="Stock")
    editor = models.ForeignKey(Editor,verbose_name="Editor",on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='books/')

    def __str__(self):
        return self.title
    def is_available(self):
        return self.estado and self.stock > 0
    def clean(self):
        if self.stock < 0:
            raise ValidationError("El stock no puede ser negativo.")
        return super().clean()

class Prestamo(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    date_prestamo = models.DateField(auto_now_add=True, verbose_name="Fecha de prestamo")
    date_devolucion = models.DateField( verbose_name="Fecha de devolución")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, verbose_name="Usuario")
    devuelto = models.BooleanField(default=False)

    def __str__(self):
       return f"Prestamo de {self.book.title} por {self.user.name}"

class Renovacion(models.Model):
    date_renovacion= models.DateField(auto_now_add=True, verbose_name="Fecha de renovacion")
    date_redevolucion= models.DateField(verbose_name="Fecha de devolucion renovacion")
    day_devolucion= models.BooleanField(default=False)

class Catalogo(models.Model):
    ejemplares= models.BooleanField(default=False)


class Multa(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Usuario")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name="Libro")
    dias_atraso = models.IntegerField(default=0)
    monto= models.IntegerField(default=0)
    cobro= models.BooleanField(default=False)

    def calcular_monto(self):
        return self.dias_atraso * 1000


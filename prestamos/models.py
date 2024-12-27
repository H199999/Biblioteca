from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date
from django.conf import settings
class CustomUser(AbstractUser):
    rut = models.CharField(max_length=9, primary_key=True, unique=True)
    username = models.CharField(max_length=100, verbose_name="Nombres", unique=True)
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    phone = models.CharField(max_length=15, verbose_name="Número de teléfono")
    mail = models.EmailField(max_length=100, verbose_name='Correo')
    rol = models.BooleanField(default=False, verbose_name="Es Administrador") 

    def clean(self):
        super().clean()
        if not self.phone.isdigit():
            raise ValidationError("El número de teléfono debe contener solo dígitos.")
        if len(self.phone) < 8 or len(self.phone) > 15:
            raise ValidationError("El número de teléfono debe tener entre 8 y 15 dígitos.")
        if not self.rut.isdigit() or len(self.rut) != 9:
            raise ValidationError("El RUT debe contener exactamente 9 dígitos numéricos.")

    def __str__(self):
        rol_str = "Administrador" if self.rol else "Trabajador"
        return f"{self.username} ({rol_str})"

    def is_admin(self):
        return self.rol 

    def is_trabajador(self):
        return not self.rol  


class PerfilCliente(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="perfil_cliente",verbose_name="Usuario")
    name = models.CharField(max_length=100, verbose_name="Nombres")
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    phone = models.CharField(max_length=15, verbose_name="Teléfono")
    mail = models.EmailField(verbose_name="Correo Electrónico", unique=True)

    def __str__(self):
        return f"{self.name} {self.last_name} ({self.rut})"

    class Meta:
        verbose_name = "Perfil de Cliente"
        verbose_name_plural = "Perfiles de Clientes"

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
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN", primary_key=True)
    title = models.CharField(max_length=100, unique=True, verbose_name="Título")
    author = models.ForeignKey('Author', on_delete=models.CASCADE, null=False, verbose_name="Autor")
    year = models.PositiveIntegerField(verbose_name="Año de publicación")
    description = models.TextField(verbose_name="Descripción")
    category = models.ManyToManyField('Category', verbose_name="Categoría")
    estado = models.BooleanField(default=False, verbose_name="Estado (Disponible)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    editor = models.ForeignKey('Editor', verbose_name="Editor", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='books/', verbose_name="Imagen")

    def clean(self):
        if self.stock < 1 or self.stock > 20:
            raise ValidationError("El stock debe ser un número entre 1 y 20.")
        current_year = date.today().year
        if self.year < 1000 or self.year > current_year:
            raise ValidationError(f"El año debe estar entre 1000 y {current_year}.")

    def __str__(self):
        return self.title

class Prestamo(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    date_prestamo = models.DateField(auto_now_add=True, verbose_name="Fecha de prestamo")
    date_devolucion = models.DateField( verbose_name="Fecha de devolución")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, verbose_name="Usuario")
    clientes= models.ForeignKey(PerfilCliente, on_delete=models.CASCADE,verbose_name="Cliente")
    devuelto = models.BooleanField(default=False)

    def __str__(self):
       return f"Prestamo de {self.book.title} por {self.user.name}"

class Renovacion(models.Model):
    date_renovacion= models.DateField(auto_now_add=True, verbose_name="Fecha de renovacion")
    date_redevolucion= models.DateField(verbose_name="Fecha de devolucion renovacion")
    day_devolucion= models.BooleanField(default=False)
    prestamo= models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name="renovaciones")
    def __str__(self):
        return f"Renovación del préstamo {self.prestamo} el {self.date_renovacion}"
        
class Multa(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Usuario")
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name="Libro")
    dias_atraso = models.IntegerField(default=0)
    monto= models.IntegerField(default=0)
    cobro= models.BooleanField(default=False)

    def calcular_monto(self):
        return self.dias_atraso * 1000


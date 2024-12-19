from django.contrib.auth import get_user_model
from prestamos.models import Rol

def create_admin_user(sender, **kwargs):
    User = get_user_model()
    admin_rut = 111111111 
    admin_username = "admin"
    admin_email = "admin@biblioteca.com"
    admin_password = "admin123" 

   
    if not User.objects.filter(rut=admin_rut).exists():
        admin_user = User.objects.create_superuser(
            username=admin_username,
            rut=admin_rut,
            mail=admin_email,
            phone=123456789,
            password=admin_password
        )
        Rol.objects.create(rut=admin_user.rut, rol='admin') 
        print("Administrador único creado exitosamente.")

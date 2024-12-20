from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model

def create_admin_user(sender, **kwargs):
    User = get_user_model()
    admin_rut = "111111111"
    admin_username = "admin"
    admin_email = "admin@biblioteca.com"
    admin_password = "admin123"

    if not User.objects.filter(rut=admin_rut).exists():
        User.objects.create_superuser(
            username=admin_username,
            rut=admin_rut,
            mail=admin_email,
            phone="123456789",
            password=admin_password,
            rol=True
        )
        print("Administrador único creado exitosamente.")
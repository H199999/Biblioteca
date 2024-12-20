from django.apps import AppConfig
from django.db.models.signals import post_migrate

class RegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registration'

    def ready(self):
        from registration.signals import create_admin_user 
        post_migrate.connect(create_admin_user, sender=self)  


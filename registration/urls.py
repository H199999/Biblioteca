from django.urls import path
from .views import RegisterView, CustomLoginView, CustomLogoutView

urlpatterns = [
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'), 
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
]
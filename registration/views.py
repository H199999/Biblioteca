from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        return super().form_valid(form)
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

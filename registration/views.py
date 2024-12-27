from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView, DeleteView
from .forms import CustomUserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from prestamos.models import CustomUser  

class RegisterView(UserPassesTestMixin, CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user-list') 

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()

    def form_valid(self, form):
        try:
            user = form.save()
            messages.success(self.request, f"Usuario {user.username} registrado exitosamente.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Ocurrió un error al registrar al usuario: {str(e)}")
            return self.form_invalid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error en {field}: {error}")
        return super().form_invalid(form)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        user = form.get_user()

        if hasattr(user, 'is_admin') and user.is_admin():
            return redirect('home') 
        elif hasattr(user, 'is_trabajador') and user.is_trabajador():
            return redirect('home') 
        else:
            return redirect('home') 
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class UserListView(UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'registration/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return CustomUser.objects.filter(rol=True) 
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()

class UserDeleteView(UserPassesTestMixin, DeleteView):
    model = CustomUser
    template_name = 'registration/user_delete.html'
    success_url = reverse_lazy('user-list')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Usuario eliminado correctamente.")
        return super().delete(request, *args, **kwargs)

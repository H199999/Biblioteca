from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.shortcuts import redirect

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()
    def form_valid(self, form):
        user = form.save(commit=False)  
        user.set_password(form.cleaned_data['password1'])
        user.set_password(form.cleaned_data['password2'])
        rol_seleccionado = form.cleaned_data.get('rol')  
        rol = Rol.objects.create(rut=user.rut, rol=rol_seleccionado)
        user.rol = rol
        user.save()
        return super().form_valid(form)

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
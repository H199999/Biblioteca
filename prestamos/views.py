from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,DeleteView, UpdateView
from django.views.generic.detail import DetailView
from .models import Book,Author, Category, Prestamo, User, Editor,Renovacion, Multa, PerfilCliente
from .forms import BookForm, AuthorForm, PrestamoForm,EditorForm,RenovForm,ClienteForm, BookUpdateForm
from .models import CustomUser
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import redirect

class UsuarioListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'prestamos/usuarios_lista.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        if self.request.user.is_admin():
            return CustomUser.objects.all() 
        else:
            return CustomUser.objects.filter(rol__rol='trabajador') 
class RegistrarUsuarioView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomUser
    template_name = 'prestamos/crear_usuario.html'
    fields = ['username', 'last_name', 'phone', 'mail', 'trabajador']

    def test_func(self):
        return self.request.user.is_admin()


class ClienteListView(LoginRequiredMixin, ListView):
    model = PerfilCliente
    template_name = 'prestamos/cliente_list.html'
    context_object_name = 'clientes'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        for cliente in context['clientes']:
            cliente.prestamos = Prestamo.objects.filter(user=cliente.user)
        
        return context

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = PerfilCliente
    template_name = 'prestamos/cliente_detail.html'
    context_object_name = 'cliente'

class BookListView(LoginRequiredMixin,ListView):
    model= Book
    template_name= 'prestamos/book_list.html'
    context_object_name='books'

class BookCreateView(CreateView):
    model = Book
    template_name = 'prestamos/book_form.html'
    form_class = BookForm
    success_url = reverse_lazy('book')

    def form_invalid(self, form):
        messages.error(self.request, "Hay errores en el formulario. Por favor, corrígelos.")
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_authors'] = not Author.objects.exists()
        context['no_categories'] = not Category.objects.exists()
        context['no_editors'] = not Editor.objects.exists()
        return context

class BookDeleteView(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'prestamos/book_delete.html'
    success_url = reverse_lazy('book')

class BookUpdateView(LoginRequiredMixin,UpdateView):
    model = Book 
    form_class= BookUpdateForm
    template_name = 'prestamos/book_update.html' 
    context_object_name = 'actualizarlibro' 
    success_url = reverse_lazy('book')
    def form_valid(self, form):
        return super().form_valid(form)

class AuthorListView(LoginRequiredMixin,ListView):
    model= Author
    template_name= 'prestamos/author_list.html'
    context_object_name='listaautor'

class AuthorCreateView(LoginRequiredMixin,CreateView):
    model= Author
    template_name= 'prestamos/author_form.html'
    form_class = AuthorForm 
    context_object_name='crearautor'
    success_url= reverse_lazy('list-author')

class AuthorDeleteView(LoginRequiredMixin,DeleteView):
    model = Author
    template_name = 'prestamos/author_delete.html'
    success_url = reverse_lazy('list-author')

class CategoryListView(LoginRequiredMixin,ListView):
    model= Category
    template_name= 'prestamos/category_list.html'
    context_object_name='listacategoria'
    success_url = reverse_lazy('home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listacategoria'] = Category.objects.all()
        return context

class CategoryCreateView(LoginRequiredMixin,CreateView):
    model= Category
    template_name= 'prestamos/category_form.html'
    context_object_name='crearcategoria'
    success_url= reverse_lazy('list-category')
    fields= ['name']

class CategoryDeleteView(LoginRequiredMixin,DeleteView):
    model = Category
    template_name = 'prestamos/category_delete.html'
    success_url = reverse_lazy('list-category')

class PrestamoListView(ListView):
    model= Prestamo
    template_name= 'prestamos/prestamo_list.html'
    context_object_name='listaprestamos'

    def get_queryset(self):
        return Prestamo.objects.all()


from django.db import transaction

class PrestamoCreateView(LoginRequiredMixin, CreateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'prestamos/prestamo_create.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente_form'] = ClienteForm(self.request.POST or None)
        return context

    def form_valid(self, form):
        cliente_form = ClienteForm(self.request.POST)
        if cliente_form.is_valid():
            with transaction.atomic():
                rut = cliente_form.cleaned_data['rut']
                
                # Verificar si el cliente ya existe
                cliente = PerfilCliente.objects.filter(rut=rut).first()

                if not cliente:  # Si el cliente no existe, crearlo
                    user = CustomUser.objects.create(
                        rut=rut,
                        username=cliente_form.cleaned_data['name'],
                        last_name=cliente_form.cleaned_data['last_name'],
                        phone=cliente_form.cleaned_data['phone'],
                        mail=cliente_form.cleaned_data['mail'],
                        rol=False  # O poner el valor que corresponda
                    )
                    cliente = PerfilCliente.objects.create(
                        user=user,
                        name=cliente_form.cleaned_data['name'],
                        last_name=cliente_form.cleaned_data['last_name'],
                        rut=rut,
                        phone=cliente_form.cleaned_data['phone'],
                        mail=cliente_form.cleaned_data['mail']
                    )
                else:
                    # Si el cliente existe, recuperarlo
                    user = cliente.user

                # Asignar el cliente al préstamo
                form.instance.clientes = cliente  # Aquí asociamos el cliente al préstamo
                form.instance.user = self.request.user  # Asignar el usuario actual al préstamo

                # Guardar el préstamo
                return super().form_valid(form)

        return self.form_invalid(form)


class PrestamoDetailView(LoginRequiredMixin,DetailView):
    model = Prestamo
    template_name = 'prestamos/prestamo_detail.html'
    context_object_name = 'detalleprestamo'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prestamo = self.get_object()

        cliente = prestamo.user.perfil_cliente
        context['cliente'] = prestamo.cliente
        context['renovaciones'] = prestamo.renovaciones.all() 

        return context

class EditorListView(ListView):
    model= Editor
    template_name= 'prestamos/ediitor_list.html'
    context_object_name='listaeditor'

class EditorCreateView(LoginRequiredMixin,CreateView):
    model= Editor
    template_name= 'prestamos/editor_form.html'
    context_object_name= 'creareditor'
    success_url=reverse_lazy('list-editor')
    form_class= EditorForm

class EditorDeleteView(LoginRequiredMixin,DeleteView):
    model= Editor
    template_name= 'prestamos/editor_delete.html'
    success_url= reverse_lazy('list-editor')

class RenovCreateView(CreateView):
    model= Renovacion
    template_name= 'prestamos/renov_form.html'
    context_object_name='crearrenov'
    success_url=reverse_lazy('list-prestamos', kwargs={'pk': Category.pk})
    form_class= RenovForm

class CatalogoListView(ListView):
    model = Book
    template_name= 'prestamos/catalogo.html'
    context_object_name='books'

class MultaListView(ListView):
    model = Multa
    template_name = "prestamos/multas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['multas'] = Multa.objects.filter(cobro=False)
        return context

    def post(self, request, multa_id):
        multa = get_object_or_404(Multa, id=multa_id)
        multa.cobro = True
        multa.save()
        return render(request, 'prestamo/multas.html', {'multas': Multa.objects.filter(cobro=False)})

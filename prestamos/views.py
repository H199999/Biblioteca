from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,DeleteView, UpdateView
from django.views.generic.detail import DetailView
from .models import Book,Author, Category, Prestamo, User, Editor,Renovacion, Multa
from .forms import BookForm, AuthorForm, PrestamoForm,EditorForm,RenovForm
from .models import CustomUser
from django.contrib import messages

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
    form_class= BookForm
    template_name = 'prestamos/book_form.html' 
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
        return Prestamo.objects.filter(devuelto=False)

class PrestamoCreateView(LoginRequiredMixin,CreateView):
    model= Prestamo
    template_name= 'prestamos/prestamo_create.html'
    context_object_name='crearprestamo'
    success_url= reverse_lazy('home')
    form_class= PrestamoForm

class PrestamoDetailView(LoginRequiredMixin,DetailView):
    model = Prestamo
    template_name = 'prestamos/prestamo_detail.html'
    context_object_name = 'detalleprestamo'

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

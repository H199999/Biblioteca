from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,DeleteView, UpdateView
from django.views.generic.detail import DetailView
from .models import Book,Author, Category, Prestamo, User, Trabajador, Catalogo, Editor,Renovacion,Reportes, Multa
from .forms import BookForm, AuthorForm, PrestamoForm,EditorForm,RenovForm

class UserView(LoginRequiredMixin,ListView):
    model= User
    context_object_name='users'

class HomeView(LoginRequiredMixin,ListView):
    model= Book
    template_name= 'prestamos/home.html'
    context_object_name='casa'

class BookListView(LoginRequiredMixin,ListView):
    model= Book
    template_name= 'prestamos/book_list.html'
    context_object_name='books'

class BookCreateView(LoginRequiredMixin,CreateView):
    model= Book
    template_name= 'prestamos/book_form.html'
    form_class = BookForm
    context_object_name='crearlibro'
    success_url= reverse_lazy('home')

class BookDeleteView(LoginRequiredMixin,DeleteView):
    model = Book
    template_name = 'prestamos/book_delete.html'
    success_url = reverse_lazy('home')

class BookUpdateView(LoginRequiredMixin,UpdateView):
    model = Book 
    form_class= BookForm
    template_name = 'prestamos/book_form.html' 
    context_object_name = 'actualizarlibro' 
    success_url = reverse_lazy('home')
    
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
    success_url= reverse_lazy('home')

class AuthorDeleteView(LoginRequiredMixin,DeleteView):
    model = Author
    template_name = 'prestamos/author_delete.html'
    success_url = reverse_lazy('home')

class CategoryListView(LoginRequiredMixin,ListView):
    model= Category
    template_name= 'prestamos/category_list.html'
    context_object_name='listacategoria'

class CategoryCreateView(LoginRequiredMixin,CreateView):
    model= Category
    template_name= 'prestamos/category_form.html'
    context_object_name='crearcategoria'
    success_url= reverse_lazy('home')
    fields= ['name']

class CategoryDeleteView(LoginRequiredMixin,DeleteView):
    model = Category
    template_name = 'prestamos/category_delete.html'
    success_url = reverse_lazy('home')

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
    context_object_name='listaprestamos'

class EditorCreateView(LoginRequiredMixin,CreateView):
    model= Editor
    template_name= 'prestamos/editor_form.html'
    context_object_name= 'creareditor'
    success_url=reverse_lazy('listaeditor')
    form_class= EditorForm

class EditorDeleteView(LoginRequiredMixin,DeleteView):
    model= Editor
    template_name= 'prestamos/editor_delete.html'
    success_url= reverse_lazy('listaeditor')

class RenovCreateView(CreateView):
    model= Renovacion
    template_name= 'prestamos/renov_form.html'
    context_object_name='crearrenov'
    success_url=reverse_lazy('listaprestamos')
    form_class= RenovForm
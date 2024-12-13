from django.urls import path
from django.contrib.auth.views import LoginView
from .views import BookListView,BookCreateView,BookDeleteView,BookUpdateView,AuthorCreateView,AuthorDeleteView,CategoryCreateView, CategoryDeleteView,PrestamoCreateView,PrestamoListView,PrestamoDetailView,HomeView,AuthorListView, CategoryListView,RenovCreateView

urlpatterns = [
    path('', BookListView.as_view(), name='home'),
    path('home',HomeView.as_view(),name='accesos'),
    path('Book/', BookCreateView.as_view(), name='create-book'),
    path('deleteBook/<int:pk>/', BookDeleteView.as_view(), name='delete-book'),
    path('updateBook/<int:pk>/', BookUpdateView.as_view(), name='update-book'),
    path('Author/', AuthorCreateView.as_view(), name='create-author'),
    path('deleteAuthor/<int:pk>/', AuthorDeleteView.as_view(), name='delete-author'),
    path('listAuthor/', AuthorListView.as_view(), name='list-author'),
    path('Category/', CategoryCreateView.as_view(), name='create-category'),
    path('deleteCategory/<int:pk>/', CategoryDeleteView.as_view(), name='delete-category'),
    path('listCategory/<int:pk>/', CategoryListView.as_view(), name='list-category'),
    path('prestamo/<int:pk>/', PrestamoCreateView.as_view(), name='create-prestamo'),
    path('listPrestamo/', PrestamoListView.as_view(), name='list-prestamo'),
    path('detailPrestamo/<int:pk>/', PrestamoDetailView.as_view(), name='prestamo-detail'),
    path('renovacion/<int:pk>/', RenovCreateView.as_view(), name='create-renovacion'),
]

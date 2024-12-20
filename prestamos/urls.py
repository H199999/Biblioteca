from django.urls import path
from django.contrib.auth.views import LoginView
from .views import BookListView,BookCreateView,BookDeleteView,BookUpdateView,AuthorCreateView,AuthorDeleteView,CategoryCreateView,CategoryListView,CategoryDeleteView,PrestamoCreateView,PrestamoListView,PrestamoDetailView,CatalogoListView,AuthorListView,RenovCreateView,EditorListView,EditorCreateView,EditorDeleteView,MultaListView
from registration.views import UserDeleteView,UserListView
urlpatterns = [
    path('', CatalogoListView.as_view(), name='home'),
    path('listBook', BookListView.as_view(), name='book'),
    path('book/', BookCreateView.as_view(), name='create-book'),
    path('deleteBook/<int:pk>/', BookDeleteView.as_view(), name='delete-book'),
    path('updateBook/<int:pk>/', BookUpdateView.as_view(), name='update-book'),
    path('listAuthor/', AuthorListView.as_view(), name='list-author'),
    path('author/', AuthorCreateView.as_view(), name='create-author'),
    path('deleteAuthor/<int:pk>/', AuthorDeleteView.as_view(), name='delete-author'),
    path('listCategory//', CategoryListView.as_view(), name='list-category'),
    path('category/', CategoryCreateView.as_view(), name='create-category'),
    path('deleteCategory/<int:pk>/', CategoryDeleteView.as_view(), name='delete-category'),
    path('listPrestamo/', PrestamoListView.as_view(), name='list-prestamo'),
    path('prestamo/<int:pk>/', PrestamoCreateView.as_view(), name='create-prestamo'),
    path('detailPrestamo/<int:pk>/', PrestamoDetailView.as_view(), name='prestamo-detail'),
    path('renovacion/<int:pk>/', RenovCreateView.as_view(), name='create-renovacion'),
    path('listEditor/', EditorListView.as_view(), name='list-editor'),
    path('editor/', EditorCreateView.as_view(), name='create-editor'),
    path('deleteEditor/<int:pk>/', EditorDeleteView.as_view(), name='delete-editor'),
    path('multas/',MultaListView.as_view(), name='list-multas'),
    path('usuarios/', UserListView.as_view(), name='user-list'),
    path('usuarios/eliminar/<pk>/', UserDeleteView.as_view(), name='user-delete')
]

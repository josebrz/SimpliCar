from django.urls import path
from . import views

urlpatterns = [
    # Library
    path('library', views.library_list_create_view, name='library-list-create'),
    path('library/<int:pk>', views.library_detail_view, name='library-detail'),
    path('library/<int:pk>/books/<int:book_pk>', views.library_book_detail_view, name='library-book-list'),
    # Login/Register
    path('auth/login', views.login_view, name="auth-login"),
    path('auth/register/', views.register_users, name="auth-register"),
    # Book
    path('book', views.book_list_create_view, name="book-list-create"),
    path('book/<int:pk>', views.book_detail_view, name="book-detail"),
    path('book/search', views.book_search_view, name="book-search"),
    # Author
    # path('author', views, name="book-author-list-create"),
    # path('author/<int:pk>', views, name="book-author-detail"),
    # Lead
    path('lead', views.lead_list_create_view, name='lead-list-create')
]


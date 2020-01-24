from django.urls import include, path
from . import views

# URL Patterns - the first parameter is the pattern, the second is the method you're calling inside of your view
# Third is the name of the pattern/function.

urlpatterns = [
    path('', views.home, name='science'),                            # home page
    path('Collection/', views.list, name='listBooks'),              # index of books
    path('AddToCollection/', views.add_book, name='createBook'),     # add new book
    path('Collection/<int:pk>/Details/', views.details_book, name='bookDetails'),    # get details for a single book
    path('Collection/<int:pk>/Edit/', views.edit_book, name='editBook'),             # edit page for a single book
    path('Collection/<int:pk>/Delete/', views.delete_book, name='deleteBook'),       # delete entry
    path('ApiService/', views.api_response, name='booksApi'),                        # API service page
    path('ApiService/addAPI', views.add_api_book, name='addApi'),  # API service page
    path('GoogleNews/', views.google_news, name='GoogleNews'),                       # data scraped news from Google

]
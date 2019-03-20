from django.urls import path

from . import views
#from views import BookList

app_name = 'novel'
urlpatterns = [
    path('', views.BookList.as_view(), name='index'),
    path('book/<int:pk>/', views.ChapterList.as_view(), name='book_detail'),
    path('chapter/<int:pk>/',
         views.ChapterDetail.as_view(), name='chapter_detail'),
    path('shelf/', views.shelf, name='shelf'),
    path('<int:book_id>/<slug:slug>/', views.add_to_favorate, name='favorate'),
    path('book/create/', views.CreateBook.as_view(), name='book_create'),
    path('author/create/', views.AuthorCreatePopup, name='AuthorCreate'),
    path('author/edit/', views.AuthorEditPopup, name='AuthorEdit'),
    path('author/get_author_id', views.get_author_id, name='get_author_id'),
    path('category/create/', views.CategoryCreatePopup, name='CategoryCreate'),
    path('chapter/create/<int:pk>/',
         views.CreateChapter.as_view(), name='chapter_create'),
]

from django.urls import path

from . import views
#from views import BookList


urlpatterns = [
    path('', views.BookList.as_view(), name='index'),
    path('book/<int:pk>/', views.ChapterList.as_view(), name='book_detail'),
    path('chapter/<int:pk>/',
         views.ChapterDetail.as_view(), name='chapter_detail'),
]

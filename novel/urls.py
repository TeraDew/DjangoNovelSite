from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('chapter/<int:chapter_id>/',
         views.chapter_detail_view, name='chapter_detail'),
]

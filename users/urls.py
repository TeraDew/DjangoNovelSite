from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('shelf/', views.shelf, name='shelf'),
    path('<int:book_id>/<slug:slug>/',views.add_to_favorate,name='favorate')
]

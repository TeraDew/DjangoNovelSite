from django.contrib import admin
from novel.models import Category, Tag, Author, Chapter, Book


# Register your models here.
myModels=[Category, Tag, Author, Chapter, Book]
admin.site.register(myModels)
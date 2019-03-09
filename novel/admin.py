from django.contrib import admin
from novel.models import Category, Tag, Author, Chapter, Book


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category']


class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'book', 'excerpt', 'created_time']


myModels = [Category, Tag, Author]
admin.site.register(myModels)
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)

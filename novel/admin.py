from django.contrib import admin
from novel.models import Category, Tag, Author, Chapter, Book


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'show_authors']

    def show_authors(self, obj):
        return '\t'.join([a.name for a in obj.authors.all()])


class ChapterAdmin(admin.ModelAdmin):
    list_display = ['chapter_idx','title', 'book', 'excerpt', 'created_time','modified_time']


myModels = [Category, Tag, Author]
admin.site.register(myModels)
admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)

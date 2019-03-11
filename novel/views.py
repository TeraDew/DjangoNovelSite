from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Book, Chapter
import markdown


# Create your views here.
def index(request):
    book_list = Book.objects.all()
    return render(request, 'novel/index.html', context={
        'book_list': book_list
    })


def book_detail_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    chapters =Chapter.objects.filter(book=book)
    return render(request, 'novel/book_detail.html', context={
        'book': book,
        'chapters': chapters
    })


def chapter_detail_view(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    chapter.body = markdown.markdown(chapter.body, extensions=[
                                     'markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc', ])

    return render(request, 'novel/chapter_detail.html', context={
        'chapter': chapter,
    })

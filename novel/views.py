from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView
from .models import Book, Chapter
import markdown


# Create your views here.
def index(request):
    book_list = Book.objects.all()
    page_name = 'Home'
    return render(request, 'novel/index.html', context={
        'book_list': book_list,
        'page_name': page_name
    })


def book_detail_view(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    chapters = Chapter.objects.filter(book=book)
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


class BookList(ListView):
    model = Book
    template_name = 'novel/index.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        context['page_name'] = 'Home'
        return context


class ChapterList(ListView):
    template_name = 'novel/book_detail.html'
    context_object_name = 'ChapterList'

    def get_queryset(self):
        self.book = get_object_or_404(Book, pk=self.kwargs['pk'])
        return Chapter.objects.filter(book=self.book)

    def get_context_data(self, **kwargs):
        context = super(ChapterList, self).get_context_data(**kwargs)
        context['book'] = self.book
        return context


class ChapterDetail(DetailView):
    template_name = 'novel/chapter_detail.html'
    model = Chapter
    context_object_name = 'chapter'

    def get_context_data(self, **kwargs):
        context = super(ChapterDetail, self).get_context_data(**kwargs)
        context['object'].body = markdown.markdown(context['object'].body, extensions=[
            'markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc', ])
        return context

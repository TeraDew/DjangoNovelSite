# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView
from .models import Book, Chapter
from users.models import History
from django.utils import timezone
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


def str_to_html(str):
    line = ''
    for l in str.split('\n'):
        l = '<p>'+l+'</p>'
        line += l
    return line


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
        # context['body'] = markdown.markdown(context['object'].body, extensions=[
        #    'markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc', ])
        context['body'] = str_to_html(context['object'].body)

        context['chapter_prev'] = Chapter.objects.filter(
            book=context['object'].book, chapter_idx__lt=context['object'].chapter_idx).order_by('-chapter_idx').first()
        context['chapter_next'] = Chapter.objects.filter(
            book=context['object'].book, chapter_idx__gt=context['object'].chapter_idx).order_by('chapter_idx').first()
        
        if self.request.user.is_authenticated:
            present_chapter = context['chapter']
            History.objects.update_or_create(read_chapter=present_chapter, user=self.request.user, defaults={
                'read_time': timezone.now()})
            # Using update_or_create instead of get_or_create will increase TTFB from 60ms to 180ms
            #  when viewing page that have been read, but will update the reading time every time you view the page

            '''
            if History.objects.filter(read_chapter=present_chapter).exists():
                h = History.objects.get(
                    read_chapter=present_chapter, user=self.request.user)
                h.read_time = timezone.now()
                h.save()
            else:
                History.objects.create(
                    user=self.request.user, read_chapter=present_chapter, read_time=timezone.now())
                '''
        return context


class HistoryView(ListView):
    template_name = 'my_history.html'
    # model=History
    context_object_name = 'history_list'

    class Meta:
        ordering = ['-pk']

    def get_queryset(self):
        return History.objects.filter(user=self.request.user).order_by('-read_time')

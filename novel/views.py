# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, get_list_or_404, HttpResponseRedirect, Http404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Book, Chapter, History
from django.utils import timezone
from django.urls import reverse
import markdown
from .forms import BookForm, AuthorForm, CategoryForm
from django.views.decorators.csrf import csrf_exempt


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


@login_required(login_url='login')
def shelf(request):
    book_list = Book.objects.filter(favorated_user=request.user)
    page_name = 'My Shelf'
    return render(request, 'novel/index.html', context={
        'book_list': book_list,
        'page_name': page_name,
    })


@login_required(login_url='login')
def add_to_favorate(request, book_id, slug):
    book = Book.objects.get(pk=book_id)
    if (slug == 'add'):
        # request.user.favorates.add(book)
        book.favorated_user.add(request.user)
        return HttpResponseRedirect(reverse('novel:book_detail', args=(book_id,)))
    elif(slug == 'remove'):
        # request.user.favorates.remove(book)
        # Favorate.objects.get(user=request.user).favorate.remove(book)
        book.favorated_user.remove(request.user)
        return HttpResponseRedirect(reverse('novel:book_detail', args=(book_id,)))
    else:
        raise Http404("Request Error")


@login_required(login_url='login')
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(reverse('novel:book_detail', args=(instance.pk,)))
    else:
        form = BookForm()

    return render(request, 'novel/create_book.html', context={'form': form})


def AuthorCreatePopup(request):
    form = AuthorForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_author");</script>' % (instance.pk, instance))

    return render(request, "novel/add_form.html", {'form': form, 'model': 'Author'})


def AuthorEditPopup(request, pk=None):
    instance = get_object_or_404(Author, pk=pk)
    form = AuthorForm(request.POST or None, instance=instance)

    if form.is_valid():
        instance = form.save()
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_author");</script>' % (instance.pk, instance))

    return render(request, "novel/add_form.html", {'form': form})


@csrf_exempt
def get_author_id(request):
    if request.is_ajax():
        author_name = request.GET['author_name']
        author_id = Author.objects.get(name=author_name).id
        data = {'author_id': author_id, }
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")


def CategoryCreatePopup(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))

    return render(request, "novel/add_form.html", {'form': form, 'model': 'Category'})

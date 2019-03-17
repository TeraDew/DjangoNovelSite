from novel.models import Book, Author, Category
from django import forms


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'cover', 'authors', 'intro', 'category']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['cover'].widget.attrs.update(
            {'class': 'form-control-file'})
        self.fields['authors'].widget.attrs.update({'class': 'form-control'})
        self.fields['intro'].widget.attrs.update({'class': 'form-control'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

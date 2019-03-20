from django.db import models
from users.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    uploader = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='img', blank=True)
    intro = models.CharField(max_length=800)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    favorated_user = models.ManyToManyField(
        User, blank=True, null=True, related_name='favorate')
    authors = models.ManyToManyField(Author, blank=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.title


class Chapter(models.Model):
    chapter_idx = models.IntegerField()
    title = models.CharField(max_length=100)
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField(blank=True, null=True)
    excerpt = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, blank=True)
    read_time = models.DateTimeField()

    def __str__(self):
        return self.read_chapter.title

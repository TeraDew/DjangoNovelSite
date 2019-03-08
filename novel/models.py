from django.db import models

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

class Chapter(models.Model):
    title = models.CharField(max_length=100)
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.title

class Book(models.Model):
    title = models.CharField(max_length=100)
    intro = models.CharField(max_length=200)
    chapters = models.ManyToManyField(Chapter, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
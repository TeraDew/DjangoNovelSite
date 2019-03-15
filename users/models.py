from django.db import models
from django.contrib.auth.models import AbstractUser
from novel.models import Book, Chapter

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    favorates = models.ManyToManyField(Book, blank=True)

    class Meta(AbstractUser.Meta):
        pass


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_chapter = models.OneToOneField(
        Chapter, on_delete=models.CASCADE, blank=True)
    read_time = models.DateTimeField()

    def __str__(self):
        return self.read_chapter.title

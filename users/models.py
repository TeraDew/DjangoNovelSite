from django.db import models
from django.contrib.auth.models import AbstractUser
from novel.models import Book

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    favorates = models.ManyToManyField(Book, blank=True)

    class Meta(AbstractUser.Meta):
        pass

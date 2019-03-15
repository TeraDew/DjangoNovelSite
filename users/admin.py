from django.contrib import admin
from .models import History, User

# Register your models here.


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['read_chapter', 'user', 'read_time']


admin.site.register(History, HistoryAdmin)

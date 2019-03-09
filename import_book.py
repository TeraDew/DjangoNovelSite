# -*- coding: UTF-8 -*-
import re
from novel.models import Chapter, Book
from django.utils import timezone
from django.shortcuts import get_object_or_404
temp_body = ''
temp_title = ''

book_obj = get_object_or_404(Book, title='红楼梦')

with open(u'红楼梦.txt', 'r', encoding='UTF-8') as f:
    for temp_line in f:
        if re.match(r'^第.*?回.*?$', temp_line):
            if temp_title == '':
                temp_title = temp_line
            else:
                #print('title' + temp_title)
                #print('body' + body)

                chapter = Chapter(book=book_obj, title=temp_title, created_time=timezone.now(
                ), modified_time=timezone.now(), body=temp_body)
                chapter.save()
                temp_body = ''
                temp_title = temp_line
        else:
            temp_body = temp_body+temp_line
    # read to the last line

chapter = Chapter(book=book_obj, title=temp_title, created_time=timezone.now(
), modified_time=timezone.now(), body=temp_body)
chapter.save()

# -*- coding: UTF-8 -*-
import re
from novel.models import Chapter, Book, Author, Category
from django.utils import timezone
from django.shortcuts import get_object_or_404


temp_body = ''
temp_title = ''

book_title = u'红楼梦'
author_list = [u'曹雪芹', u'高鹗']
intro = u'真事隐去，假语存焉'
category_name = u'言情'
file_name = u'红楼梦.txt'
# authors=Author.objects.none()


category, created = Category.objects.get_or_create(name=category_name)

book_obj, created = Book.objects.get_or_create(title=book_title, defaults={
                                               'intro': intro, 'category': category})
old_author_set = book_obj.authors.all()
deleted_author = old_author_set.difference(
    Author.objects.filter(name__in=author_list))

for author in author_list:
    author_obj, created = Author.objects.get_or_create(name=author)
    book_obj.authors.add(author_obj)

book_obj.authors.remove(*deleted_author)

chapter_number = len(Chapter.objects.filter(book=book_obj))
chapter_number += 1

with open(file_name, 'rt', encoding='UTF-8') as f:
    for temp_line in f:
        if re.match(r'^第[一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾百千万零]+回.*?$', temp_line):
            if temp_title == '':
                temp_title = temp_line
            else:
                #print('title' + temp_title)
                #print('body' + body)

                chapter = Chapter.objects.create(chapter_idx=chapter_number, book=book_obj, title=temp_title, created_time=timezone.now(
                ), modified_time=timezone.now(), body=temp_body)
                temp_body = ''
                temp_title = temp_line
        else:
            temp_body += temp_line

        chapter_number += 1
    # read to the last line

chapter = Chapter.objects.create(book=book_obj, title=temp_title, created_time=timezone.now(
), modified_time=timezone.now(), body=temp_body)

#from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    title = models.CharField('Title', max_length=100)
    #text = RichTextUploadingField('Text')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Category')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.category} :: {self.title}'


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1600)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    approved = models.BooleanField('Approved', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.datetime}'

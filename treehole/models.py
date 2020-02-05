from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import exceptions
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse

class Message(models.Model):
    content=RichTextUploadingField()
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    create_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['create_time']

class Defender(models.Model):
    question=models.TextField(max_length=20)
    answer=models.TextField(max_length=20)
    stars=models.IntegerField(default=0)

class Saying(models.Model):
    content=models.CharField(max_length=100)
    author=models.CharField(max_length=20)




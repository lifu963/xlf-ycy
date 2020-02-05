from django.db import models
from django.db.models.fields import exceptions
from django.urls import reverse
import os

def image_path(instance,filename):
    return os.path.join('img','home',filename)

class HomeImage(models.Model):
    stars=models.IntegerField(default=0)
    image=models.ImageField(upload_to=image_path,blank=True,null=True)
    def image_url(self):
        return self.image.url
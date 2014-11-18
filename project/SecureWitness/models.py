from django.db import models
from django.contrib.auth.models import User
import datetime


class Folder(models.Model):
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Bulletin(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today)
    location = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    public = models.BooleanField(default=False)
    folder = models.ForeignKey(Folder, default = 0, on_delete=models.DO_NOTHING)
    author = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Document(models.Model):
    file = models.FileField()
    bulletin = models.ForeignKey(Bulletin, on_delete=models.DO_NOTHING)

class Sharing(models.Model):
    author = models.CharField(max_length=100)
    reader = models.CharField(max_length=100)
    bulletin = models.ForeignKey(Bulletin, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.bulletin+": " + self.author + " to " + self.reader 
# Create your models here.

from django.db import models
from django.contrib.auth.models import User
import datetime


class Folder(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default = 0)
    def __str__(self):
        return self.name

class Bulletin(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today)
    location = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    public = models.BooleanField(default=False)
    folder = models.ForeignKey(Folder, default = 0, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, default = 0, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name

class Document(models.Model):
    file = models.FileField()
    bulletin = models.ForeignKey(Bulletin, on_delete=models.DO_NOTHING)

class Sharing(models.Model):
    author = models.ForeignKey(User, related_name='sharing_author', on_delete=models.DO_NOTHING)
    reader = models.ForeignKey(User, related_name='sharing_reader', on_delete=models.DO_NOTHING)
    bulletin = models.ForeignKey(Bulletin, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.bulletin+": " + self.author + " to " + self.reader 
# Create your models here.

from django.db import models
from django.contrib.auth.models import User
import datetime


def place_document(instance, filename):
    return 'documents/'+instance.user+'/'+str(instance.bulletin.id)+'/'+filename

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
    file = models.FileField(upload_to=place_document)
    bulletin = models.ForeignKey(Bulletin, on_delete=models.DO_NOTHING)
    user = models.CharField(max_length=100)

class Sharing(models.Model):
    author = models.CharField(max_length=100)
    reader = models.CharField(max_length=100)
    bulletin = models.ForeignKey(Bulletin, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.bulletin+": " + self.author + " to " + self.reader


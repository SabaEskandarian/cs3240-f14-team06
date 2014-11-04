from django.db import models
import datetime

#Guessing what we need for now, may change later
class User(models.Model):
    username = models.CharField(max_length=100)
    passHash = models.CharField(max_length=200)
    isAdmin = models.BooleanField(default=False)

#Don't technically need this, may do away with it later
class Folder(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User)

class Bulletin(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today)
    location = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    public = models.BooleanField(default=False)
    folder = models.ForeignKey(Folder, default = 0)
    author = models.ForeignKey(User, default = 0)

class Document(models.Model):
    file = models.FileField()
    bulletin = models.ForeignKey(Bulletin)

class Sharing(models.Model):
    author = models.ForeignKey(User, related_name='sharing_author')
    reader = models.ForeignKey(User, related_name='sharing_reader')
    bulletin = models.ForeignKey(Bulletin)

# Create your models here.
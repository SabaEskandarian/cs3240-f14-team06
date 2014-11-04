from django.shortcuts import render, render_to_response
from SecureWitness import models
from django.views.decorators.http import require_http_methods
from django.forms import ModelForm, BooleanField
from django.http import HttpResponseRedirect

#folders
@require_http_methods(["POST"])
def createFolder(request):
    return

@require_http_methods(["DELETE"])
def deleteFolder(request):

    return

@require_http_methods(["POST"])
def renameFolder(request):
    return

@require_http_methods(["POST"])
def copyFolder(request):
    return

@require_http_methods(["GET"])
def getFolders(request):
    return


#bulletins
@require_http_methods(["POST"])
def createBulletin(request, userId):
    data = request.POST
    #user = models.User.objects.get(pk=userId);
    #user = models.User(username="abc", passHash = "def", isAdmin = False)
    #folder = models.Folder(name = "woo", user = user)
    #folder = models.Folder.objects.get(pk=data['folder']) may change that
    public = False
    if 'public' in data:
        public = True
    bulletin = models.Bulletin(name=data['name'], date=data['date'], location = data['location'], description = data['description'], public = public)#, folder = folder, author = user)#change author/folder later
    bulletin.save()
    bulletins = models.Bulletin.objects.filter(author_id = userId).values() # this bit is a duplicate of the getBulletins code
    #return render_to_response('list_bulletins.html', {'bulletins':bulletins})
    #return showUserHome(userId, request)
    return HttpResponseRedirect('/'+userId+'/')

#@require_http_methods(["DELETE"]) this was causing problems
def deleteBulletin(request, userId, bulletinId):
    bulletin = models.Bulletin.objects.get(pk=bulletinId)
    bulletin.delete()
    return HttpResponseRedirect('/'+userId+'/')

@require_http_methods(["POST"])
def renameBulletin(request, userId, bulletinId):
    bulletin = models.Bulletin.objects.get(pk=bulletinId)
    bulletin.name = request.POST['name']
    bulletin.save()
    return HttpResponseRedirect('/'+userId+'/')

@require_http_methods(["POST"])
def copyBulletin(request, userId, bulletinId):
    bulletin = models.Bulletin.objects.get(pk=bulletinId)
    bulletin.pk=None
    bulletin.name = request.POST['name']
    bulletin.save()
    return HttpResponseRedirect('/'+userId+'/')

@require_http_methods(["GET"])
def getBulletins(request, userId):
    bulletins = models.Bulletin.objects.filter(author_id = userId).values()
    #return render_to_response('list_bulletins.html', {'bulletins':bulletins})
    #return showUserHome(userId, request)
    return HttpResponseRedirect('/'+userId+'/')

@require_http_methods(["GET"])
def getBulletin(request, userId, bulletinId):
    return

#documents
@require_http_methods(["POST"])
def createDocument(request):
    return

@require_http_methods(["DELETE"])
def deleteDocument(request):
    return

@require_http_methods(["GET"])
def getDocuments(request):
    return

#sharing
@require_http_methods(["POST"])
def createSharing(request):
    return

@require_http_methods(["DELETE"])
def deleteSharing(request):
    return

@require_http_methods(["GET"])
def getSharings(request):
    return
# Create your views here.

def homePage(request):
    return render_to_response('index.html')

@require_http_methods(["GET"])
def userPage(request, userId):
    return showUserHome(userId, request)

#the things below are not views... maybe move them out later?

#return the interface page of the user
def showUserHome(userId, request):
    bulletinForm = BulletinForm()
    bulletins = models.Bulletin.objects.filter(author_id = userId).values()
    #return render_to_response('user_home.html', {'bulletinForm': bulletinForm, 'bulletins':bulletins}, )
    return render(request, 'user_home.html', {'userId':userId, 'bulletinForm': bulletinForm, 'bulletins':bulletins})

class BulletinForm(ModelForm):
    public = BooleanField(required=False)
    class Meta:
        model = models.Bulletin
        fields = ['name', 'date', 'location', 'description', 'public']
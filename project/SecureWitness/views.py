from django.shortcuts import render, render_to_response
from SecureWitness import models
from django.views.decorators.http import require_http_methods
from django.forms import ModelForm, BooleanField
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template import RequestContext
from django.shortcuts import render_to_response

#user
@require_http_methods(["POST"])
def login(request, userId):
    username = request.POST['userName']
    password = request.POST['passWord']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            return HttpResponse("Active User")
        else:
            return HttpResponse("Disabled Account")
    else:
        return HttpResponse('Invalid Login')

@require_http_methods(["POST"])
def createUser(request,userId):
    data = request.POST
    user = User.objects.create_user(username=data['userName'], email=data['email'], password=data['passWord'])
    user.save()
    return HttpResponse("User Created!")


#folders
@require_http_methods(["POST"])
def createFolder(request, userId):
    data = request.POST
    folder = models.Folder(name=data['name'])#add user later
    folder.save()
    return HttpResponseRedirect('/'+userId+'/')

@require_http_methods(["DELETE"])
def deleteFolder(request, userId, folderId):
    folder = models.Folder.objects.get(pk=folderId)
    bulletins = models.Bulletin.objects.filter(folder_id = folder.pk)
    for bulletin in bulletins:
        bulletin.delete()
    folder.delete()
    return HttpResponseRedirect('/'+userId+'/')

@require_http_methods(["POST"])
def renameFolder(request, userId, folderId):
    folder = models.Folder.objects.get(pk=folderId)
    folder.name = request.POST['name']
    folder.save()
    return HttpResponseRedirect('/'+userId+'/')

@require_http_methods(["POST"])
def copyFolder(request, userId, folderId):
    folder = models.Folder.objects.get(pk=folderId)
    bulletins = models.Bulletin.objects.filter(folder_id = folder.pk)
    folder.pk = None
    folder.name = request.POST['name']
    folder.save()
    for bulletin in bulletins:
        bulletin.pk = None
        bulletin.folder = folder
        bulletin.save()
    return HttpResponseRedirect('/'+userId+'/')

#bulletins
@require_http_methods(["POST"])
def createBulletin(request, userId):
    data = request.POST
    public = False
    folder_id = 0
    if 'folder' in data:
        folder_id = data['folder']
    if 'public' in data:
        public = True
    bulletin = models.Bulletin(name=data['name'], date=data['date'], location = data['location'], description = data['description'], public = public, folder_id = folder_id)#, author = user)#change author later
    bulletin.save()
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
def setBulletinFolder(request, userId, bulletinId):
    folder_id = request.POST['folder']
    bulletin = models.Bulletin.objects.get(pk=bulletinId)
    bulletin.folder_id=folder_id
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

def homePage(request):
    return render_to_response('index.html')

@require_http_methods(["GET"])
def userPage(request, userId):
    return showUserHome(userId, request)

@require_http_methods(["GET"])
def userFolder(request, userId, folderId):
    return showUserFolder(userId, folderId, request)

#reader search
@require_http_methods(["POST"])
def searchRequest(request, userId):
    return showSearchResults(userId, request.POST['query'], request)

#the things below are not views... maybe move them out later?

#return the interface page of the user
def showUserHome(userId, request):
    bulletinForm = BulletinForm()
    bulletins = models.Bulletin.objects.filter(author_id = userId, folder_id = 0).values()
    folders = models.Folder.objects.filter(user_id = userId).values()
    #return render_to_response('user_home.html', {'bulletinForm': bulletinForm, 'bulletins':bulletins}, )
    return render(request, 'user_home.html', {'userId':userId, 'bulletinForm': bulletinForm, 'bulletins':bulletins, 'folders':folders})

def showUserFolder(userId, folderId, request):
    bulletins = models.Bulletin.objects.filter(author_id = userId, folder_id = folderId).values()
    folder = models.Folder.objects.get(id = folderId)
    folders = models.Folder.objects.filter(user_id = userId).values()
    return render(request, 'folder_bulletins.html', {'userId': userId, 'folder':folder, 'bulletins':bulletins, 'folders':folders})

def showSearchResults(userId, query, request):
    results = models.Bulletin.objects.raw("SELECT DISTINCT * FROM SecureWitness_Bulletin " +
                                            "WHERE (author_id = %s AND (name LIKE %s OR description LIKE %s OR location LIKE %s)) " +
                                            "OR (public = 1 AND (name LIKE %s OR description LIKE %s OR location LIKE %s))", [userId, '%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%'])
    return render(request, 'search_results.html', {'results': results, 'query': query, 'userId': userId})

class BulletinForm(ModelForm):
    public = BooleanField(required=False)
    class Meta:
        model = models.Bulletin
        fields = ['name', 'date', 'location', 'description', 'public']
from django.shortcuts import render, render_to_response
from SecureWitness import models
from django.views.decorators.http import require_http_methods
from django.forms import ModelForm, BooleanField
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.core.servers.basehttp import FileWrapper
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
#user
@require_http_methods(["POST"])
def loginUser(request):
    username = request.POST['userName']
    password = request.POST['passWord']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render(request, 'loggedin.html', {'full_name': username})
        else:
            return HttpResponse("Disabled Account")
    else:
        return render(request,'invalid_login.html')

@require_http_methods(["POST"])
def createUser(request):
    data = request.POST
    try:
        user = User.objects.create_user(username=data['userName'], email=data['email'], password=data['passWord'])
        user.save()
        return HttpResponse("User Created!")
    except:
        return HttpResponse("User already exists!")
  



def disableUser(request, userId):
    request.user.is_active = False
    request.user.save()
    return HttpResponse("You have disabled your account.")

def loggedin(request):
    return render(request,'loggedin.html',
        {'full_name': request.user.username})

def invalid_login(request):
    return render(request,'invalid_login.html')

def logout(request):
    auth.logout(request)
    return render(request,'logout.html')

#folders
@require_http_methods(["POST"])
def createFolder(request, userId):
    data = request.POST
    folder = models.Folder(name=data['name'], user=userId)
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
    bulletin = models.Bulletin(name=data['name'], date=data['date'], location = data['location'], description = data['description'], public = public, folder_id = folder_id, author=userId)
    bulletin.save()
    return HttpResponseRedirect('/'+userId+'/')

#@require_http_methods(["DELETE"]) this was causing problems
def deleteBulletin(request, userId, bulletinId):
    bulletin = models.Bulletin.objects.get(pk=bulletinId)
    documents = models.Document.objects.filter(user=bulletin.author)
    for document in documents:
        document.delete()
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
    bulletins = models.Bulletin.objects.filter(author = userId).values()
    #return render_to_response('list_bulletins.html', {'bulletins':bulletins})
    #return showUserHome(userId, request)
    return HttpResponseRedirect('/'+userId+'/')

#documents
@require_http_methods(["POST"])
def addDocument(request, userId, bulletinId):
    file = request.FILES['doc']
    doc = models.Document(file = file, bulletin_id = bulletinId, user=userId)
    doc.save()
    return HttpResponseRedirect('/'+userId+'/')

@require_http_methods(["GET"])
def getDocument(request, userId, bulletinId, fileName):
    response = HttpResponse(FileWrapper(open('documents/'+userId+'/'+bulletinId+'/'+fileName)), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename='+fileName
    response['X-Sendfile'] = 'documents/'+userId+'/'+bulletinId+'/'+fileName
    return response

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
    return render(request,'index.html')

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
    bulletins = models.Bulletin.objects.filter(author = userId, folder_id = 0).values()
    folders = models.Folder.objects.filter(user = userId).values()
    docs = models.Document.objects.filter(user = userId).values()
    #return render_to_response('user_home.html', {'bulletinForm': bulletinForm, 'bulletins':bulletins}, )
    return render(request, 'user_home.html', {'userId':userId, 'bulletinForm': bulletinForm, 'bulletins':bulletins, 'folders':folders, 'documents':docs})

def showUserFolder(userId, folderId, request):
    bulletins = models.Bulletin.objects.filter(author = userId, folder_id = folderId).values()
    folder = models.Folder.objects.get(id = folderId)
    folders = models.Folder.objects.filter(user = userId).values()
    docs = models.Document.objects.filter(user = userId).values()
    return render(request, 'folder_bulletins.html', {'userId': userId, 'folder':folder, 'bulletins':bulletins, 'folders':folders, 'documents':docs})

def showSearchResults(userId, query, request):
    results = models.Bulletin.objects.raw("SELECT DISTINCT * FROM SecureWitness_Bulletin " +
                                            "WHERE (author = %s AND (name LIKE %s OR description LIKE %s OR location LIKE %s)) " +
                                            "OR (public = 1 AND (name LIKE %s OR description LIKE %s OR location LIKE %s))", [userId, '%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%', '%'+query+'%'])
    return render(request, 'search_results.html', {'results': results, 'query': query, 'userId': userId})

class BulletinForm(ModelForm):
    public = BooleanField(required=False)
    class Meta:
        model = models.Bulletin
        fields = ['name', 'date', 'location', 'description', 'public']

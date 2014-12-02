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
from django.contrib.auth.decorators import login_required
from subprocess import call
import encryption

#user
@require_http_methods(["POST"])
def loginUser(request):
    username = request.POST['userName']
    password = request.POST['passWord']
    user = authenticate(username=username, password=password)
    if request.user.is_authenticated():
        return render(request, 'already_logged_in.html', {'user_name': request.user.username})
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/'+username+'/')
        else:
            return render(request, 'disabled_account.html')
    else:
        return render(request,'invalid_login.html')

@require_http_methods(["POST"])
def createUser(request):
    data = request.POST
    try:
        user = User.objects.create_user(username=data['userName'], email=data['email'], password=data['passWord'])
        user.save()
        return render(request, 'user_created.html')
    except:
        return render(request, 'invalid_user_creation.html')

def disableUser(request, userId):
    request.user.is_active = False
    request.user.save()
    return render(request, 'disabled_account.html')

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
    #return showUserHome(userId, request)

#@require_http_methods(["DELETE"])
def deleteFolder(request, userId, folderId):
    folder = models.Folder.objects.get(pk=folderId)
    bulletins = models.Bulletin.objects.filter(folder_id = folder.pk)
    for bulletin in bulletins:
        bulletin.delete()
    folder.delete()
    return HttpResponseRedirect('/'+userId+'/')
    #return showUserHome(userId, request)

@require_http_methods(["POST"])
def renameFolder(request, userId, folderId):
    folder = models.Folder.objects.get(pk=folderId)
    folder.name = request.POST['name']
    folder.save()
    return HttpResponseRedirect('/'+userId+'/')
    #return showUserHome(userId, request)

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
    #return showUserHome(userId, request)

#bulletins
@login_required(login_url='/index')
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
    #return showUserHome(userId, request)

#@require_http_methods(["DELETE"]) this was causing problems
def deleteBulletin(request, userId, bulletinId):
    bulletin = models.Bulletin.objects.get(pk=bulletinId)
    documents = models.Document.objects.filter(user=bulletin.author)
    for document in documents:
        document.file.delete()
        document.delete()
    bulletin.delete()
    return HttpResponseRedirect('/'+userId+'/')


@require_http_methods(["POST"])
def renameBulletin(request, userId, bulletinId):
    bulletin = models.Bulletin.objects.get(pk=bulletinId)
    bulletin.name = request.POST['name']
    bulletin.save()
    return HttpResponseRedirect('/'+userId+'/')
    #return showUserHome(userId, request)

@require_http_methods(["POST"])
def editBulletin(request, userId, bulletinId):
    data = request.POST
    #only make a change if a new value is given
    bulletin = models.Bulletin.objects.get(pk=bulletinId)
    if(data["date"] and data["date"] != ""):
        bulletin.date = data["date"]
    if(data["location"] and data["location"] != ""):
        bulletin.location = data["location"]
    if 'public' in data:
        bulletin.public = True
    if(data["description"] and data["description"] != ""):
        bulletin.description = data["description"]
    if(data["name"] and data["name"] != ""):
        bulletin.name = data["name"]
    bulletin.save()
    return HttpResponseRedirect('/'+userId+'/')
    #return showUserHome(userId, request)

@require_http_methods(["POST"])
def setBulletinFolder(request, userId, bulletinId):
    folder_id = request.POST['folder']
    bulletin = models.Bulletin.objects.get(pk=bulletinId)
    bulletin.folder_id=folder_id
    bulletin.save()
    return HttpResponseRedirect('/'+userId+'/')
    #return showUserHome(userId, request)

@require_http_methods(["POST"])
def copyBulletin(request, userId, bulletinId):
    bulletin = models.Bulletin.objects.get(pk=bulletinId)
    bulletin.pk=None
    bulletin.name = request.POST['name']
    bulletin.save()
    return HttpResponseRedirect('/'+userId+'/')
    #return showUserHome(userId, request)

@require_http_methods(["GET"])
def getBulletins(request, userId):
    bulletins = models.Bulletin.objects.filter(author = userId).values()
    #return render_to_response('list_bulletins.html', {'bulletins':bulletins})
    return HttpResponseRedirect('/'+userId+'/')
    #return showUserHome(userId, request)

#documents
@require_http_methods(["POST"])
def addDocument(request, userId, bulletinId):
    file = request.FILES['doc']
    doc = models.Document(file = file, bulletin_id = bulletinId, user=userId)
    doc.save()
    if models.Bulletin.objects.get(pk=bulletinId).public == False:
        call(["touch", "outfile"]) 
        prevURL = doc.file.url
        unencrypted = open(doc.file.url, 'r+')
        encryption.encrypt(unencrypted, open("outfile", 'r+'), str(userId) + str(bulletinId) + str(doc.file.url))
        call(["rm", "-rf", prevURL])
        call(["mv", "outfile", prevURL])
    #return HttpResponseRedirect('/'+userId+'/')
    return showUserHome(userId, request)

@require_http_methods(["GET"])
def getDocument(request, userId, bulletinId, fileName):
    if models.Bulletin.objects.get(pk=bulletinId).public == False:
        call(["touch", "outfile"])
        out = open('outfile', 'r+')
        encrypted = open('documents/'+userId+'/'+bulletinId+'/'+fileName, 'r+')
        encryption.decrypt(encrypted, out, str(userId) + str(bulletinId) + str('documents/'+userId+'/'+bulletinId+'/'+fileName))
        out.close()
        response = HttpResponse(FileWrapper(open('outfile', 'r+')), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+fileName
        response['X-Sendfile'] = 'documents/'+userId+'/'+bulletinId+'/'+fileName
        call(['rm', '-rf', 'outfile'])
    else:
        response = HttpResponse(FileWrapper(open('documents/'+userId+'/'+bulletinId+'/'+fileName)), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+fileName
        response['X-Sendfile'] = 'documents/'+userId+'/'+bulletinId+'/'+fileName
    return response

def deleteDocument(request, userId, bulletinId, fileName):
    document = models.Document.objects.get(user = userId, bulletin_id = bulletinId, file = 'documents/'+userId+'/'+bulletinId+'/'+fileName)
    document.file.delete()
    document.delete()
    return HttpResponseRedirect('/'+userId+'/')
    #return showUserHome(userId, request)

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

@require_http_methods(["GET"])
def userEdit(request, userId, bulletinId):
    return showEdit(userId, bulletinId, request)

#reader search
@require_http_methods(["POST"])
def searchRequest(request, userId):
    return showSearchResults(userId, request.POST['query'], request)

#the things below are not views... maybe move them out later?

#return the interface page of the user
def showUserHome(userId, request):
    if request.user.username != userId:
        return render(request, 'not_allowed.html', {'userId': request.user.username})
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

def showEdit(userId, bulletinId, request):
    bulletinForm = BulletinForm()
    bulletin = models.Bulletin.objects.get(id=bulletinId)
    return render(request, 'edit_bulletin.html', {'bulletinForm': bulletinForm, 'userId': userId, 'bulletin':bulletin})

class BulletinForm(ModelForm):
    public = BooleanField(required=False)
    class Meta:
        model = models.Bulletin
        fields = ['name', 'date', 'location', 'description', 'public']

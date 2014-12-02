from django.contrib import admin
from SecureWitness.models import Folder 
from SecureWitness.models import Document
from SecureWitness.models import Bulletin
from SecureWitness.models import Sharing

class FolderAdmin(admin.ModelAdmin):
	fields=['user','name']

class BulletinAdmin(admin.ModelAdmin):
	fields=['name','date','location','description','public','folder','author']

# Register your models here.
admin.site.register(Folder, FolderAdmin)
admin.site.register(Bulletin,BulletinAdmin)
admin.site.register(Document)
admin.site.register(Sharing)

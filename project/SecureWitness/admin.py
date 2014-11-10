from django.contrib import admin
from SecureWitness.models import Folder 
from SecureWitness.models import Document
from SecureWitness.models import Bulletin
from SecureWitness.models import Sharing

class BulletinInline(admin.StackedInline):
	model = Bulletin
	extra = 3

class FolderAdmin(admin.ModelAdmin):
	fields=['user','name']
	inlines = [BulletinInline]

class BulletinAdmin(admin.ModelAdmin):
	fields=['name','date']

# Register your models here.
admin.site.register(Folder, FolderAdmin)
admin.site.register(Bulletin,BulletinAdmin)
admin.site.register(Document)
admin.site.register(Sharing)
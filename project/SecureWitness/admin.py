from django.contrib import admin
from SecureWitness.models import Folder 
from SecureWitness.models import Document
from SecureWitness.models import Bulletin
from SecureWitness.models import Sharing

# Register your models here.
admin.site.register(Folder)
admin.site.register(Bulletin)
admin.site.register(Document)
admin.site.register(Sharing)
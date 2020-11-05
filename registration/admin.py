from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Usuario, TipoUsuario, Pais

# Register your models here.

admin.site.register(Usuario)
admin.site.register(Permission)
admin.site.register(ContentType)
admin.site.register(TipoUsuario)
admin.site.register(Pais)
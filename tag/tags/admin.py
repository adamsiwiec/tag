from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Tag)
admin.site.register(Friendship)
admin.site.register(LoginUser)
admin.site.register(Extra)
admin.site.register(Credits)

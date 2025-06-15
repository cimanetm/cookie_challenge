from django.contrib import admin
from .models import *
 
admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(Vote)
admin.site.register(Result)

from django.contrib import admin
from user_profile.models import *

class UserProfileAdmin(admin.ModelAdmin):

    list_display = ('user',)
    search_fields = ['user']
    list_filter = ('user',)

admin.site.register(UserProfile, UserProfileAdmin)
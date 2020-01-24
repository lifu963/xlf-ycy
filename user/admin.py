from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class Profileinline(admin.StackedInline):
    model = Profile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (Profileinline,)
    list_display = ('username','email','is_staff','is_active','is_superuser','nickname')

    def nickname(self,obj):
        return obj.profile.nickname

    nickname.short_description = '昵称'

admin.site.unregister(User)
admin.site.register(User,UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','nickname')


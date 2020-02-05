from django.contrib import admin
from .models import HomeImage
# Register your models here.

@admin.register(HomeImage)
class homeImageAdmin(admin.ModelAdmin):
    list_display = ('id','stars','image')

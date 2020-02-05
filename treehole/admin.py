from django.contrib import admin
from .models import Message,Defender,Saying
# Register your models here.

@admin.register(Message)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('id','content','author','create_time')

@admin.register(Defender)
class DefenderAdmin(admin.ModelAdmin):
    list_display = ('question','answer','stars')

@admin.register(Saying)
class SayingAdmin(admin.ModelAdmin):
    list_display = ('content','author')
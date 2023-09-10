from django.contrib import admin
from django.urls import path
from .models import PhotoContent
from django.shortcuts import render


# Register your models here.

class PhotoContentChange(admin.ModelAdmin):
    change_list_template = 'admin_panel/index.html'


admin.site.register(PhotoContent, PhotoContentChange)

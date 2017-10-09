from django.contrib import admin
from .models import Post, Tag, Rating


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id', 'title',]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=['title']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display=['user','shop','score']



# Register your models here.

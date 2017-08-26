from django.contrib import admin
from .models import Post, Tag, Rating, Tag2


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id', 'title', 'score']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=['name']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display=['user','shop','score']


@admin.register(Tag2)
class TagAdmin2(admin.ModelAdmin):
    list_display=['name']

# Register your models here.

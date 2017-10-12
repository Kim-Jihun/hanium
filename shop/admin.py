from django.contrib import admin
from .models import Post, Tag, Rating,Review


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id', 'title',]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=['title']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display=['user','shop','score']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=['post','content','user']



# Register your models here.

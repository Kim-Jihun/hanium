from django.shortcuts import render
from .decorators import bot
from . import functions
from shop.models import Post, Tag, Rating
from django.http import JsonResponse

@bot
def on_init(request):

    return {'type': 'buttons', 'buttons': ['서울대입구', '신촌', '왕십리']}

@bot
def on_message(request):

    user_key = request.JSON['user_key']
    type = request.JSON['type']
    content = request.JSON['content'] # photo 타입일 경우에는 이미지 URL

    if content.startswith('서울대'):
        qs = Post.objects.filter(tag_set__location__icontains='서울대')
        ordered_query = qs.order_by('-score')
        response = ordered_query[0]
    elif content.startswith('신촌'):
        qs = Post.objects.filter(tag_set__location__icontains='신촌')
        ordered_query = qs.order_by('-score')
        response = ordered_query[0]

    elif content.startswith('왕십리'):
        qs = Post.objects.filter(tag_set__location__icontains='왕십리')
        ordered_query = qs.order_by('-score')
        response = ordered_query[0]
    else:
        response='지원하는 답변이 아닙니다.'


    if isinstance(response, str):

        return {
            'message': {
                'text': response
            }
        }
    else:
        return {
            'message': {
                'text': '식당이름:' + response.title,
                'photo': {
			"url": response.image.url,
			"width": 640,
			"height": 480,
		},
            }
        }


@bot
def on_added(request):
    user_key = request.JSON['user_key']

@bot
def on_block(request, user_key):
    pass

@bot
def on_leave(request, user_key):
    pass

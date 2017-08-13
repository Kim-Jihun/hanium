from django.shortcuts import render
from .decorators import bot
from . import functions
from shop.models import Post, Tag, Rating

@bot
def on_init(request):
    qs = Post.objects.filter(tag_set__name__icontains='sin')
    ordered_query = qs.order_by('-score')
    print(ordered_query)
    print("{},{}".format(ordered_query[0].title, ordered_query[0].image.url))
    return {'type': 'buttons', 'buttons': ['서울대입구 태그', '신촌태크', '나의 추천 맛집 보기']}

@bot
def on_message(request):

    user_key = request.JSON['user_key']
    type = request.JSON['type']
    content = request.JSON['content'] # photo 타입일 경우에는 이미지 URL

    if content.startswith('서울대'):
        qs = Post.objects.filter(tag_set__name__icontains='snu')
        ordered_query = qs.order_by('-score')
        response = ordered_query[0]
    elif content.startswith('신촌'):
        qs = Post.objects.filter(tag_set__name__icontains='sin')
        ordered_query = qs.order_by('-score')
        response = ordered_query[0]
    else:
        response='지원하는 답변이 아닙니다.'

    print(response)

    if isinstance(response, str):
        return {
            'message': {
                'text': response
            }
        }
    else:
        return {
            'message': {
                'text': response.title,
                'photo': response.image.url
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

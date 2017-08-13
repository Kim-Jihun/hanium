from django.shortcuts import render
from .decorators import bot
from . import functions
from shop.models import Post, Tag, Rating

@bot
def on_init(request):
    return {'type': 'buttons', 'buttons': ['서울대입구 태그', '신촌태크', '나의 추천 맛집 보']}

@bot
def on_message(request):

    '''

    user_key = request.JSON['user_key']
    type = request.JSON['type']
    content = request.JSON['content'] # photo 타입일 경우에는 이미지 URL

    if content.startswith('멜론검색:'):
        query = content[6:]
        response = '멜론 "{}" 검색결과\n\n'.format(query) + functions.melon_search(query)
    else:
        response = '지원하는 명령어가 아닙니다.'

    return {
        'message': {
            'text': response,
        }
    }



    '''

    '''
        #rated_qs=Rating.objects.select_related("shop").filter(user__username__icontains=request.user)
    #not_rated_qs=Rating.objects.select_related("shop").exclude(user__username__icontains=request.user)
    rated_qs = Post.objects.filter(rating__user__username__icontains=request.user)
    not_rated_qs = Post.objects.exclude(rating__user__username__icontains=request.user)

    '''

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
    #elif content.startswith('나의'):
    #    qs = Post.objects.filter(rating__user__username__icontains='')
    #    ordered_query = qs.order_by('-score')
    #    response = ordered_query[0]
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

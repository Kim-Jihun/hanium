from django.shortcuts import render, resolve_url
from .decorators import bot
from . import functions
from shop.models import Post, Tag, Rating
from django.http import JsonResponse
from django.db.models import Q

@bot
def on_init(request):

    return  {"type": "text" }



@bot
def on_message(request):

    user_key = request.JSON['user_key']
    type = request.JSON['type']
    content = request.JSON['content'] # photo 타입일 경우에는 이미지 URL



    if content != '다시 검색하기' or content !='나가기':

        list = content.split(',')
        new_list = []
        for i in list:
            new_list.append(i.strip())

        try:

            location = new_list[0]
            menu = new_list[1]
            price = new_list[2]

            query_set = Post.objects.filter(
                Q(tag_set__location__icontains=location)&Q(tag_set__menu__icontains=menu)
            ).order_by('-score')[0:7]

        except Exception:
            return {
                'message': {
                    'text': '지원하는 형식이 아닙니다. ,를 붙이시고 다시 입력해 주세요.',

                },

                "keyboard": {
                    "type": "text",
                }
            }
    elif content == '다시 검색하기':
        return {
            'message': {
                'text': 'Eatcha입니다! 맛집검색시 장소, 메뉴로 검색해 주세요, 높은 평점대로 보여드립니다!',
                'photo': {
                    #"url": 'https://s3.ap-northeast-2.amazonaws.com/eatcha' + response.image.url,
                    "url": 'http://blogfiles1.naver.net/20140806_24/eat_korea_1407302198842EXh5b_JPEG/K-2.jpg',
                    "width": 640,
                    "height": 480,
                },

                "message_button": {
                    "label": "상세 url로 이동",
                    "url": 'http://production.g3g2me2gp2.ap-northeast-2.elasticbeanstalk.com/shop/home/'
                    #"url": 'www.naver.com'
                },

            },
        }

    elif content != '그만 검색':
        return {
                'message': {
                    'text': '이용해 주셔서 감사합니다!',

                },

            }

    final_shop_list = []

    for i in query_set:
        tag = i.tag_set.all()[0]
        shop_temp = dict()
        shop_temp['이름'] = tag.title
        shop_temp['메뉴'] = tag.menu
        shop_temp['평균가격'] = tag.avg_price
        shop_temp['별점'] = i.score
        shop_temp['상세소개 url'] = 'http://production.g3g2me2gp2.ap-northeast-2.elasticbeanstalk.com'+resolve_url('shop:detail', id=i.id)
        final_shop_list.append(shop_temp)

    return {
        'message': {
            'text': '식당이름:' + final_shop_list,
        },

        "keyboard": {
            "type": "buttons",
            "buttons": [
              "다시 검색하기",
              "그만 검색",

            ]
         }
    }


'''
   return {
        'message': {
            'text': '식당이름:' + final_shop_list,
            'photo': {
                #"url": 'https://s3.ap-northeast-2.amazonaws.com/eatcha' + response.image.url,
                "url": 'https://s3.ap-northeast-2.amazonaws.com/eatcha/media/srchttp3A2F2Fblogfiles.naver.net2F20150529_1362Fwdojo_1432876822368n6oMb_JPEG2FIMG_7019.JPG',
                "width": 640,
                "height": 480,
            },
            "message_button": {
                "label": "상세 url로 이동",
                "url": 'http://production.g3g2me2gp2.ap-northeast-2.elasticbeanstalk.com'+resolve_url('shop:detail', id=response.id)
                #"url": 'www.naver.com'
            },

        },


        "keyboard": {
            "type": "buttons",
            "buttons": [
              "메뉴",
              "가격",
              "장소"
            ]
         }
    }
'''



'''
    return

if '장소' in content:
    return {'type': 'buttons', 'buttons': ['서울대입구', '신촌', '왕십리']}

elif content in ['서울대입구', '신촌', '왕십리'] :
    location = content
    return {'type': 'buttons', 'buttons': ['메뉴(#을 앞에 붙여주세)','가격']}
    #qs = Post.objects.filter(tag_set__location__icontains='신촌')
    #ordered_query = qs.order_by('-score')
    #response = ordered_query[0]

elif '메뉴' in content:

    #qs = Post.objects.filter(tag_set__location__icontains='왕십리')
    #ordered_query = qs.order_by('-score')
    #response = ordered_query[0]
    return {'type': 'text', 'buttons': ['가격']}



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
                #"url": 'https://s3.ap-northeast-2.amazonaws.com/eatcha' + response.image.url,
                "url": 'https://s3.ap-northeast-2.amazonaws.com/eatcha/media/srchttp3A2F2Fblogfiles.naver.net2F20150529_1362Fwdojo_1432876822368n6oMb_JPEG2FIMG_7019.JPG',
                "width": 640,
                "height": 480,
            },
            "message_button": {
                "label": "상세 url로 이동",
                "url": 'http://production.g3g2me2gp2.ap-northeast-2.elasticbeanstalk.com'+resolve_url('shop:detail', id=response.id)
                #"url": 'www.naver.com'
            },

        },


        "keyboard": {
            "type": "buttons",
            "buttons": [
              "메뉴",
              "가격",
              "장소"
            ]
         }
    }


}'''




@bot
def on_added(request):
    user_key = request.JSON['user_key']

@bot
def on_block(request, user_key):
    pass

@bot
def on_leave(request, user_key):
    pass
